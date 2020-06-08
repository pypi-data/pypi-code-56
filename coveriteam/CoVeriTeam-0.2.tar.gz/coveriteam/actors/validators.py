# This file is part of CoVeriTeam, a tool for on-demand composition of cooperative verification systems:
# https://gitlab.com/sosy-lab/software/coveriteam
#
# SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

from coveriteam.language.artifact import (
    CProgram,
    ReachabilityWitness,
    Verdict,
    Witness,
    Specification,
)
from coveriteam.language.actor import Validator
from coveriteam.language.atomicactor import AtomicActor
from benchexec.result import get_result_classification
import os
import glob
import logging


class ProgramValidator(Validator, AtomicActor):
    _input_artifacts = {
        "program": CProgram,
        "spec": Specification,
        "witness": Witness,
        "verdict": Verdict,
    }
    _output_artifacts = {"verdict": Verdict, "witness": Witness}
    _result_files_patterns = ["**/*.graphml"]

    def _act(self, program, spec, witness, verdict):
        # TODO I know the verdict is not used, but it is still there for the type.
        options = ["-witness", witness.path]
        self._run_tool(program.path, spec.path, options)
        return super()._act()

    def _extract_result(self):
        # read output
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

        # extract result
        glob_pattern = self.logDirSelf() + "/**/*" + ".graphml"
        for file in glob.glob(glob_pattern, recursive=True):
            witness = ReachabilityWitness(os.path.abspath(file))

        return {"verdict": verdict, "witness": witness}
