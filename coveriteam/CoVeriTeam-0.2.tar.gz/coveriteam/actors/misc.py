# This file is part of CoVeriTeam, a tool for on-demand composition of cooperative verification systems:
# https://gitlab.com/sosy-lab/software/coveriteam
#
# SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

from benchexec.result import get_result_classification
from coveriteam.language.artifact import (
    CProgram,
    Condition,
    Witness,
    Specification,
    TestGoal,
    TestSpecification,
    TestSuite,
    Verdict,
)
from coveriteam.language.actor import Instrumentor, Reducer, Transformer
from coveriteam.language.atomicactor import AtomicActor
import os
import glob
import logging


class WitnessInstrumentor(Instrumentor, AtomicActor):
    actorName = "witness-instrumentor"
    _input_artifacts = {"program": CProgram, "witness": Witness}
    _output_artifacts = {"program": CProgram}
    _result_files_patterns = ["**/*.c"]

    def _act(self, program, witness):
        # Witness is passes as specification in this case. This is from CPAchecker, can't do much
        self._run_tool(program.path, witness.path)
        return super()._act()

    def _extract_result(self):
        # extract result
        glob_pattern = self.logDirSelf() + "/**/*" + ".c"
        for file in glob.glob(glob_pattern, recursive=True):
            instrumentedProgram = CProgram(os.path.abspath(file))

        return {"program": instrumentedProgram}


class WitnessToTest(AtomicActor):
    actorName = "witness-to-test"
    _input_artifacts = {"program": CProgram, "spec": Specification, "witness": Witness}
    _output_artifacts = {"test_suite": TestSuite}
    _result_files_patterns = ["**/*.xml"]

    def _act(self, program, spec, witness):
        options = ["-witness", witness.path]
        self._run_tool(program.path, spec.path, options)
        return super()._act()

    def _extract_result(self):
        # We assume that the test generator will succeed and create a directory
        # containing metadata.xml. This directory is the test suite.
        glob_pattern = self.logDirSelf() + "/**/metadata.xml"
        for file in glob.glob(glob_pattern, recursive=True):
            testSuite = TestSuite(os.path.dirname(os.path.abspath(file)))

        return {"test_suite": testSuite}


class TestCriterionInstrumentor(Instrumentor, AtomicActor):
    actorName = "test-criterion-instrumentor"
    _input_artifacts = {"program": CProgram, "test_spec": TestSpecification}
    _output_artifacts = {"program": CProgram}
    _result_files_patterns = ["**/*.c"]

    def _act(self, program, test_spec):
        # hard coded output path
        options = ["--output", "instrumented.c"]
        self._run_tool(program.path, test_spec.path, options)
        return super()._act()

    def _extract_result(self):
        # extract result
        glob_pattern = self.logDirSelf() + "/**/*" + ".c"
        for file in glob.glob(glob_pattern, recursive=True):
            instrumentedProgram = CProgram(os.path.abspath(file))

        return {"program": instrumentedProgram}


class TestGoalPruner(Reducer, AtomicActor):
    actorName = "test-goal-pruner"
    _input_artifacts = {
        "program": CProgram,
        "test_spec": TestSpecification,
        "covered_goals": TestGoal,
    }
    _output_artifacts = {"program": CProgram}
    _result_files_patterns = ["**/*.c"]

    def _act(self, program, test_spec, covered_goals):
        # hard coded output path
        options = ["--output", "reduced.c"]
        if covered_goals.path:
            options += ["--covered-labels", covered_goals.path]

        self._run_tool(program.path, test_spec.path, options)
        return super()._act()

    def _extract_result(self):
        # extract result
        glob_pattern = self.logDirSelf() + "/**/" + "reduced.c"
        for file in glob.glob(glob_pattern, recursive=True):
            prunedProgram = CProgram(os.path.abspath(file))

        return {"program": prunedProgram}


class TestGoalAnnotator(Reducer, AtomicActor):
    actorName = "test-goal-annotator"
    _input_artifacts = {
        "program": CProgram,
        "test_spec": TestSpecification,
        "covered_goals": TestGoal,
    }
    _output_artifacts = {"program": CProgram}
    _result_files_patterns = ["**/*.c"]

    def _act(self, program, test_spec, covered_goals):
        # hard coded output path
        options = ["--output", "reduced.c"]
        if covered_goals.path:
            options += ["--covered-labels", covered_goals.path]

        self._run_tool(program.path, test_spec.path, options)
        return super()._act()

    def _extract_result(self):
        # extract result
        glob_pattern = self.logDirSelf() + "/**/" + "reduced.c"
        for file in glob.glob(glob_pattern, recursive=True):
            annotatedProgram = CProgram(os.path.abspath(file))

        return {"program": annotatedProgram}


class TestGoalExtractor(Transformer, AtomicActor):
    actorName = "test-goal-extractor"
    _input_artifacts = {
        "program": CProgram,
        "test_spec": TestSpecification,
        "test_suite": TestSuite,
    }
    _output_artifacts = {"extracted_goals": TestGoal}
    _result_files_patterns = ["**/*.txt"]

    def _act(self, program, test_spec, test_suite):
        # hard coded output path
        options_output = ["-o", "covered_goals.txt"]
        # Passing the directory of the test suite
        options_remaining_goals = ["--test-suite", test_suite.path]
        options = options_remaining_goals + options_output
        self._run_tool(program.path, test_spec.path, options)
        return super()._act()

    def _extract_result(self):
        # extract result
        glob_pattern = self.logDirSelf() + "/**/" + "covered_goals.txt"
        for file in glob.glob(glob_pattern, recursive=True):
            extracted_goals = TestGoal(os.path.abspath(file))

        return {"extracted_goals": extracted_goals}


class CMCReducer(Transformer, AtomicActor):
    actorName = "cmc-reducer"
    _input_artifacts = {"program": CProgram, "condition": Condition}
    _output_artifacts = {"program": CProgram}
    _result_files_patterns = ["**/*.c"]

    def _act(self, program, condition):
        # hard coded output path
        options_assm_file = [
            "-setprop",
            "residualprogram.assumptionFile=" + condition.path,
        ]
        options_assm_automaton = [
            "-setprop",
            "AssumptionAutomaton.cpa.automaton.inputFile=" + condition.path,
        ]
        options = options_assm_automaton + options_assm_file
        self._run_tool(program.path, "", options)
        return super()._act()

    def _extract_result(self):
        # extract result
        glob_pattern = self.logDirSelf() + "/**/*" + ".c"
        for file in glob.glob(glob_pattern, recursive=True):
            reducedProgram = CProgram(os.path.abspath(file))

        return {"program": reducedProgram}


class TestValidator(Transformer, AtomicActor):
    actorName = "test-validator"
    _input_artifacts = {
        "program": CProgram,
        "test_suite": TestSuite,
        "test_spec": TestSpecification,
    }
    _output_artifacts = {"verdict": Verdict}
    _result_files_patterns = ["**/*.c"]

    def _act(self, program, test_suite, test_spec):
        options_spec = ["--goal", test_spec.path]
        testzip = os.path.join(os.path.dirname(test_suite.path), "test_suite.zip")
        os.system("zip -qr " + testzip + " " + test_suite.path)
        options_test_suite = ["--test-suite", testzip]
        options = options_test_suite + options_spec
        self._run_tool(program.path, "", options)
        return super()._act()

    def _extract_result(self):
        try:
            with open(self.logFile(), "rt", errors="ignore") as outputFile:
                output = outputFile.readlines()
                # first 6 lines are for logging, rest is output of subprocess, see runexecutor.py for details
                output = output[6:]
        except IOError as e:
            logging.warning("Cannot read log file: %s", e.strerror)
            output = []

        verdict = Verdict(
            get_result_classification(self._tool.determine_result(0, 0, output, False))
        )
        return {"verdict": verdict}
