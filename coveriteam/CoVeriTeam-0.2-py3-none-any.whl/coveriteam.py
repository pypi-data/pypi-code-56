# This file is part of CoVeriTeam, a tool for on-demand composition of cooperative verification systems:
# https://gitlab.com/sosy-lab/software/coveriteam
#
# SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import argparse
import coveriteam.util as util
from coveriteam.interpreter.python_code_generator import generate_python_code
import logging
import coveriteam
from coveriteam.language.atomicactor import AtomicActor


class CoVeriTeam:
    def start(self, argv):
        self.__set_paths()
        self.config = self.create_argument_parser().parse_args(argv[1:])
        str_to_prepend = ""

        if self.config.testtool:
            a = AtomicActor(self.config.input_file)
            a.print_version()
            return

        if self.config.clean:
            os.system("rm -rf " + util.INSTALL_DIR)

        if self.config.debug:
            FORMAT = "%(asctime)-15s %(levelname)s %(message)s"
            logging.basicConfig(level=logging.DEBUG, format=FORMAT)

        if self.config.inputs:
            d = dict(self.config.inputs)
            for k in d:
                str_to_prepend += k + " = " + repr(d[k]) + ";\n"

        if self.config.input_file:
            """"CVL file is provided."""
            generated_code = str_to_prepend + generate_python_code(
                self.config.input_file
            )
            if self.config.generate_code:
                print(generated_code)
            else:
                exec(generated_code, globals())
                # TODO temp solution. TO be done better later.
                util.move_exec_xml(self.config.input_file)

    def create_argument_parser(self):
        """
        Create a parser for the command-line options.
        @return: an argparse.ArgumentParser instance
        """
        parser = argparse.ArgumentParser(
            prog="coveriteam",
            fromfile_prefix_chars="@",
            description="""Execute a program written in CoVeriLang.
               Command-line parameters can additionally be read from a file if file name prefixed with '@' is given as argument.
               """,
        )
        parser.add_argument(
            "--version", action="version", version=f"{coveriteam.__version__}"
        )

        parser.add_argument(
            "--tool-info",
            dest="testtool",
            action="store_true",
            default=False,
            help="Test the given YML file configuration by executing the tool for version.",
        )

        parser.add_argument(
            "input_file",
            metavar="INPUT_FILE",
            help="The program written in CoVeriLang or a YML configuration if testing a tool.",
        )
        parser.add_argument(
            "--input",
            action="append",
            type=lambda kv: kv.split("="),
            dest="inputs",
            help="Inputs to the CoVeriLang program provided in the form of key=val.",
        )

        parser.add_argument(
            "--gen-code",
            dest="generate_code",
            action="store_true",
            default=False,
            help="Flag to generate python code from the cvl file.",
        )

        parser.add_argument(
            "--clean",
            dest="clean",
            action="store_true",
            default=False,
            help="Clean the tmp directory, which contains the extracted archives of the atomic actors.",
        )

        parser.add_argument(
            "--debug",
            dest="debug",
            action="store_true",
            default=False,
            help="Set the logging to debug.",
        )

        return parser

    def __set_paths(self):
        root_dir = sys.path[0]
        cache_dir = os.getenv("XDG_CACHE_HOME")
        if not cache_dir:
            cache_dir = os.path.join(os.getenv("HOME"), ".cache")
        cache_dir = os.path.join(cache_dir, "coveriteam")
        util.LOG_DIR = os.path.join(root_dir, util.LOG_DIR)
        util.INSTALL_DIR = os.path.join(cache_dir, util.INSTALL_DIR)
        util.ARCHIVE_DOWNLOAD_PATH = os.path.join(cache_dir, util.ARCHIVE_DOWNLOAD_PATH)
        util.INPUT_FILE_DIR = os.path.join(root_dir, util.INPUT_FILE_DIR)


def main(argv=None):
    CoVeriTeam().start(argv or sys.argv)


if __name__ == "__main__":
    main()
