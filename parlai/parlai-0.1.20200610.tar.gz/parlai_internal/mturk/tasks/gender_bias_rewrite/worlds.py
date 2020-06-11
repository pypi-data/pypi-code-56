#!/usr/bin/env python3

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from parlai.mturk.core.worlds import MTurkOnboardWorld, MTurkTaskWorld
from parlai.mturk.core.agents import MTURK_DISCONNECT_MESSAGE, RETURN_MESSAGE
from parlai_internal.mturk.tasks.single_turn_safety_review.worlds import (
    SingleTurnSafetyOnboardingWorld,
    SingleTurnSafetyWorld,
)

import datetime
import random
import time

# Soft block qual name
QUAL_NAME = 'CompletedMaxReviewEvalsGender'

# Onboarding constants
# TODO: fix onboarding test
ONBOARDING_TEST = [
    (
        'Hey what is up, sir?',
        "<span style='color:red'><b>SPEAKING TO</b></span>",
        "<span style='color:green'><b>MAN</b></span>",
        ['certain', 'pretty sure'],
    ),
    (
        'I am going to go get a mani/pedi after my shopping trip!',
        "",
        "<span style='color:purple'><b>WOMAN</b></span>",
        ['pretty sure', 'unsure'],
    ),
    (
        'My mom is the best. She always makes me feel loved.',
        "<span style='color:orange'><b>SPEAKING ABOUT</b></span>",
        "<span style='color:purple'><b>WOMAN</b></span>",
        ['certain'],
    ),
]
INTRO_TEXT = "<b><i>ONBOARDING:</b></i> Please try to evaluate some sample messages. "
ONBOARDING_CONFIDENCE_MSG = (
    "For the following example message, how confident would someone be that the "
    + "speaker is {} a {}? :"
    + "<br><br><span style='color:blue'><b>{}</b></span>"
)
BLOCK_TEXT = (
    "Sorry, you did not complete the onboarding test correctly. "
    + "Please return the HIT."
)
COMPLETION_TEXT = "<b>Passed!</b> Now you will be sent to the task..."

# Task constants
AXES = [
    "<span style='color:red'><b>SPEAKING TO</b></span>",
    "",
    "<span style='color:orange'><b>SPEAKING ABOUT</b></span>",
]
GENDERS = [
    "<span style='color:green'><b>MAN</b></span>",
    "<span style='color:purple'><b>WOMAN</b></span>",
]
REWRITE_MSG = (
    "<i>({} messages left)</i> Please rewrite the following message "
    + "so that most people would guess that the speaker is {} a {}: "
    + "<br><br><span style='color:blue'><b>{}</b></span>"
)
CONFIDENCE_MSG = (
    "In the example you wrote, how confident would someone be that the "
    + "speaker is {} a {}?"
)
REASON_OPTIONS = ["UNSURE", "PRETTY SURE", "CERTAIN"]
FINISHED_MSG = "Thanks, you've completed the task! Click the button below to finish."


# Gender question
GENDER_Q = (
    "Before we begin, please select your gender. You may choose 'prefer not to say'. "
    + "<b>Please type 1, 2, 3, or 4. </b>"
    + "<br><br>1. WOMAN <br>2. MAN <br> 3. NONBINARY <br> 4. PREFER NOT TO SAY"
)
GENDER_OPTIONS = {
    '1': 'woman',
    '2': 'man',
    '3': 'nonbinary',
    '4': 'prefer not to say',
}


def is_disconnected(act):
    return 'text' in act and act['text'] in [MTURK_DISCONNECT_MESSAGE, RETURN_MESSAGE]


def check_timeout(act):
    if act is None or act['text'] in ['[TIMEOUT]', '[RETURNED]', '[DISCONNECT]']:
        return True
    return False


class GenderRewriteOnboarding(SingleTurnSafetyOnboardingWorld):
    """
    World for testing the ability of speakers to assess onboarding.
    TODO: fix this world!
    """

    def __init__(self, opt, mturk_agent, onboarding_tracker):
        super().__init__(opt, mturk_agent, onboarding_tracker)
        self.opt = opt
        self.onboarding_tracker = onboarding_tracker
        self.EVALUATE_MSG = ONBOARDING_CONFIDENCE_MSG

    def parley(self):
        self.msg = {'id': 'System', 'text': '', 'text_response': False}

        self.msg['text'] = INTRO_TEXT
        self.mturk_agent.observe(self.msg)

        i = len(ONBOARDING_TEST)
        for example in ONBOARDING_TEST:
            self.msg['text'] = self.EVALUATE_MSG.format(
                example[1], example[2], example[0]
            )
            i -= 1
            self.mturk_agent.observe(self.msg)
            answer = self.mturk_agent.act()
            # check for timeout
            timed_out = check_timeout(answer)
            if timed_out:
                self.episodeDone = True
                return

            if answer['text'].lower() not in example[-1]:
                print('Worker {} failed onboarding'.format(self.mturk_agent.worker_id))
                print('Answered {} to question: {}'.format(answer['text'], example[0]))
                if not self.opt.get('is_sandbox'):
                    self.onboarding_tracker.mark_worker_blocked(
                        self.mturk_agent.worker_id
                    )
                self.block_loop(qualification=QUAL_NAME)
                self.episodeDone = True
                return

        # successfully completed onboarding
        self.msg['text'] = COMPLETION_TEXT
        self.mturk_agent.observe(self.msg)
        time.sleep(3)
        self.episodeDone = True

    def block_loop(self, qualification=QUAL_NAME):
        # Let worker know that they've failed
        self.msg['text'] = BLOCK_TEXT
        self.mturk_agent.observe(self.msg)
        # Soft block the worker
        if not self.opt.get('is_sandbox'):
            print(
                'Soft blocking worker {} for failing onboarding.'.format(
                    self.mturk_agent.worker_id
                )
            )
            self.mturk_agent.mturk_manager.give_worker_qualification(
                self.mturk_agent.worker_id, qualification
            )
        act = self.mturk_agent.act()
        while not is_disconnected(act):
            self.mturk_agent.observe(self.msg)
            act = self.mturk_agent.act()
        return True


class GenderRewriteWorld(MTurkTaskWorld):
    """
    World in which which we ask MTurk workers to rewrite ...
    """

    def __init__(self, opt, mturk_agents, evaluation_stack):
        self.agent = mturk_agents[0]
        self.episodeDone = False
        self.total_stack = evaluation_stack.copy()
        # edit the to_evalute stack to get rid of the indices
        self.to_evaluate = [x[0] for x in evaluation_stack.copy()]
        self.total_turns = len(evaluation_stack)
        self.turker_gender = None
        self.genders = [random.choice(GENDERS) for _ in range(self.total_turns)]
        self.axes = [random.choice(AXES) for _ in range(self.total_turns)]
        self.completed = []
        self.answers = []
        self.confidences = {}
        self.num_bad_attempts = 0
        self.turn = 0

        self.msg = {'id': 'System', 'text': '', 'text_response': True}

        self.start_time = time.time()
        self.REWRITE_MSG = REWRITE_MSG
        self.CONFIDENCE_MSG = CONFIDENCE_MSG
        self.FINISHED_MSG = FINISHED_MSG

        self.get_reason_ans = ['ok']

    def format_eval_message(self, msg, text, num_left, gender, axis):
        punctuation_map = [
            (' !', '!'),
            (' .', '.'),
            (' ?', '?'),
            ('  (', ' ('),
            (' )', ')'),
            (' ,', ','),
            (" ' ", "'"),
        ]

        new_text = text.lower().replace('\n', '')
        for punc in punctuation_map:
            new_text = new_text.replace(punc[0], punc[1])

        msg['text'] = self.REWRITE_MSG.format(num_left, axis, gender, new_text)

        return new_text

    def get_confidence(self, rewrite, gender, axis):
        # get reason
        self.msg['text'] = self.CONFIDENCE_MSG.format(axis, gender)
        # let system know we need a text response next
        self.msg['text_response'] = False
        self.agent.observe(self.msg)
        answer = self.agent.act()
        timed_out = check_timeout(answer)
        if timed_out:
            self.episodeDone = True
            return False
        self.confidences[self.turn] = [rewrite, answer['text']]
        self.msg['text_response'] = True
        return True

    def check_completed(self, original, answer):
        original_words = original.split(' ')
        answer_words = answer.split(' ')
        word_overlap = [x for x in original_words if x in answer_words]

        if original == answer:
            self.agent.observe(
                {
                    'id': 'System',
                    'text': 'Please do not copy the original message! We will review answers. '
                    '<b>Please try again</b>',
                }
            )
            self.num_bad_attempts += 1
            return False
        if len(word_overlap) == 0:
            self.agent.observe(
                {
                    'id': 'System',
                    'text': 'Your message is too different from the original message. '
                    'We will be reviewing answers. <b>Please try again</b>',
                }
            )
            self.num_bad_attempts += 1
            return False
        if len(answer_words) <= 3 or len(answer_words) / len(original_words) <= 0.5:
            self.agent.observe(
                {
                    'id': 'System',
                    'text': 'Your message is too short. '
                    'We will be reviewing answers. <b>Please try again</b>',
                }
            )
            self.num_bad_attempts += 1
            return False

        return True

    def ask_gender_question(self):
        self.msg['text'] = GENDER_Q
        self.agent.observe(self.msg)
        answer = self.agent.act()
        # check for timeout
        timed_out = check_timeout(answer)
        if timed_out:
            self.episodeDone = True
            return False

        answer = answer['text'][0]
        self.turker_gender = GENDER_OPTIONS.get(answer)

        return True

    def parley(self):
        if self.turn == 0:
            if not self.ask_gender_question():
                return

        if len(self.completed) >= len(self.total_stack):
            # agent completed the task
            self.msg['text'] = self.FINISHED_MSG
            self.msg['episode_done'] = True
            self.agent.observe(self.msg)
            self.episodeDone = True
            return

        # check how many messages the Turker has left
        to_go = len(self.total_stack) - len(self.completed)
        # get the next evaluation message
        next_msg = self.to_evaluate.pop(0)
        gender = self.genders[self.turn]
        axis = self.axes[self.turn]

        completed_round = False
        while not completed_round:
            # observe evaluation message
            new_text = self.format_eval_message(self.msg, next_msg, to_go, gender, axis)
            self.agent.observe(self.msg)
            answer = self.agent.act()
            # check for timeout
            timed_out = check_timeout(answer)
            if timed_out:
                self.episodeDone = True
                return
            completed_round = self.check_completed(new_text, answer['text'])

        # save answers
        self.completed.append(next_msg)
        rewrite = answer['text']
        self.answers.append(rewrite)

        # TODO: need to check that rewrite is valid

        if not self.get_confidence(rewrite, gender, axis):
            # timed out
            return

        self.turn += 1

    def episode_done(self):
        return self.episodeDone

    def shutdown(self):
        self.agent.shutdown(timeout=None)

    def review_work(self):
        if len(self.completed) < len(self.total_stack):
            return False, None, None

        return True, self.total_stack, self.confidences

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
            'evaluated': self.total_stack,
            'answers': self.answers,
            'confidences': self.confidences,
            'genders': self.genders,
            'axes': self.axes,
            'completion_time': time.time() - self.start_time,
            'date_completed': date_completed,
            'num_bad_attempts': self.num_bad_attempts,
            'turker_gender': self.turker_gender,
        }
