# This file is part of CoVeriTeam, a tool for on-demand composition of cooperative verification systems:
# https://gitlab.com/sosy-lab/software/coveriteam
#
# SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

from benchexec.model import cmdline_for_run, load_tool_info
from benchexec.runexecutor import RunExecutor
from benchexec.test_benchmark_definition import DummyConfig
from coveriteam.language.actor import Actor
from coveriteam.util import (
    TOOL_OUTPUT_FILE,
    str_dict,
    get_actor_config,
    install_if_needed,
)
import os
import uuid
from xml.etree import ElementTree
import coveriteam.util as util
from coveriteam.language import CoVeriLangException


class AtomicActor(Actor):
    def __init__(self, path):
        config = get_actor_config(path)
        self.actorName = config["actor_name"]
        self._tool_name = config["toolinfo_module"]
        self._archive_location = config["archive"]["location"]
        self._options = config["options"]
        self._reslim = config["resourcelimits"]
        self._tool_dir = install_if_needed(self._archive_location, self._tool_name)

    def name(self):
        return self.actorName

    def logDirSelf(self):
        return util.LOG_DIR + self.actorName + "/" + self._execution_id + "/"

    def logFile(self):
        return self.logDirSelf() + TOOL_OUTPUT_FILE

    def print_version(self):
        cwd = os.getcwd()
        os.chdir(self._tool_dir)

        tool_name = self._tool_name or self.actorName
        tool_info, self._tool = load_tool_info(tool_name, DummyConfig)
        version = self._tool.version(self._tool.executable())
        print(self._tool.name() + " " + version)
        os.chdir(cwd)

    def act(self, **kwargs):
        # 1. generate and set uuid
        self._execution_id = str(uuid.uuid4())
        res = super().act(**kwargs)
        self.gen_xml_elem(kwargs, res)

        return res

    def _act(self):
        try:
            return self._extract_result()
        except UnboundLocalError:
            msg = "The execution of the actor {} did not produce the expected result".format(
                self.name()
            )
            msg += "More information can be found in the logfile produced by the tool: {}".format(
                self.logFile()
            )
            raise CoVeriLangException(msg)

    def _run_tool(self, program_path, property_path, additional_options=[]):
        # Change directory to tool's directory
        cwd = os.getcwd()
        os.chdir(self._tool_dir)

        tool_name = self._tool_name or self.actorName
        tool_info, self._tool = load_tool_info(tool_name, DummyConfig)
        lims_for_exec = {
            "softtimelimit": self._reslim["timelimit"],
            "memlimit": self._reslim["memlimit"],
        }
        cmd = cmdline_for_run(
            self._tool,
            self._tool.executable(),
            self._options + additional_options,
            [program_path],
            property_path,
            lims_for_exec,
        )
        self.measurements = RunExecutor().execute_run(
            cmd,
            self.logFile(),
            output_dir=self.logDirSelf(),
            result_files_patterns=self._result_files_patterns,
            **lims_for_exec
        )
        # Change back to the original directory
        os.chdir(cwd)

    def gen_xml_elem(self, inputs, outputs):
        super().gen_xml_elem(inputs, outputs)
        data = self.get_measurements_data_for_xml()
        self.xml_elem.append(ElementTree.Element("measurements", str_dict(data)))

    def get_measurements_data_for_xml(self):
        data_filter = ["cputime", "walltime", "memory"]
        data = {k: self.measurements[k] for k in data_filter}
        return str_dict(data)
