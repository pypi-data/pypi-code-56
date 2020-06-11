#!/usr/bin/env python3

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import json
import os
import pickle
import random
import threading
import time

import parlai.mturk.core.mturk_utils as mutils
from parlai.core.params import ParlaiParser
from parlai.mturk.core.mturk_manager import MTurkManager
from parlai_internal.mturk.tasks.wizard_model_eval.mtdont import MTDONT_LIST

from task_config import task_config
from worlds import (
    SafetyOnboardingWorld,
    SafetyWorld,
    BAD_CAND_PATH,
    DATA_PATHS,
    FLAGGING_FIELDS,
    QUAL_NAME,
    SAVE_FOLDER,
)


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


class GetEvaluationStack(object):
    def __init__(self, opt, has_flag=True):
        save_dir = opt.get('save_dir')
        self.sandbox = opt.get('is_sandbox')
        version_num = opt.get('version_num', 0)
        self.version_str = '_v{}'.format(version_num)
        self.has_flag = has_flag

        if self.sandbox:
            base_folder = os.path.join(save_dir, 'sandbox')
            if has_flag:
                self.SAFETY_FLAG_PATH = os.path.join(
                    base_folder, 'flagged_list__safety.json'
                )
            self.JSON_PATH = os.path.join(base_folder, 'completed_stack.json')
        else:
            if has_flag:
                self.SAFETY_FLAG_PATH = os.path.join(
                    save_dir, 'flagged_list{}__safety.json'.format(self.version_str)
                )
            self.JSON_PATH = os.path.join(
                save_dir, 'completed_stack{}.json'.format(self.version_str)
            )

        if has_flag:
            ensure_dir(self.SAFETY_FLAG_PATH)

        ensure_dir(self.JSON_PATH)

        self.num_per_eval = opt['num_per_eval']
        self.total_evals = opt['evals_per_cand']
        self.pointer = 0

        self.stack = {}
        self.flagging_fields = FLAGGING_FIELDS
        self.flagged_lists = {'safety': {}}
        self.build_or_load_stack(opt)
        self.next_stack_lock = threading.RLock()

        self.save_stack_interval = 60
        self.last_save_time = time.time()
        self.save_lock = threading.RLock()
        self.save_stack()

    def flag(
        self, stack_idx: int, text_idx: int, flag_type: str, responses: dict, worker_id
    ):
        idx = stack_idx * self.num_per_eval + text_idx
        fields = self.flagging_fields[flag_type]
        if idx in self.flagged_lists[flag_type]:
            self.flagged_lists[flag_type][idx]['workers'].append(worker_id)
            for field in fields:
                self.flagged_lists[flag_type][idx][field].append(responses[field])
        else:
            self.flagged_lists[flag_type][idx] = {}
            self.flagged_lists[flag_type][idx]['workers'] = [worker_id]
            for field in fields:
                self.flagged_lists[flag_type][idx][field] = [responses[field]]

    def load_stack(self):
        print(f'[ Loading stack from file... {self.JSON_PATH}]')
        with open(self.JSON_PATH, 'r') as f:
            self.stack = json.loads(f.read())
            # find pointer
            found = False
            while not found:
                if len(self.stack[str(self.pointer)]['workers']) >= self.total_evals:
                    self.pointer += 1
                else:
                    found = True
        if self.has_flag:
            with open(self.SAFETY_FLAG_PATH, 'r') as g:
                self.flagged_lists['safety'] = json.loads(g.read())

    def build_stack(self, opt):
        print('[ Building stack from original file... ]')
        data_file = opt.get('data_file') or DATA_PATHS[opt.get('version_num')]
        with open(data_file, 'r') as f:
            message_params = json.load(f)

        stack_idx = 0
        curr_stack = []
        for txt_idx, params in enumerate(message_params):
            if txt_idx % self.num_per_eval == 0 and txt_idx != 0:
                self.stack[str(stack_idx)] = {'stack': curr_stack, 'workers': []}
                stack_idx += 1
                curr_stack = [params['message']]
            else:
                curr_stack.append(params['message'])

    def build_or_load_stack(self, opt):
        # check if this stack has been partially completed
        if os.path.isfile(self.JSON_PATH):
            self.load_stack()
            return

        self.build_stack(opt)

    def save_stack(self):
        if time.time() - self.last_save_time > self.save_stack_interval:
            with self.save_lock:
                # save data
                print('Saving all data to {}.'.format(self.JSON_PATH))
                data = json.dumps(self.stack)
                with open(self.JSON_PATH, 'w') as f:
                    f.write(data)
                self.last_save_time = time.time()

                # save flagged info
                if self.has_flag:
                    print(f'Saving all flagged items to {self.SAFETY_FLAG_PATH}.')
                    safety_flags = json.dumps(self.flagged_lists['safety'])
                    with open(self.SAFETY_FLAG_PATH, 'w') as g:
                        g.write(safety_flags)

    def get_next_stack(self, worker_id):
        """Returns the next stack for a given worker id, checking to see if
        they've reviewed this stack before. Should be called under lock."""
        with self.next_stack_lock:
            worker_done = False  # assign worker qualification to prevent more work

            # check against worker_id to see if they've completed this before
            stack = self.stack.get(str(self.pointer))
            while stack is not None and len(stack['workers']) >= self.total_evals:
                self.pointer += 1
                print('Pointer at {}'.format(self.pointer))
                stack = self.stack.get(str(self.pointer))

            worker_pointer = self.pointer
            while stack is not None and worker_id in stack['workers']:
                worker_pointer += 1
                stack = self.stack.get(str(worker_pointer))

            if stack is None:
                print('Getting a random stack for worker {}'.format(worker_id))
                key = random.choice(list(self.stack.keys()))
                stack = self.stack[key]
                worker_pointer = int(key)
                worker_done = True

            self.save_stack()
            print(
                'Retrieving stack {} for worker {}.'.format(worker_pointer, worker_id)
            )
            stack['workers'].append(worker_id)

            return worker_pointer, stack['stack'], worker_done

    def remove_worker_from_stack(self, worker, stack_index):
        if worker in self.stack[str(stack_index)]['workers']:
            print(f'Removing worker {worker} from stack {stack_index:d}.')
            self.stack[str(stack_index)]['workers'].remove(worker)
            if stack_index < self.pointer:
                print(f'Moving pointer from {self.pointer:d} to {stack_index:d}.')
                self.pointer = stack_index
        else:
            print(f'Worker {worker} not found in stack {stack_index:d}.')


class TrackOnboardingCompletion(object):
    def __init__(self, save_dir: str):
        self.list_path = os.path.join(save_dir, 'completed_onboarding.txt')
        self.blocked_path = os.path.join(save_dir, 'blocked_onboarding.txt')
        ensure_dir(self.list_path)
        self.completed = self.load_completion_list()
        self.soft_blocked = self.load_soft_blocked_list()
        self.list_lock = threading.RLock()
        self.block_lock = threading.RLock()

    def did_worker_complete(self, worker_id):
        with self.list_lock:
            return True if worker_id in self.completed else False

    def mark_worker_completed(self, worker_id):
        with self.list_lock:
            if worker_id not in self.completed:
                self.completed.append(worker_id)
            # now save list
        self.save_completion_list()

    def save_completion_list(self):
        print('Saving onboarding completion list to {}.'.format(self.list_path))
        with self.list_lock:
            with open(self.list_path, 'wb') as g:
                pickle.dump(self.completed, g)

    def remove_worker_from_completion_list(self, worker_id):
        with self.list_lock:
            if worker_id in self.completed:
                self.completed.remove(worker_id)

    def load_completion_list(self):
        if os.path.isfile(self.list_path):
            with open(self.list_path, 'rb') as f:
                completed = pickle.load(f)
            return completed
        return []

    def was_worker_blocked(self, worker_id):
        with self.block_lock:
            return True if worker_id in self.soft_blocked else False

    def mark_worker_blocked(self, worker_id):
        with self.block_lock:
            self.soft_blocked.append(worker_id)
        # save list
        self.save_blocked_list()

    def save_blocked_list(self):
        print('Saving blocked list to {}.'.format(self.blocked_path))
        with self.block_lock:
            with open(self.blocked_path, 'wb') as g:
                pickle.dump(self.soft_blocked, g)

    def load_soft_blocked_list(self):
        if os.path.isfile(self.blocked_path):
            with open(self.blocked_path, 'rb') as f:
                blocked = pickle.load(f)
            return blocked
        return []


def main():
    """Handles setting up and running a ParlAI-MTurk task by instantiating
    an MTurk manager and configuring it for the safety_filtering_and_rewriting task.
    """
    # Get relevant arguments
    argparser = ParlaiParser(False, False)
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()
    argparser.add_argument(
        '--data-file', type=str, default=None, help='Path to data file'
    )
    argparser.add_argument(
        '--save-dir', type=str, default=SAVE_FOLDER, help='where to save partial data'
    )
    argparser.add_argument(
        '--evals-per-cand',
        type=int,
        default=2,
        help='number of evaluations per candidate',
    )
    argparser.add_argument(
        '--num-per-eval', type=int, default=20, help='number of candidates per HIT'
    )
    argparser.add_argument(
        '-mx_rsp_time',
        '--max_resp_time',
        type=int,
        default=90,
        help='time limit for entering a dialog message',
    )
    argparser.add_argument(
        '--run-onboard', type='bool', default=True, help='run onboard to as a test'
    )
    argparser.add_argument(
        '--bad-cand-fraction',
        type=float,
        default=0.25,
        help='The fraction of HITs to add a bad candidate to as a check',
    )
    argparser.add_argument(
        '--bad-cand-list',
        type=str,
        default=BAD_CAND_PATH,
        help='list of bad candidates to check Turker ability',
    )
    # The default file is a subset of /private/home/edinan/ParlAI/data/safety_checks/offensive_list_twitter.txt
    argparser.add_argument(
        '--auto-approve-delay',
        type=int,
        default=3600 * 24 * 5,
        help='how long to wait for auto approval',
    )
    argparser.add_argument(
        '--version-num', type=int, default=0, help='increase this to create a new stack'
    )
    argparser.set_defaults(
        num_conversations=100,
        max_hits_per_worker=300,
        reward=0.33,
        allowed_conversations=1,
    )
    opt = argparser.parse_args()

    # Set the task name to be the folder name
    opt['task'] = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

    # append the contents of task_config.py to the configuration
    opt.update(task_config)

    # build evaluation stack
    eval_stacks = GetEvaluationStack(opt)

    if opt.get('bad_cand_fraction') > 0 and os.path.isfile(opt.get('bad_cand_list')):
        with open(opt.get('bad_cand_list'), 'r') as f:
            bad_cands = [cand.strip() for cand in f.readlines()]
    else:
        bad_cands = None
    worker_watch_list = []

    # Select an agent_id that worker agents will be assigned in their world
    mturk_agent_roles = ['Evaluator']

    # Instantiate an MTurkManager with the given options and a maximum number
    # of agents per world of 1 (based on the length of mturk_agent_ids)
    mturk_manager = MTurkManager(
        opt=opt, mturk_agent_ids=mturk_agent_roles, use_db=True
    )

    mturk_manager.setup_server(
        task_directory_path=os.path.dirname(os.path.abspath(__file__))
    )

    if opt['save_dir'] is None:
        raise ValueError("--save-dir must not be None!")

    # Get onboarding folder
    if opt['is_sandbox']:
        onboarding_save_dir = os.path.join(opt['save_dir'], 'sandbox', 'onboarding')
    else:
        onboarding_save_dir = os.path.join(opt['save_dir'], 'onboarding')
    os.makedirs(onboarding_save_dir, exist_ok=True)

    onboarding_tracker = TrackOnboardingCompletion(save_dir=onboarding_save_dir)

    # Create an onboard_function, which will be run for workers who have
    # accepted your task and must be completed before they are put in the
    # queue for a task world.
    def run_onboard(worker):
        orig_worker_id = worker.worker_id
        worker.worker_id = clean_worker_id(orig_worker_id)
        nonlocal onboarding_tracker
        if onboarding_tracker.was_worker_blocked(worker.worker_id):
            print(
                f'WARNING: {orig_worker_id} attempting to take new HIT after being '
                f'blocked!'
            )
            # TODO: I'm not sure if it helps to try to "re-block" them...
            mturk_manager.give_worker_qualification(worker.worker_id, QUAL_NAME)
            if orig_worker_id != worker.worker_id:
                # TODO: change when you know if this blocking of the duplicated ID works
                try:
                    mturk_manager.give_worker_qualification(orig_worker_id, QUAL_NAME)
                    print(f'Gave {orig_worker_id} qualification.')
                except Exception as e:
                    print(f'WARNING: did not soft block worker {orig_worker_id}: {e}')
        elif onboarding_tracker.did_worker_complete(worker.worker_id):
            return
        else:
            role = mturk_agent_roles[0]
            worker.update_agent_id('Onboarding {}'.format(role))
            world = SafetyOnboardingWorld(
                opt=opt,
                mturk_agent=worker,
                onboarding_tracker=onboarding_tracker,
                max_resp_time=opt['max_resp_time'],
                save_dir=onboarding_save_dir,
            )
            while not world.episode_done():
                world.parley()
            world.shutdown()
            return world.prep_save_data([worker])

    if opt.get('run_onboard'):
        mturk_manager.set_onboard_function(onboard_function=run_onboard)

    try:
        # Initialize run information
        mturk_manager.start_new_run()

        # Set up the sockets and threads to recieve workers
        mturk_manager.ready_to_accept_workers()

        # Create a qualification to ensure a worker won't repeat evaluations
        # This will become necessary toward the end of the stack
        qual_desc = 'Qualification to ensure worker does not repeat evaluations.'
        qualification_id = mutils.find_or_create_qualification(
            QUAL_NAME, qual_desc, False, must_be_owned=True
        )
        print('Found or created qualification: ', qualification_id)
        max_qualif_new = {
            'QualificationTypeId': qualification_id,
            'Comparator': 'DoesNotExist',
            'RequiredToPreview': True,
        }
        qualifications = [max_qualif_new]

        if not opt.get('is_sandbox'):
            additional_blocked_worker_list = [
                'A3HFS6Q0TONAB9'  # Made up many nonsense offensiveness percentages
            ]
            blocked_worker_list = MTDONT_LIST + additional_blocked_worker_list
            for worker_id in blocked_worker_list:
                try:
                    print(f'Soft blocking worker: {worker_id}')
                    mturk_manager.give_worker_qualification(worker_id, QUAL_NAME)
                except:
                    print('Did not soft block worker:', worker_id)
                time.sleep(0.1)

        # Create the hits as specified by command line arguments
        mturk_manager.create_hits(qualifications=qualifications)

        def check_workers_eligibility(workers):
            return workers

        # Assign worker roles is used to determine what the role each worker
        # in the given worker list will play. Setting `id` to None will return
        # the worker to the pool rather than putting them in a given task,
        # which is useful for having tasks with different possible worker
        # counts.
        def assign_worker_roles(workers):
            for worker in workers:
                worker.id = mturk_agent_roles[0]

        # Define the task function, which will be run with workers that are
        # as the main task.
        global run_conversation

        def run_conversation(mturk_manager, opt, workers):

            workers[0].worker_id = clean_worker_id(workers[0].worker_id)

            idx, stack, done = eval_stacks.get_next_stack(workers[0].worker_id)

            if bad_cands is not None:
                if random.random() < opt['bad_cand_fraction']:
                    bad_cand = random.choice(bad_cands)
                else:
                    bad_cand = None
            else:
                bad_cand = None

            # Create the task world
            world = SafetyWorld(
                mturk_agents=workers,
                evaluation_stack=stack,
                stack_idx=idx,
                max_resp_time=opt['max_resp_time'],
                bad_cand=bad_cand,
            )
            # run the world to completion
            while not world.episode_done():
                world.parley()

            # shutdown and review the work
            world.shutdown()
            completed, safety_flagged, block_worker = world.review_work()

            if block_worker and not opt.get('is_sandbox'):

                # soft block worker
                worker_id = workers[0].worker_id
                worker_watch_list.append(worker_id)
                # list of workers who did not mark reddit candidate as offensive
                print('Updated worker watch list: {}'.format(worker_watch_list))
                try:
                    print('Soft blocking worker: {}\n'.format(worker_id))
                    mturk_manager.give_worker_qualification(worker_id, QUAL_NAME)
                except:
                    print('Did not soft block worker:', worker_id)

                # remove worker from stack
                eval_stacks.remove_worker_from_stack(workers[0].worker_id, idx)

            # add any flagged items to the flagged lists
            if len(safety_flagged) > 0:
                for key in safety_flagged.keys():
                    text_idx = int(key)
                    eval_stacks.flag(
                        stack_idx=idx,
                        text_idx=text_idx,
                        flag_type='safety',
                        responses=safety_flagged[key],
                        worker_id=workers[0].worker_id,
                    )

            if not completed:
                eval_stacks.remove_worker_from_stack(workers[0].worker_id, idx)

            if done:
                # give worker qualification to prevent them from working on
                # more tasks
                mutils.give_worker_qualification(
                    workers[0].worker_id, qualification_id, value=None, is_sandbox=False
                )

            # Return the contents for saving
            return world.prep_save_data(workers)

        # Begin the task, allowing mturk_manager to start running the task
        # world on any workers who connect
        mturk_manager.start_task(
            eligibility_function=check_workers_eligibility,
            assign_role_function=assign_worker_roles,
            task_function=run_conversation,
        )
    except BaseException:
        raise
    finally:
        eval_stacks.save_stack()
        onboarding_tracker.save_completion_list()
        # Any hits that aren't claimed or completed have to be shut down. Must
        # keep the world running until that point.
        mturk_manager.expire_all_unassigned_hits()
        # Shutdown the manager and free all related resources
        mturk_manager.shutdown()


def clean_worker_id(worker_id: str) -> str:
    """
    Fix issue where worker ID is sometimes duplicated.
    """
    if ',' not in worker_id:
        return worker_id
    else:
        worker_id_parts = worker_id.split(',')
        assert len(worker_id_parts) == 2 and worker_id_parts[0] == worker_id_parts[1]
        print(f'Worker {worker_id_parts[0]} has had their ID de-duplicated.')
        return worker_id_parts[0]


if __name__ == '__main__':
    main()
