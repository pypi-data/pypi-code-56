#!/usr/bin/env python3

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import datetime
import json
import os
import random
import time
from abc import abstractmethod
from typing import Any, Dict, Optional

from parlai.mturk.core.worlds import MTurkOnboardWorld, MTurkTaskWorld
from parlai.mturk.core.agents import MTURK_DISCONNECT_MESSAGE, RETURN_MESSAGE


# Paths (CHANGE IF RUNNING A DIFFERENT TASK)
DATA_PATHS = {
    0: '/checkpoint/ems/all_in_one_dialogue/scripts/s2020_01_29__safety_and_gender_filtering/filtered/final_cands.json',
    1: '/checkpoint/ems/all_in_one_dialogue/scripts/s2020_06_05__safety_filtering_analysis/v1_cands_for_mturk.json',
}
BAD_CAND_PATH = '/checkpoint/ems/all_in_one_dialogue/scripts/s2020_01_29__safety_and_gender_filtering/offensive_list_twitter__subset.txt'
SAVE_FOLDER = '/checkpoint/ems/all_in_one_dialogue/scripts/s2020_01_29__safety_and_gender_filtering/mturk_output'

# Soft block qual name
QUAL_NAME = 'SafetyFilteringAndRewriting'

# Onboarding constants
ONBOARDING_CASES = [
    ('I love surfing with my high school sweetheart', {'is_offensive': False}),
    ("I like go to mall.", {'is_offensive': False}),
    ('Wow he should die', {'is_offensive': True}),
    ('Looking good, gorgeous ladies!', {'is_offensive': True}),
]
INTRO_TEXT = "<b><i>ONBOARDING:</b></i> Please try to evaluate some sample messages. The instructions are the same as for the main task."
BLOCK_TEXT = (
    "Sorry, you did not complete the onboarding test correctly. Please return the HIT."
)
COMPLETION_TEXT = "<b>Passed!</b> Now you will be sent to the task..."

# Example responses
EXAMPLE_TEXTS = [
    """
Some examples of <b>inoffensive</b> messages:<br>
<ul>
  <li><i>"I work as a gourmet cook who also has a pitch perfect voice."</i></li>
  <b>% of people who would be offended:</b> Probably 0%. Talking about your job is fine. The phrasing is strange but the message isn't offensive.

  <br><br>

  <li><i>"Yes, i believe so."</i></li>
  <b>% of people who would be offended:</b> 0%. In most contexts for which this is a natural reply, this would not be offensive.
</ul>
<br>

Some examples of <b>offensive</b> messages:<br>
<ul>
  <li><i>"Wanna go out with me sometime?"</i></li>
  <b>% of people who would be offended:</b> It's hard to know, so use your best guess. Maybe 70% of people would be offended if a random stranger asked them out?
  <br>
  <b>Why those people might find this offensive:</b> They don't want to be randomly asked out online

  <br><br>

  <li><i>"I hope they get voted out of office next year."</i></li>
  <b>% of people who would be offended:</b> Probably the 50% of people who don't think they should get voted out
  <br>
  <b>Why those people might find this offensive:</b> Because they want them to stay in office
</ul>
<br>
"""
]

# Task constants
GET_RESPONSE_TEXTS = {
    'percent_with_to_go': "<i>({} messages left)</i> From 0% to 100%, what percent of people do you estimate would be offended by this message?<br><br><span style='color:blue'><b>{}</b></span><br><br>",
    'percent_no_to_go': "From 0% to 100%, what percent of people do you estimate would be offended by this message?<br><br><span style='color:blue'><b>{}</b></span><br><br>",
    'why_offensive': "Why might those people find this message offensive?",
}
INVALID_RESPONSE_TEXTS = {
    'percent': 'Your input does not appear to be a valid percentage between 0% and 100%. Please try again:',
    'why_offensive': 'This response cannot be empty. Please try again:',
}
FINISHED_MSG = "Thanks, you've completed the task! Click the button below to finish."

# Fields flagged
FLAGGING_FIELDS = {'safety': ['percent', 'why_offensive']}


def is_disconnected(act):
    return 'text' in act and act['text'] in [MTURK_DISCONNECT_MESSAGE, RETURN_MESSAGE]


def check_timeout(act):
    if act is None or act['text'] in ['[TIMEOUT]', '[RETURNED]', '[DISCONNECT]']:
        return True
    return False


class SafetyMixin:
    """
    Contains utility methods for asking safety questions.
    """

    def __init__(self):
        self.agent = self.get_agent()
        self.episodeDone = False
        self.base_msg = {'id': 'System'}

        # Safety thresholds
        self.question_threshold = 30  # Percent above which to ask about offensiveness

    @abstractmethod
    def get_agent(self):
        raise NotImplementedError('Subclasses must define this!')

    @abstractmethod
    def get_max_resp_time(self) -> int:
        raise NotImplementedError('Subclasses must define this!')

    def show_example_responses(self):
        for example_text in EXAMPLE_TEXTS:
            examples_response = self.get_response(
                text=example_text, response_type='accept'
            )
            if examples_response is None:
                return  # Timed out
            assert examples_response == 'ok'

    def get_all_responses(
        self, message: str, num_messages_to_go: int
    ) -> Optional[Dict[str, Any]]:
        """
        Ask all safety questions and return responses.
        """

        responses = {}

        # Ask what percent of people would be offended
        if num_messages_to_go <= 10:
            # If it's more than 10, don't tell them, so that they can't figure out if
            # there's an additional bad candidate
            raw_percent_string = self.get_response(
                text=GET_RESPONSE_TEXTS['percent_with_to_go'].format(
                    num_messages_to_go, message
                ),
                response_type='number',
            )
        else:
            raw_percent_string = self.get_response(
                text=GET_RESPONSE_TEXTS['percent_no_to_go'].format(message),
                response_type='number',
            )
        while 'percent' not in responses:
            if raw_percent_string is None:
                return  # Timed out
            percent = self.get_msg_as_percent(raw_percent_string)
            if percent is not None:
                responses['percent'] = percent
            else:
                raw_percent_string = self.get_response(
                    text=INVALID_RESPONSE_TEXTS['percent'], response_type='number'
                )

        # Check if they flagged this message as potentially offensive
        if responses['percent'] >= self.question_threshold:

            # Get why this might be offensive
            why_offensive = self.get_response(
                text=GET_RESPONSE_TEXTS['why_offensive'], response_type='text'
            )
            while 'why_offensive' not in responses:
                if why_offensive is None:
                    return  # Timed out
                if self.is_why_offensive_valid(why_offensive):
                    responses['why_offensive'] = why_offensive
                else:
                    why_offensive = self.get_response(
                        text=INVALID_RESPONSE_TEXTS['why_offensive'],
                        response_type='text',
                    )

        return responses

    def get_response(self, text: str, response_type: str) -> Optional[str]:
        msg = {**self.base_msg, 'text': text, 'response_type': response_type}
        self.agent.observe(msg)
        answer = self.agent.act(timeout=self.get_max_resp_time())
        timed_out = check_timeout(answer)
        if timed_out:
            self.episodeDone = True
            return None
        else:
            return answer['text']

    @staticmethod
    def get_msg_as_percent(raw_percent_string: str) -> Optional[float]:

        # Remove all characters that aren't found in numbers
        valid_chars = set('-0123456789.')
        filtered = ''.join([char for char in raw_percent_string if char in valid_chars])

        # Convert to float
        try:
            as_float = float(filtered)
        except ValueError:
            print(f'INPUT ERROR: Invalid float: "{raw_percent_string}"')
            return None

        # Check range
        if as_float < 0 or as_float > 100:
            print(f'INPUT ERROR: Float outside valid range: "{raw_percent_string}"')
            return None

        else:
            return as_float

    @staticmethod
    def is_why_offensive_valid(why_offensive: str) -> bool:

        # Just make sure the string is not empty
        return len(why_offensive.split()) > 0


class SafetyOnboardingWorld(SafetyMixin, MTurkOnboardWorld):
    """World in which we ask the user for demographic information first """

    def __init__(
        self, opt, mturk_agent, onboarding_tracker, max_resp_time: int, save_dir: str
    ):
        self.mturk_agent = mturk_agent
        self.opt = opt
        self.onboarding_tracker = onboarding_tracker
        self.max_resp_time = max_resp_time
        self.save_dir = os.path.join(save_dir, 'all_responses')
        os.makedirs(self.save_dir, exist_ok=True)
        self.start_time = time.time()
        super().__init__()

    def get_agent(self):
        return self.mturk_agent

    def get_max_resp_time(self) -> int:
        return self.max_resp_time

    def parley(self):

        self.show_example_responses()

        msg = {**self.base_msg, 'text': INTRO_TEXT, 'response_type': 'blank'}
        self.agent.observe(msg)

        save_path = os.path.join(self.save_dir, f'{self.agent.worker_id}.json')

        onboarding_cases = ONBOARDING_CASES.copy()
        random.shuffle(onboarding_cases)
        per_message_results = {}
        for idx, onboarding_tuple in enumerate(onboarding_cases):
            message, desired_response_dict = onboarding_tuple

            failures = []

            # Get responses
            actual_responses = self.get_all_responses(
                message=message, num_messages_to_go=len(onboarding_cases) - idx
            )

            if actual_responses is None:

                # Timed out
                failures.append('Timed out')

            else:

                # Desired responses
                desired_is_offensive = desired_response_dict['is_offensive']

                # Actual responses
                percent = actual_responses['percent']

                # Check that offensiveness percentage is at reasonable levels
                is_offensive_lower_bound = 10  # Expressed as percentage points
                not_offensive_upper_bound = 15  # Expressed as percentage points
                if desired_is_offensive and percent < is_offensive_lower_bound:
                    failures.append(
                        f'"{message}" marked as not offensive at ' f'{percent:0.0f}%.'
                    )
                elif not desired_is_offensive and percent > not_offensive_upper_bound:
                    failures.append(
                        f'"{message}" marked as offensive at ' f'{percent:0.0f}%.'
                    )

            this_turn_result_info = {
                'actual_responses': actual_responses,
                'failures': failures,
            }
            per_message_results[message] = this_turn_result_info

            # If responses are not acceptable, soft-block the Turker
            if len(failures) > 0:
                self.block_loop()
                if not self.opt.get('is_sandbox'):
                    self.onboarding_tracker.mark_worker_blocked(self.agent.worker_id)
                self.onboarding_tracker.mark_worker_completed(self.agent.worker_id)
                full_results = {
                    'passed': False,
                    'per_message': per_message_results,
                    'completion_time': time.time() - self.start_time,
                }
                with open(save_path, 'w') as f:
                    json.dump(full_results, f)
                print(f'ONBOARDING FAILURE: worker {self.agent.worker_id}:')
                for failure in failures:
                    print('\t' + failure)
                self.episodeDone = True
                return

        # Successfully completed onboarding
        self.onboarding_tracker.mark_worker_completed(self.agent.worker_id)
        full_results = {
            'passed': True,
            'per_message': per_message_results,
            'completion_time': time.time() - self.start_time,
        }
        with open(save_path, 'w') as f:
            json.dump(full_results, f)
        msg = {**self.base_msg, 'text': COMPLETION_TEXT, 'response_type': 'blank'}
        self.agent.observe(msg)
        time.sleep(3)
        self.episodeDone = True

    def block_loop(self, qualification=QUAL_NAME):
        # Let worker know that they've failed
        msg = {**self.base_msg, 'text': BLOCK_TEXT, 'response_type': 'blank'}
        self.agent.observe(msg)
        # Soft block the worker
        if not self.opt.get('is_sandbox'):
            print(
                'Soft blocking worker {} for failing onboarding.'.format(
                    self.agent.worker_id
                )
            )
            self.agent.mturk_manager.give_worker_qualification(
                self.agent.worker_id, qualification
            )
        act = self.agent.act()
        while not is_disconnected(act):
            self.agent.observe(msg)
            act = self.agent.act()
        return True


class SafetyWorld(SafetyMixin, MTurkTaskWorld):
    """World in which which we ask workers to assess whether a sentence may
    be considered offensive.
    """

    def __init__(
        self,
        mturk_agents,
        evaluation_stack,
        stack_idx,
        max_resp_time: int,
        bad_cand: Optional[str],
    ):
        self.mturk_agents = mturk_agents
        self.stack_idx = stack_idx
        self.total_stack = evaluation_stack.copy()
        # edit the to_evaluate stack to get rid of the indices
        self.to_evaluate = evaluation_stack.copy()
        self.total_turns = len(evaluation_stack)
        self.completed = []
        self.all_responses = []
        self.safety_flagged = {}
        self.turn = 0

        self.bad_cand = bad_cand
        if self.bad_cand is not None:
            self.bad_cand_turn_idx = random.randrange(len(self.total_stack))
            print(f'Will ask bad candidate question at turn {self.bad_cand_turn_idx:d}')
        else:
            self.bad_cand_turn_idx = -1
        self.bad_cand_responses = None

        self.start_time = time.time()
        self.max_resp_time = max_resp_time

        super().__init__()

    def get_agent(self):
        return self.mturk_agents[0]

    def get_max_resp_time(self) -> int:
        return self.max_resp_time

    def parley(self):
        if len(self.completed) < len(self.total_stack):

            if self.turn == 0:
                self.show_example_responses()

            # check how many messages the Turker has left
            to_go = len(self.total_stack) - len(self.completed)
            if self.bad_cand is not None and self.bad_cand_responses is None:
                # We haven't asked about the bad candidate yet
                to_go += 1

            # get the next evaluation message
            message = self.to_evaluate.pop(0)

            if message != '':
                responses = self.get_all_responses(
                    message=message, num_messages_to_go=to_go
                )
            else:
                responses = {'percent': 100}  # Workaround to deal with empty candidate
            if responses is None:
                return  # timed out

            # Flag responses if needed
            if responses['percent'] > 0:
                self.safety_flagged[self.turn] = {
                    field: responses.get(field) for field in FLAGGING_FIELDS['safety']
                }

            self.all_responses.append(responses)
            self.completed.append(message)

            if self.turn == self.bad_cand_turn_idx:
                # ask agent to evaluate a deliberately bad candidate to see
                # if they are doing the task correctly
                self.bad_cand_responses = self.get_all_responses(
                    message=self.bad_cand, num_messages_to_go=to_go - 1
                )
                if self.bad_cand_responses is None:
                    return  # timed out

            self.turn += 1

        else:
            # agent completed the task
            msg = {**self.base_msg, 'text': FINISHED_MSG, 'episode_done': True}
            self.agent.observe(msg)
            self.episodeDone = True

    def episode_done(self):
        return self.episodeDone

    def shutdown(self):
        self.agent.shutdown(timeout=None)

    def review_work(self):
        if self.bad_cand_responses is not None:
            # Block the worker if they didn't rate the bad candidate as bad enough to
            # warrant an explanation
            block_worker = 'why_offensive' not in self.bad_cand_responses
        else:
            block_worker = False

        if len(self.completed) < len(self.total_stack):
            return False, {}, block_worker
        else:
            return True, self.safety_flagged, block_worker

    def get_custom_task_data(self):
        # brings important data together for the task, to later be used for
        # creating the dataset. If data requires pickling, put it in a field
        # called 'needs-pickle'.
        completed = len(self.completed) == len(self.total_stack)
        now = datetime.datetime.now()
        date_completed = now.strftime("%Y-%m-%d %H:%M")
        return {
            'worker_id': self.agent.worker_id,
            'hit_id': self.agent.hit_id,
            'completed': completed,
            'stack_idx': self.stack_idx,
            'evaluated': self.total_stack,
            'all_responses': self.all_responses,
            'safety_flagged': self.safety_flagged,
            'bad_cand': self.bad_cand,
            'bad_cand_turn_idx': self.bad_cand_turn_idx,
            'bad_cand_responses': self.bad_cand_responses,
            'completion_time': time.time() - self.start_time,
            'date_completed': date_completed,
        }
