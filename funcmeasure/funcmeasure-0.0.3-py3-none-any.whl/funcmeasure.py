# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import List, Callable
import time

# Local
from .measurement import Measurement

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def measure(
    funcs: List[Callable],
    times: int = 1000,
    print_benchmark: bool = True
) -> List[Measurement]:
    measurements = []

    for func in funcs:
        total_duration = 0

        for _ in range(0, times):
            start = time.time()
            func()
            total_duration += time.time() - start

        measurements.append(
            Measurement(
                func.__name__,
                total_duration,
                times
            )
        )

    measurements = sorted(measurements, key=lambda k: k.avg_duration)

    if print_benchmark:
        __print(measurements, times)

    return measurements

def partial(func: Callable, *args, **kwargs):
    from functools import partial as _partial

    return _partial(func, *args, **kwargs)


# ----------------------------------------------------------- Private methods ------------------------------------------------------------ #

def __print(measurements: List[Measurement], times: int) -> None:
    fastest = measurements[0].avg_duration

    val_table_on_columns = [
        ['rank'],
        ['name'],
        ['duration'],
        ['benchmark']
    ]

    rank=0
    for measurement in measurements:
        rank+=1
        val_table_on_columns[0].append(str(rank))
        val_table_on_columns[1].append(measurement.func_name)

        val_table_on_columns[2].append("%.8f" % measurement.avg_duration + 's')

        multi = measurement.avg_duration / fastest
        multi_str = "%.2f" % multi + 'x'

        if multi == 1:
            multi_str = ''
        elif multi == int(multi):
            multi_str = "%.0f" % multi + 'x'
        
        val_table_on_columns[3].append(multi_str)
    
    longest_lens = []

    for column_vals in val_table_on_columns:
        longest_len = 0

        for val in column_vals:
            val_len =len(val)

            if val_len > longest_len:
                longest_len = val_len

        longest_lens.append(longest_len)

    val_table_on_rows = []
    for _ in range(0, len(val_table_on_columns[0])):
        val_table_on_rows.append([])

    for i in range(0, len(val_table_on_columns)):
        longest_len = longest_lens[i]
        column_vals = val_table_on_columns[i]

        for j in range(0, len(column_vals)):
            column_val = column_vals[j]

            val_table_on_rows[j].append(
                __fixed_len_str(
                    column_val,
                    longest_len,
                    filling_char = ' ',
                    center = j == 0
                )
            )

    header = __line(val_table_on_rows[0])
    divider = '-' * len(header)

    print('\nRan', times, 'times\n')
    print(divider)
    print(header)
    print(divider)

    for i in range(1, len(val_table_on_rows)):
        print(__line(val_table_on_rows[i]))

    print(divider)

def __line(elements: List[str], divider_char: str = '|') -> str:
    return divider_char + ' ' + (' ' + divider_char + ' ').join(elements) + ' ' + divider_char

def __fixed_len_str(
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


# ---------------------------------------------------------------------------------------------------------------------------------------- #