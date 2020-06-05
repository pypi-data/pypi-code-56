from itertools import chain

import numpy as np
from numba import njit, jit


def fitness_function_song(chromosome):
    answer = np.array(
        [
            1,
            0,
            1,
            1,
            0,
            0,
            0,
            1,
            1,
            1,
            0,
            0,
            1,
            0,
            1,
            1,
            0,
            1,
            1,
            0,
            1,
            0,
            0,
            0,
            1,
            0,
            0,
            1,
            0,
            0,
            1,
            0,
            0,
            0,
            0,
            0,
            1,
            0,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            0,
            0,
            0,
        ]
    )

    return -np.abs(answer - chromosome).sum()


def fitness_function_sudoku(chromosome):

    puzzle = chromosome.reshape(9, 9)

    units = np.array(list(chain(*[np.vsplit(sub, 3) for sub in np.hsplit(puzzle, 3)])))

    points = 0

    target = np.arange(1, 10).astype(float)

    for m in range(9):
        points += -0.1 * ((puzzle[m, :]).sum() - 45) ** 2 + 100

        unique = np.unique(puzzle[m, :])

        points += (
            200 if len(unique) == len(target) and np.equal(unique, target).all() else 0
        )

    for n in range(9):
        points += -0.1 * ((puzzle[:, n]).sum() - 45) ** 2 + 100

        unique = np.unique(puzzle[:, n])

        points += (
            200 if len(unique) == len(target) and np.equal(unique, target).all() else 0
        )

    for unit in units:
        points += -0.1 * (unit.sum() - 45) ** 2 + 100

        unique = np.unique(unit.flatten())

        points += (
            200 if len(unique) == len(target) and np.equal(unique, target).all() else 0
        )

    return points


def fitness_function_quadratic(chromosome):

    # if chromosome[0] < -5 or chromosome[0] > 5 or chromosome[1] < -5 or chromosome[1] > 5:
    #     return -np.inf

    return -(chromosome[0] ** 2 + chromosome[1] ** 2)


def fitness_function_2(chromosome):

    if (
        chromosome[0] < 0
        or chromosome[0] > 10
        or chromosome[1] < 0
        or chromosome[1] > 10
    ):
        return 0

    return -(
        chromosome[0] * np.sin(4 * chromosome[0])
        + 1.1 * chromosome[1] * np.sin(2 * chromosome[1])
    )
