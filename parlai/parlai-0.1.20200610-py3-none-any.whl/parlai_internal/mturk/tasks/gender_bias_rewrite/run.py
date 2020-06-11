#!/usr/bin/env python3

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from parlai.core.params import ParlaiParser
from worlds import GenderRewriteOnboarding, GenderRewriteWorld
from parlai.mturk.core.mturk_manager import MTurkManager
import parlai.mturk.core.mturk_utils as mutils
from parlai_internal.mturk.tasks.wizard_model_eval.mtdont import MTDONT_LIST
from parlai_internal.mturk.tasks.gender_bias_rewrite.aggregate_hits import BAD_TURKERS
from parlai_internal.mturk.tasks.single_turn_safety_review.run import (
    TrackOnboardingCompletion,
)
from parlai_internal.tasks.gender_multiclass.new_data import NewData1Teacher
from task_config import task_config

import json
import os
import pickle
import random
import threading
import time


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


class GetRewriteStack(object):
    # TODO: rewrite this to do a random selection instead
    def __init__(self, opt):
        save_dir = opt.get('save_dir')
        self.sandbox = opt.get('is_sandbox')
        version_num = opt.get('version_num', 0)
        self.version_str = '_v{}'.format(version_num)

        if self.sandbox:
            self.JSON_PATH = os.path.join(save_dir, 'sandbox', 'completed_stack.json')
        else:
            self.JSON_PATH = os.path.join(
                save_dir, 'completed_stack{}.json'.format(self.version_str)
            )

        ensure_dir(self.JSON_PATH)

        self.num_per_eval = opt.get('num_per_eval', 5)

        self.stack = []
        self.completed_list = []
        self.load_stack()

        self.save_stack_interval = 60
        self.last_save_time = time.time()
        self.save_lock = threading.RLock()
        self.save_stack()

    def add_to_completed(self, evaluated, confidences, worker):
        self.completed_list.append((evaluated, confidences, worker))

    def load_stack(self):
        if os.path.isfile(self.JSON_PATH):
            with open(self.JSON_PATH, 'r') as f:
                self.completed_list = json.loads(f.read())
        self.stack = []
        teacher = NewData1Teacher(
            {'labels_to_use': 'all', 'datatype': 'train', 'balance': False}
        )
        for ex in teacher.data:
            self.stack.append((ex['text'], ex['labels'][0]))

    def save_stack(self):
        if time.time() - self.last_save_time > self.save_stack_interval:
            with self.save_lock:
                # save data
                print('Saving all data to {}.'.format(self.JSON_PATH))
                data = json.dumps(self.completed_list)
                with open(self.JSON_PATH, 'w') as f:
                    f.write(data)
                self.last_save_time = time.time()

    def get_next_stack(self):
        """
        Get a new stack to re-write.
        """
        to_return_text = []
        to_return = []
        while len(to_return) < self.num_per_eval:
            tmp = random.choice(self.stack)
            if tmp[0] not in to_return_text:
                to_return.append(tmp)
                to_return_text.append(tmp[0])

        return random.sample(self.stack, self.num_per_eval)


class TrackOnboardingCompletion(object):
    def __init__(self, opt):
        save_dir = opt.get('save_dir')
        version_num = opt.get('version_num', 0)
        self.list_path = os.path.join(
            save_dir, 'completed_onboarding_v{}.txt'.format(version_num)
        )
        self.blocked_path = os.path.join(
            save_dir, 'blocked_onboarding_v{}.txt'.format(version_num)
        )
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
    an MTurk manager and configuring it for the single_turn_safety task.
    """
    # Get relevant arguments
    argparser = ParlaiParser(False, False)
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()
    # TODO: create a file with the data for review
    argparser.add_argument(
        '--save-dir',
        type=str,
        default='/private/home/edinan/ParlAI/data/gender_annotations/',
        help='where to save partial data',
    )
    argparser.add_argument(
        '--evals-per-cand',
        type=int,
        default=1,
        help='number of evaluations per candidate',
    )
    argparser.add_argument(
        '--num-per-eval', type=int, default=5, help='number of candidates per HIT'
    )
    argparser.add_argument(
        '--run-onboard', type='bool', default=True, help='run onboard to as a test'
    )
    argparser.add_argument(
        '--auto-approve-delay',
        type=int,
        default=3600 * 24 * 2,
        help='how long to wait for auto approval (default ' 'is two days)',
    )
    argparser.add_argument(
        '--version-num', type=int, default=0, help='increase this to create a new stack'
    )
    argparser.set_params(tmpdir='/tmp/')
    opt = argparser.parse_args()

    # Set the task name to be the folder name
    opt['task'] = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

    # append the contents of task_config.py to the configuration
    opt.update(task_config)

    eval_stacks = GetRewriteStack(opt)

    # Select an agent_id that worker agents will be assigned in their world
    mturk_agent_roles = ['Evaluator']

    # Instantiate an MTurkManager with the given options and a maximum number
    # of agents per world of 1 (based on the length of mturk_agent_ids)
    mturk_manager = MTurkManager(
        opt=opt, mturk_agent_ids=mturk_agent_roles, use_db=True,
    )

    mturk_manager.setup_server(
        task_directory_path=os.path.dirname(os.path.abspath(__file__))
    )

    onboarding_tracker = TrackOnboardingCompletion(opt)

    # Create an onboard_function, which will be run for workers who have
    # accepted your task and must be completed before they are put in the
    # queue for a task world.
    def run_onboard(worker):
        nonlocal onboarding_tracker
        if onboarding_tracker.did_worker_complete(worker.worker_id):
            return
        else:
            role = mturk_agent_roles[0]
            worker.update_agent_id('Onboarding {}'.format(role))
            world = GenderRewriteOnboarding(
                opt=opt, mturk_agent=worker, onboarding_tracker=onboarding_tracker,
            )
            while not world.episode_done():
                world.parley()
            world.shutdown()
            onboarding_tracker.mark_worker_completed(worker.worker_id)
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
        qual_desc = 'Completed maximum amount of rewrites for this task.'
        qual_name = 'CompletedMaxReviewEvalsGender'
        qualification_id = mutils.find_or_create_qualification(
            qual_name, qual_desc, False, must_be_owned=True
        )
        print('Found or created qualification: ', qualification_id)
        max_qualif = {
            'QualificationTypeId': qualification_id,
            'Comparator': 'DoesNotExist',
            'RequiredToPreview': True,
        }
        qualifications = [max_qualif]

        if not opt.get('is_sandbox'):
            # ADD BLOCKED WORKERS HERE
            blocked_worker_list = MTDONT_LIST + BAD_TURKERS

            for w in blocked_worker_list:
                try:
                    print('Soft blocking worker: {}'.format(w))
                    mturk_manager.give_worker_qualification(w, qual_name)
                except:
                    print('Did not soft block worker:', w)
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
            stack = eval_stacks.get_next_stack()

            # Create the task world
            world = GenderRewriteWorld(
                opt=opt, mturk_agents=workers, evaluation_stack=stack
            )
            # run the world to completion
            while not world.episode_done():
                world.parley()

            # shutdown and review the work
            world.shutdown()
            completed, evaluated, confidences = world.review_work()
            if completed:
                eval_stacks.add_to_completed(
                    evaluated, confidences, workers[0].worker_id
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


if __name__ == '__main__':
    main()
