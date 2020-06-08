# This file is part of CoVeriTeam, a tool for on-demand composition of cooperative verification systems:
# https://gitlab.com/sosy-lab/software/coveriteam
#
# SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import filecmp
import os
import shutil
import uuid

VERDICT_TRUE = "TRUE"
VERDICT_FALSE = "FALSE"
VERDICT_UNKNOWN = "UNKNOWN"
VERDICT_ERROR = "ERROR"
VERDICT_TIMEOUT = "TIMEOUT"


class Artifact:
    def __init__(self, path: str):
        if path:
            self.path = os.path.abspath(path)
        else:
            self.path = ""

    def __str__(self):
        return self.path


class Joinable:
    def join(self, artifact2):
        """
        Definition of this function is to be provided by the child class.
        """
        pass


class BehaviorDescription(Artifact):
    pass


class Justification(Artifact):
    pass


class Verdict(Artifact):
    def __init__(self, verdict: str):
        self.verdict = verdict

    def __str__(self):
        return self.verdict

    def __eq__(self, other):
        return self.verdict == other


class Specification(Artifact):
    pass


class Program(BehaviorDescription):
    pass


class CProgram(Program):
    pass


class JavaProgram(Program):
    pass


class TestSpecification(Specification):
    pass


class BranchCoverage(TestSpecification):
    pass


class AutomatonSpecification(Specification):
    pass


class LTLSpecification(Specification):
    pass


class ReachSafety(LTLSpecification):
    pass


class Termination(LTLSpecification):
    pass


class MemSafety(LTLSpecification):
    pass


class NoOverflow(LTLSpecification):
    pass


class Witness(Justification):
    pass


class ReachabilityWitness(Witness):
    pass


class Condition(Justification):
    pass


class TestGoal(Condition, Joinable):
    def join(self, other):
        assert type(self) is type(
            other
        ), "Cannot join %r and %r. Types are not same." % (self, other)
        if not self.path:
            return TestGoal(other.path)
        elif other.path:
            # If files are same then no need to compare
            if filecmp.cmp(self.path, other.path, False):
                return self
            joined = os.path.join(os.path.dirname(self.path), str(uuid.uuid4()))
            with open(joined, "w") as f:
                with open(self.path) as f1:
                    f.write(f1.read())
                with open(other.path) as f1:
                    f.write(f1.read())
            return TestGoal(joined)
        # When other does not exist
        return self

    def __eq__(self, other):
        if isinstance(other, TestGoal):
            if self.path and other.path:
                return filecmp.cmp(self.path, other.path, False)
            elif not (self.path or other.path):
                return True
            else:
                return False
        else:
            return False


class TestSuite(Justification):
    def join(self, other):
        assert type(self) is type(
            other
        ), "Cannot join %r and %r. Types are not same." % (self, other)
        if not self.path:
            self.path = other.path
        elif other.path:
            # 1) Move all files from self to a child folder
            """files_to_move = os.listdir(self.path)
            child_path = os.path.join(self.path, "self")
            os.makedirs(child_path)
            for f in files_to_move:
                shutil.move(os.path.join(self.path, f), child_path)
            """
            # 2) copy the other folder to this path
            shutil.copytree(other.path, os.path.join(self.path, str(uuid.uuid4())))
        return self
