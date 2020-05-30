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

import io
import sys
import csv
import argparse
import textwrap
import collections

import cchardet
import argcomplete
import numpy as np

from .assignment import assignments


def parseargs():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            """
            A tool to assign students to time slots.

            With allowed assignments provided in a csv (e.g. from a survey),
            provide a acceptable solution.
            """
        ),
        epilog=textwrap.dedent(
            """
            Workflow example:
              - Give a survey to your students providing a little bit more time
                slots than student number. Export the survey result in CSV.
              - To have a fist allocation, run the command:
                  %(prog)s survey.csv -o output.csv
                If you have not assigned students, contact all the students
                marked as problematic (not only the not assigned) to extend
                their choices. Once a allocation can be made go to next step.
              - If you have more time slots than student, you can try to choice
                the time slot you want to free.
                 1. First, export the timeslot list from the csv:
                     %(prog)s survey.csv -e timeslots.txt
                 2. Edit the timeslots file, adding a '#' in the begining of the
                    timeslots you want to free.
                 3. Run the command with the timeslots
                     %(prog)s -t timeslots.txt survey.csv -o output.csv
            """
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version="", help=argparse.SUPPRESS
    )

    parser.add_argument(
        "-e",
        "--export-timeslots",
        dest="export",
        type=argparse.FileType("wb"),
        metavar="TIMESLOT_FILE",
        help="""
            Export in TIMESLOT_FILE all timeslots from the input csv.
            """,
    )

    parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("wb"),
        metavar="OUTPUT_FILE",
        help="""
            Output CSV file where to write assignments. The encoding and CSV
            dialect is the same than the input.
            """,
    )

    parser.add_argument(
        "-t",
        "--timeslots",
        type=argparse.FileType("rb"),
        metavar="TIMESLOT_FILE",
        help="""
            Restrict allowed timeslots to timeslots provided in TIMESLOT_FILE.
            All line beginning with a '#' is ignored. See -e to generate a
            version of this file. If not provided, all timeslots are allowed.
            """,
    )

    parser.add_argument(
        "-g",
        "--groups",
        type=argparse.FileType("rb"),
        metavar="GROUPS_FILE",
        help="""
            Students are in groups, and the assignments must be done by groups.
            The GROUPS_FILE must be a CSV with a header and two columns, the
            first must be a column identifying the student and must have exactly
            the same name than one of the columns provided in the INPUT_FILE,
            and values must corresponds (order or rows doesn't matter), and the
            second column must be a group identifier (whatever its name). If
            more than one student answer for a group, the intersection is made
            to build allowed timeslots for the group.
            """,
    )

    parser.add_argument(
        "input",
        type=argparse.FileType("rb"),
        metavar="INPUT_FILE",
        help="""
            Input CSV file with headers. Encoding and CSV dialect are
            autodetected. This file must contain a header. The firsts
            columns contains a student identifier (e.g. the name or the name and
            the email address). Following columns are timeslots. the column name
            must identify the timeslot and therefore must be unique.
            """,
    )

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    return args


class InputDesc:
    def __init__(self, encoding, dialect, timeslots, student_id, students, bmat):
        self.encoding = encoding
        self.dialect = dialect
        self.timeslots = timeslots
        self.student_id = student_id
        self.students = students
        self.bmat = bmat

    def __repr__(self):
        return textwrap.dedent(
            f"""
            InputDesc(
                encoding={self.encoding!r}, 
                dialect={self.dialect!r},
                timeslots={self.timeslots!r},
                student_id={self.student_id!r},
                students={self.students!r},
                bmat={self.bmat!r},
            )"""
        )


def read_input(filedesc) -> InputDesc:
    bcontent = filedesc.read()
    filedesc.close()
    encoding = cchardet.detect(bcontent)["encoding"]
    content = bcontent.decode(encoding)
    dialect = csv.Sniffer().sniff(content)
    reader = csv.DictReader(io.StringIO(content), dialect=dialect)
    fieldnames = reader.fieldnames
    readed = list(reader)
    allbin = lambda cn: all((r[cn] in ("0", "1")) for r in readed[:-1])
    timeslots = tuple(cn for cn in fieldnames if allbin(cn))
    student_id = tuple(cn for cn in fieldnames if not allbin(cn))
    if not all((readed[-1][cn] in ("0", "1")) for cn in timeslots):
        # last row not valid
        readed.pop()
    bmat = np.array([[r[ts] for ts in timeslots] for r in readed], dtype=int)
    students = tuple({si: r[si] for si in student_id} for r in readed)
    return InputDesc(encoding, dialect, timeslots, student_id, students, bmat)


def make_timeslots_input(input_desc: InputDesc, timeslotfile):
    bcontent = timeslotfile.read()
    timeslotfile.close()
    encoding = cchardet.detect(bcontent)["encoding"]
    content = bcontent.decode(encoding)
    content.replace("\r", "")
    allowed_timeslots = set(x for x in content.split("\n") if not x.startswith("#"))
    newts = tuple(
        (i, ts) for i, ts in enumerate(input_desc.timeslots) if ts in allowed_timeslots
    )
    input_desc.timeslots = tuple(ts for i, ts in newts)
    input_desc.bmat = input_desc.bmat[:, [i for i, ts in newts]]


def make_groups_input(input_desc: InputDesc, groupsfile):
    bcontent = groupsfile.read()
    groupsfile.close()
    encoding = cchardet.detect(bcontent)["encoding"]
    content = bcontent.decode(encoding)
    dialect = csv.Sniffer().sniff(content)
    reader = csv.DictReader(io.StringIO(content), dialect=dialect)
    readed = list(reader)

    if len(reader.fieldnames) < 2:
        print("E: Groups file must contains 2 columns", file=sys.stderr)
        sys.exit(1)
    if len(reader.fieldnames) > 2:
        print(f"W: Groups file must contains 2 columns.", file=sys.stderr)
        print(
            f"W: This file contains {len(reader.fieldnames)}, columns after the second are ignored",
            file=sys.stderr,
        )

    student_id = reader.fieldnames[0]
    if not student_id in input_desc.student_id:
        print(
            f"E: The column {student_id!r} from the groups file must be a id of the student found in the input file",
            file=sys.stderr,
        )
        sys.exit(1)

    students = set(r[student_id] for r in readed)
    student_dict = {s[student_id]: i for i, s in enumerate(input_desc.students)}
    not_found_students = [
        s for s in input_desc.students if s[student_id] not in students
    ]
    if not_found_students:
        print(
            "E: The following students from input file are not found in group file:",
            file=sys.stderr,
        )
        for s in not_found_students:
            print(f"E:  - {s}", file=sys.stderr)
            sys.exit(1)

    groupcolname = reader.fieldnames[1]
    groups = collections.defaultdict(lambda: [])
    for r in readed:
        if r[student_id] in student_dict:
            groups[r[groupcolname]].append(r[student_id])

    for g, gstud in groups.items():
        if not gstud:
            print("W: No reply for group {g!r}", file=sys.stderr)

    groups_list = tuple(groups.keys())
    groups_bmat = np.array(
        [
            input_desc.bmat[[student_dict[sid] for sid in groups[g]], :].prod(axis=0)
            if groups[g]
            else np.ones(input_desc.bmat.shape[1], dtype=int)
            for g in groups_list
        ],
        dtype=int,
    )

    input_desc.bmat = groups_bmat
    input_desc.students = tuple({groupcolname: g} for g in groups)
    input_desc.student_id = (groupcolname,)


def main():
    args = parseargs()
    if args.export is not None and (
        args.output is not None or args.groups is not None or args.timeslots is not None
    ):
        print(
            "When --export-timeslots is used, the following options are forbidden: --output, --groups, --timeslots.",
            file=sys.stderr,
        )
        sys.exit(1)

    input_desc = read_input(args.input)

    if args.export is not None:
        export_file = io.TextIOWrapper(args.export, encoding=input_desc.encoding)
        for timeslot in input_desc.timeslots:
            print(timeslot, file=export_file)
        export_file.close()
        args.export.close()
        sys.exit(0)

    if args.timeslots is not None:
        make_timeslots_input(input_desc, args.timeslots)

    if args.groups is not None:
        make_groups_input(input_desc, args.groups)

    res = assignments(input_desc.bmat)
    if res.not_assigned_rows:
        print("W: The following students are not assigned:", file=sys.stderr)
        for i in res.not_assigned_rows:
            print(f"W:   - {input_desc.students[i]}", file=sys.stderr)
        print(
            "W: The problem can be solved by examinating the following students:",
            file=sys.stderr,
        )
        for i, _ in res.pb_rows:
            print(f"W:   - {input_desc.students[i]}", file=sys.stderr)

    if args.output is not None:
        writer = csv.DictWriter(
            io.TextIOWrapper(args.output, encoding=input_desc.encoding),
            ["Timeslot"] + list(input_desc.student_id),
        )
        writer.writeheader()
        for i, j in sorted(res.best_assignments, key=lambda x: x[1]):
            row = {"Timeslot": input_desc.timeslots[j]}
            row.update(input_desc.students[i])
            writer.writerow(row)
    else:
        print(
            "W: No output provided. See -o/--output to write the output to a file",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
