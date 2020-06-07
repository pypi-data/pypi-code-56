from typing import List, Callable
import time

def measure(funcs: List[Callable], times: int = 1000):
    stats = []

    for func in funcs:
        total_duration = 0

        for _ in range(0, times):
            start = time.time()

            func()

            total_duration += time.time() - start

        stats.append({
            'name': func.__name__,
            'duration': total_duration/float(times)
        })
    
    stats = sorted(stats, key=lambda k: k['duration'])
    fastest = stats[0]['duration']

    longest_name_len = 4
    longest_dur_len = 0
    longest_perc_len = 0

    for stat in stats:
        name_len = len(stat['name'])
        if name_len > longest_name_len:
            longest_name_len = name_len

        perc_times = float(int(stat['duration'] * 100 / fastest) / 100)
        if perc_times == int(perc_times):
            perc = "%.0f" % perc_times + 'x'
        else:
            perc = "%.2f" % perc_times + 'x'
        stat['perc'] = perc

        perc_len = len(perc)
        if perc_len > longest_perc_len:
            longest_perc_len = perc_len

        stat['duration'] = "%.8f" % stat['duration']
        dur_len = len(stat['duration'])
        if dur_len > longest_dur_len:
            longest_dur_len = dur_len

    print('\nRan', times, 'times\n')
    header = '| rank | ' + __uniform_len_string('name', longest_name_len, center=True) + ' | ' + __uniform_len_string('duration', longest_dur_len, center=True) + ' | ' + __uniform_len_string('perc', longest_perc_len, center=True) + ' |'

    divider = ''
    for _ in range(0, len(header)):
        divider += '-'

    print(divider)
    print(header)
    print(divider)

    i = 0

    for stat in stats:
        i += 1

        print(
            '|',
            __uniform_len_string(str(i), 4), '|',
            __uniform_len_string(stat['name'], longest_name_len), '|',
            __uniform_len_string(str(stat['duration']), longest_dur_len), '|',
            __uniform_len_string(stat['perc'], longest_perc_len), '|'
        )

    print(divider)

def __uniform_len_string(
    string: str,
    preferred_length: int = 8,
    filling_char: str = ' ',
    center: bool = False
) -> str:
    last_side = 0

    while len(string) < preferred_length:
        if center:
            if last_side == 0:
                last_side = 1
                string = filling_char + string
            else:
                last_side = 0
                string += filling_char
        else:
            string = filling_char + string
    
    if len(string) > preferred_length:
        string = string[:preferred_length-1] + '.'
    
    return string