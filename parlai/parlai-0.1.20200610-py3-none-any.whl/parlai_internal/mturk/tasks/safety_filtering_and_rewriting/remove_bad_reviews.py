#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
"""
Script for collecting data from MTurk task logs.
"""

import argparse
import json
import os

from parlai_internal.mturk.tasks.safety_filtering_and_rewriting.worlds import (
    SAVE_FOLDER,
)


def remove_bad_reviews(version: int):

    # Params
    failing_onboarding = [
        'A30BD7UZA2GLQ2',
        'A1V3QE3IDOUM8A',
        'A3UVY9KA7GD5SP',
        'A3LQCV132YFHSD',
        'A1SRQ63M2VV6QP',
        'A1E8XWQA2ORZQQ',
        'A3NQK6VK36A4GA',
        'A2WVPE3AI07JTZ',
        'A16W9JV70ER852',
        'AF114PN3TN6C3',
        'A268ITHAZWNWZO',
        'A3D4UDWEJLFV2N',
        'A3CIB3BTA5T89N',
        'A1A9C6R0VWJAOU',
        'AVTKJYDC3MLSP',
        'AGHKGWDYPVDFE',
        'AO3K51Z39MYN9',
        'AYW62R027PUT1',
        'A1K64SRWJOJ6XB',
        'AZKZCA3XGV3FI',
        'A3UI9ARHP4BGZY',
        'A3UUHATPTZC700',
        'A2UUTOBBGTCMBE',
        'A3FVZYN24BCKT7',
        'A3W1UOYHYHINRA',
        'A25F8VUZP0O1Z6',
        'A2YNHC0B210HLK',
        'A2WN9Y7JPLXGJX',
        'AO2M8J1H30OZF',
        'A2FE0I7W269C1C',
        'A3IQNEOSH76E7X',
        'A2QPUGA4X04GMN',
        'A15C8YU629AIDE',
        'A31TTT2YULSPYQ',
        'ADM5OBMT4U6UK',
        'AOHQV4DW7JDR',
        'ARHW2C7XN6OCB',
        'AUH6CZ7JFKJM5',
        'A3VCDIOJ83SN7W',
        'A3JKT80ST6DQQD',
        'A1QQNQN745J3M9',
        'A19SPL1DDGX2KR',
        'A1KZ6MGN2IXT4N',
        'A1ODKX8APG7Q9J',
        'A3UYSHALAOJNTV',
        'A386T7BS87Q4Z3',
        'A2221JS78I9P2D',
        'A35AEGPE73CX8Q',
        'A3LW9WQOQQMA5V',
        'AX33V6TCLMAN8',
        'A1B7K7VA82MNKS',
        'A17NBPHLOP42EX',
        'AHYQC0I8W1IMY',
        'A1QYJD438400C5',
        'A160B5Z54CQ478',
        'A167FXL9W18A5',
        'ALG1RZEAZ4WPA',
        'A14K0FSQTR3D02',
        'AERC8E4ACMY3M',
        'AIY2BEOY1NEUU',
        'AXXYX6K93E1YE',
        'A3NE2H8VEPQWFG',
        'A136DZVKWPP39T',
        'ATZ4IKTQPRANS',
        'A35AF4J6NPR2T9',
        'A34Q3GKF6OD5KE',
        'A3IJRZXXZ1LAFP',
        'A20JF8A76ASX4T',
        'A3U0Z1MOGCPTZF',
        'A1VV8QCMXO470U',
        'AIOFX0RWB5U4I',
        'A2P20NN1DBRZUF',
        'A2LJU9I5WC9E54',
        'AHOWLYVQTV8CV',
        'A11N3AK1XTJV8',
        'A2IQ2NZ03PPF7P',
        'A84CRWQJ4L7VX',
        'A1E126PWFILB2I',
        'A1B4BMWCE4GFGW',
        'A1YSCYUXLSIH6L',
        'A38RX2O4GNOI8D',
        'A3S0IC3M8RZ54U',
        'A3PD4XSXQT67L3',
        'A1D57LUCF072FJ',
        'A1P37ODJ8MY8UK',
        'AN5LX957VP73X',
        'A1VYD4NVU04BS6',
        'A1Q80Y8GQCLM8X',
        'AC8K71PXQTLAG',
        'A25ETLFUFH3MO4',
        'AFSRJQX7ZN6OW',
        'A3FQ0Y56LJ8SXB',
        'A3HQATY1RYKLXF',
        'AHQ6043GP6LDE',
        'ARK2ZTEWQWN0Q',
        'A2E3JEYPGQ7OU4',
        'A3DAMO1OF24IS9',
        'A29CBBQN5WJV90',
        'A382QGY4DZKZB3',
        'A3PFQO498Q6O72',
        'A3DHDQTBZSPFQE',
        'AB5HO1K9GIFPG',
        'A2YEE7PBKLC3B0',
        'A10A44IMGJ49QH',
        'A1R6J2VHRK5YR6',
        'A29S0R4TWY45SY',
        'A2J1T2WW04YAWU',
        'AWV52VOWIDUH8',
        'AGUZUE5WOD7JK',
        'A3ZWMVK6GNTJ8',
        'A2623C5UOABWD7',
        'A1Y7TYVUO3Q8U4',
        'A17R94QZ22Q84L',
        'A1H4RXFUNZGXIT',
        'A1WJTI3DL5HUKY',
        'A1T6HER891K5B7',
        'A7TZ8UVBP54VZ',
        'A23WEAVGAOC5XZ',
        'A3LXDJMMQLD9UH',
        'A3LIDIQTG8JQH1',
        'A29ES4DGUSA74I',
        'A3J3L6SL4RWBIY',
        'A2QTJ6795QIDWT',
        'A35QIBTLYD377C',
        'A1BQ07RDJRSIKU',
        'AJF954955YWZG',
        'A2F5NCG5YURL0U',
        'AD1B89HWQMYVX',
        'A2ZMMF5XRUWKIK',
        'A2B4KDGE9BVMQU',
        'A2074VMS950Q3V',
        'A1QCT0FXT7CT2S',
        'A3B78WUGC7TK32',
        'AY999MGRE1NTA',
        'A2Q45U44DLMPI4',
        'AFUQNGH2MB6P7',
        'A2P6WQTAHM55I0',
        'A3EHNYYKEVYSK6',
        'A1667AC975LPB3',
        'AS5BWWAMX2SU9',
        'A15TLO9BJIQ4M',
        'A10BVG4R9L08HP',
        'A2IV53DEXG0VM3',
        'A36KDWI1CGJFFA',
        'A2Q3BNM5VDYLYG',
        'A3K52OBIGIW3R5',
        'A3HU9JOPC9UK8Q',
        'A33FND7SQME47Z',
        'AYY7JSAD0SGXL',
        'A1OQTE6O4Z7LXZ',
        'A3GITKS8VABUNB',
        'A2WECSQH6MU7CO',
        'A2DG13OLO4FMOE',
        'A15D5D7GFW3MD4',
        'A601YFNTDO6R8',
        'A2LSWW37VV5RYH',
        'A1KRVZGJ2QVNON',
        'A37G73AUJO06ER',
        'A2MC9YIZ4ZCUP0',
        'A2POF6HIPSMTF8',
        'A3NG777FV354SM',
        'A1O0K64JAO2OHT',
        'AY4UCK4TQQ38Q',
        'A2N77KHHAYOC14',
        'A3VI2FYRBVWB0Z',
        'A15DR047PGCOBQ',
        'A1UQKXXKMB21C7',
        'AZ8WW23R33U6I',
        'A2KGTB3F9LL7SS',
        'A1JVY246YM0SD4',
        'A1F7HBLXK8JOY8',
        'A3TACWNU7D8EWT',
        'A3KMLB6WBWXCU0',
        'AYDHJW4ZG0D38',
        'A1END64LXSJL51',
        'A3PGYM90AJ92IT',
        'A1EB7U0FL6Y09Q',
        'A2YH9KGAZELMCL',
        'ANHASU9UI7AUR',
        'A3BZTAAC9XZ381',
        'A2CLSASUR08Z0O',
        'A13SW4U7ZZ9X6O',
        'A39GBZ4ZWUV8Q6',
        'A319R80Z9QYG3R',
        'A1TSV4YO3EL36M',
        'A116LG52AS82Q1',
        'A2XO5D6Z76VZ8G',
        'A1SI4UV8KC3YJ',
        'A2LXWB6NASGE6F',
        'AN17H6W2N3EZV',
        'A3VVR5EIALOQUD',
        'A3UA074KB35ORV',
    ]
    # These Turkers failed onboarding but contributed to one or more HITs
    fraudulent_responses = ['A2YEE7PBKLC3B0']
    # This Turker clearly gave fraudulent reasons for flagging a bunch of messages
    workers_to_remove = failing_onboarding + fraudulent_responses

    # Paths
    archived_stack_path = os.path.join(
        SAVE_FOLDER, f'completed_stack_v{version:d}.before_removing_bad_reviews.json'
    )
    stack_path = os.path.join(SAVE_FOLDER, f'completed_stack_v{version:d}.json')

    # If the archived stack path doesn't exist, create it by copying the main stack to
    # it
    if not os.path.isfile(archived_stack_path):
        os.rename(stack_path, archived_stack_path)

    # Load in stack
    with open(archived_stack_path, 'r') as f:
        original_stack = json.load(f)

    # Check in the original stacks how many stacks have fewer than 2 workers
    num_fewer_than_2_workers = len(
        [stats for stats in original_stack.values() if len(stats['workers']) < 2]
    )
    if len(num_fewer_than_2_workers) > 0:
        print(
            f'WARNING: {num_fewer_than_2_workers:d} stacks have fewer than 2 ratings '
            f'in the original stack!'
        )

    # Check for stacks that the same worker reviewed more than once
    num_duplicated_reviews = 0
    for stack_key, stack_stats in original_stack.items():
        workers = stack_stats['workers']
        if len(workers) != len(set(workers)):
            num_duplicated_reviews += 1
    if num_duplicated_reviews > 0:
        raise NotImplementedError(
            'Filter out stacks that the same reviewer reviewed multiple times!'
        )

    # Remove all stacks from bad workers out of the stack
    filtered_stack = {}
    workers_to_stack_counts = {worker: 0 for worker in workers_to_remove}
    for stack_key, stack_stats in original_stack.items():
        filtered_stack_stats = {}
        for stat_key, stat in stack_stats.items():
            if stat_key == 'workers':
                new_worker_list = []
                for worker in stat:
                    if worker in workers_to_remove:
                        workers_to_stack_counts[worker] += 1
                    else:
                        new_worker_list.append(worker)
                filtered_stack_stats['workers'] = new_worker_list
            else:
                filtered_stack_stats[stat_key] = stat
        filtered_stack[stack_key] = filtered_stack_stats
    assert all([stack_count > 0 for stack_count in workers_to_stack_counts.values()])

    # Report how any worker-stack combos were filtered out
    num_original_worker_entries = sum(
        [len(stats['workers']) for stats in original_stack.values()]
    )
    num_filtered_worker_entries = sum(
        [len(stats['workers']) for stats in filtered_stack.values()]
    )
    num_filtered_out = num_original_worker_entries - num_filtered_worker_entries
    print(
        f'There were {num_original_worker_entries:d} worker entries in the stack '
        f'originally and there are {num_filtered_worker_entries:d} after filtering, so '
        f'{num_filtered_out:d} were filtered out.'
    )

    # Check now how many stacks have fewer than 2 workers
    num_fewer_than_2_workers = len(
        [stats for stats in filtered_stack.values() if len(stats['workers']) < 2]
    )
    if len(num_fewer_than_2_workers) > 0:
        print(
            f'WARNING: {num_fewer_than_2_workers:d} stacks have fewer than 2 ratings '
            f'in the filtered stack!'
        )

    # Save new stack
    with open(stack_path, 'w') as f:
        json.dump(filtered_stack, f)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--version-num', type=int, help='increase this to create a new stack'
    )
    args = parser.parse_args()

    remove_bad_reviews(version=args.version_num)
