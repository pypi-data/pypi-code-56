# Copyright 2020, Jean-Benoist Leger <jb@leger.tf>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import random
import itertools
import collections

import numpy as np


def _multiple_argmin(g, *, key=None):
    it = iter(g)
    if key is None:
        key = lambda x: x
    try:
        first = next(it)
    except StopIteration:
        return []
    vmin = key(first)
    amin = [first]
    while True:
        try:
            cur = next(it)
        except StopIteration:
            return amin
        val = key(cur)
        if val < vmin:
            vmin = val
            amin.clear()
            amin.append(cur)
        elif val == vmin:
            amin.append(cur)


def _assigments_one_try(bmat, order):
    assigned_students = set()
    bmat = np.array(bmat, dtype=int)
    assignments = []
    while bmat.sum() > 0:
        Dr, Dc = bmat.sum(axis=1), bmat.sum(axis=0)
        while True:
            combis = [
                c
                for c, _ in _multiple_argmin(
                    (
                        (c, sum(Dr[i].sum() + Dc[j] for i, j in c))
                        for c in itertools.combinations(
                            ((i, j) for i, j in np.argwhere(bmat)), order
                        )
                        if (
                            len(set(i for i, j in c)) == order
                            and len(set(j for i, j in c)) == order
                        )
                    ),
                    key=lambda x: x[1],
                )
            ]
            if combis:
                break
            if order == 1:
                break
            order -= 1
        if not combis:
            break
        i, j = random.choice(random.choice(combis))
        assigned_students.add(i)
        assignments.append((i, j))
        bmat[i, :] = 0
        bmat[:, j] = 0
    not_assigned_students = tuple(
        i for i in range(bmat.shape[0]) if i not in assigned_students
    )
    return (tuple(assignments), not_assigned_students)


AssignmentsResult = collections.namedtuple(
    "AssignmentsResult", ("best_assignments", "not_assigned_rows", "pb_rows")
)


def assignments(bmat, order=1, ntry=10):
    """Make assignments between rows and columns.

    The objective is to have assigments following the following conditions:
     - all association are allowed in bmat,
     - each row is associated with a unique column,
     - each column is associated with a unique row,
     - all rows are associated.

    A classical use case is to assign students to defense schedule.

    Parameters
    ----------
    bmat : array of bool or int
        Binary matrix indicating which assignments are allowed.
    order : int, optional
        Order of the greedy search. Default: 1. A higher oreder can be used for
        small dataset if a solution can not be found with oreder 1.
    ntry : int
        Number of random tries to use to solve the assignments problem.

    Returns
    -------
    AssignmentResult
        Attributes are:
          - ``best_assignments`` contains the assigments that solve the problem
            or aith the higher number of associated rows.
          - ``not_assigned_rows`` contains the indexes of not assignated rows in
            the ``best_assignments`` (empty if the problem is solved)
          - ``problematic_rows`` contains tuples of problematics rows indexes
            and scores. A higher score indicating a row is problematic for the
            assignement problem.
    """
    min_not_assigned_rows = np.inf
    best_assignments = ()
    best_not_assigned_rows = ()
    not_assigned_rows = []
    for _ in range(ntry):
        cur_assignments, cur_not_assigned_rows = _assigments_one_try(bmat, order)
        if not cur_not_assigned_rows:
            return AssignmentsResult(cur_assignments, (), ())
        if len(cur_not_assigned_rows) < min_not_assigned_rows:
            min_not_assigned_rows = len(cur_not_assigned_rows)
            best_assignments = cur_assignments
            best_not_assigned_rows = cur_not_assigned_rows
        not_assigned_rows.extend(cur_not_assigned_rows)
    pb_rows = [
        (i, sum(j == i for j in not_assigned_rows) / ntry)
        for i in set(not_assigned_rows)
    ]
    pb_rows.sort(key=lambda x: x[1], reverse=True)
    return AssignmentsResult(best_assignments, best_not_assigned_rows, tuple(pb_rows))
