#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import glob
import os
import json
import numpy as np
from collections import defaultdict

from parlai.core.params import ParlaiParser

ParlaiParser()  # instantiate to set PARLAI_HOME environment var

"""Script for collecting data from gender rewrite logss"""

MAIN_DIR = '/private/home/edinan/ParlAI/parlai/mturk/run_data/live/'
TASKS = [
    'gender_bias_rewrite_1586958681',  # first trial, no onboarding
    'gender_bias_rewrite_1586965934',  # trial 2, no onboarding
    'gender_bias_rewrite_1586977227',  # trial 3, first example with onboarding
    'gender_bias_rewrite_1586981790',  # with onboarding, and gender annotation
    'gender_bias_rewrite_1587044951',  # with onboarding, and gender annotation (2)
    'gender_bias_rewrite_1587071402',  # with onboarding, and gender annoation (3)
]

NEW_DATAFILE = '/checkpoint/parlai/tasks/gender_multiclass/new_data2/data.jsonl'

BAD_ATTEMPT_THRESHOLD = 3
BAD_TURKERS = [
    'A2YMR9ZNYWFYU5',
    'A3K8WQICXRO3F8',
    'A11W0ZZNWZ6XBZ',
    'A25YZ7RE911DPQ',
    'A2K4U5E1LC9O3J',
    'A1ONTPD4RQHVYK',
    'A13RYEV98JL01L',
    'A3FFZN4FO3Q789',
    'A2JBNDG0U9IA6I',
    'A1PEDOFX00RHUM',
    'A2JQPSIVUCW92T',
    'A3NTQ56P7IZUZU',
    'AERTM9Y12LBNF',
    'AOWLCXNXCSQAC',
    'ANPNK6CIBGLIF',
    'A3VHNIFFP8Y9H',
    'ALQ7GPHT431Q2',
    'A3388HIWAKD3DV',
]


def check_ok(log):
    if not log['completed']:
        return False
    if log['worker_id'] in BAD_TURKERS:
        return False
    if log['num_bad_attempts'] > BAD_ATTEMPT_THRESHOLD:
        atmpts = log['num_bad_attempts']
        worker = log['worker_id']
        print(f'Found bad worker: {worker} ({atmpts} bad attempts)')
        return False

    return True


def get_axis_label(axis):
    if axis == 'AS':
        return 'SELF'
    if axis == 'TO':
        return 'PARTNER'
    return 'ABOUT'


def get_gender_label(gender):
    if gender == 'MAN':
        return 'male'
    if gender == 'WOMAN':
        return 'female'
    return 'unknown'


def analyze_data(data):
    examples = []
    idx = 0
    complete_time = []
    genders = []
    for log in data:
        for orig, confidence, gender, axis in zip(
            log['evaluated'], log['confidences'].values(), log['genders'], log['axes']
        ):
            print(f'{idx + 1}.')
            print(f'Original: {orig[0]}')
            worker = log['worker_id']
            axis = axis.split('<b>')[-1].split('</b>')[0].split('SPEAKING ')[-1]
            gender = gender.split('<b>')[-1].split('</b>')[0]
            if axis == '':
                axis = 'AS'
            print(f'Rewrite for: {axis}, {gender}')
            print(f'New: {confidence[0]}')
            print(f'Confidence: {confidence[1]}')
            print(f'Worker: {worker}')
            turker_gender = log.get('turker_gender')
            if turker_gender is not None:
                genders.append(turker_gender)
            print(f'Worker gender: {turker_gender}')
            print('=' * 50 + '\n')
            examples.append(
                {
                    'text': confidence[0],
                    'original': orig[0],
                    'labels': [f'{get_axis_label(axis)}:{get_gender_label(gender)}'],
                    'class_type': get_axis_label(axis).lower(),
                    'confidence': confidence[1],
                    'episode_done': True,
                    'turker_gender': turker_gender,
                }
            )

            idx += 1
        complete_time.append(log['completion_time'])

    avg_complete = sum(complete_time) / len(complete_time)
    mins = avg_complete / 60
    print(f'Average completion time: {mins} minutes.')
    pay = round((mins * 15) / 60, 2)
    print(f'Recommended pay: ${pay}')
    print(f'Gender counts:')
    gd_cnts = defaultdict(int)
    for gend in genders:
        gd_cnts[gend] += 1
    for k, v in gd_cnts.items():
        print(f'\t{k}: {v}')

    return examples


def load_data():
    data = []

    for task in TASKS:
        for fle in glob.glob(
            '{}/t_*/custom/data.json'.format(os.path.join(MAIN_DIR, task))
        ):
            with open(fle, 'rb') as f:
                log = json.load(f)
            if check_ok(log):
                data.append(log)

    return data


def write_to_file(examples):
    with open(NEW_DATAFILE, 'w') as f:
        for example in examples:
            j_ex = json.dumps(example)
            f.write(j_ex + '\n')

    print(f'\n\n[ New examples successfully written to {NEW_DATAFILE}... ]')


if __name__ == '__main__':
    data = load_data()
    examples = analyze_data(data)
    write_to_file(examples)
