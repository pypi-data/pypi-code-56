# This file is part of CoVeriTeam, a tool for on-demand composition of cooperative verification systems:
# https://gitlab.com/sosy-lab/software/coveriteam
#
# SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import yaml
from zipfile import ZipFile
from coveriteam.language.artifact import Artifact
import re
import benchexec
import time


LOG_DIR = "output/"
TOOL_OUTPUT_FILE = "output.txt"
OPTIONS_FILE_PATH = "config/options"
# TODO The following is problematic. It will fail when used for running tests.
# It should change.
INPUT_FILE_DIR = "coveriteam/artifactlibrary/"
INSTALL_DIR = "tools/"
ARCHIVE_DOWNLOAD_PATH = "archives/"


def get_actor_config(path):
    with open(path, "r") as f:
        try:
            d = yaml.safe_load(f)
        except yaml.YAMLError as e:
            sys.exit("Actor config yaml file {} is invalid: {}".format(path, e))

        if d["toolinfo_module"].endswith(".py"):
            d["toolinfo_module"] = d["toolinfo_module"].rpartition(".")[0]

        # translate resource limits
        reslim = d.get("resourcelimits", None)
        if reslim:
            reslim["memlimit"] = benchexec.util.parse_memory_value(reslim["memlimit"])
            reslim["timelimit"] = benchexec.util.parse_timespan_value(
                reslim["timelimit"]
            )
            d["resourcelimits"] = reslim

        return d


def get_actor_installation_dir(archive):
    # Get the dir name from the zip archive
    # Assuming that the archive is wellformed.
    with ZipFile(archive, "r") as z:
        return INSTALL_DIR + z.filelist[0].filename.split("/")[0]


def is_url(path):
    return path.startswith("http://") or path.startswith("https://")


def resolve_url_archive(url):
    # Assumping that the provided archive path ends in .zip
    expected_download_path = ARCHIVE_DOWNLOAD_PATH + url.rpartition("/")[2]
    if not os.path.isfile(expected_download_path):
        os.system("wget " + url + " -P " + ARCHIVE_DOWNLOAD_PATH)
    return expected_download_path


def install_if_needed(archive, dir_name):
    target_dir = INSTALL_DIR + dir_name
    if os.path.isdir(target_dir):
        return target_dir
    if is_url(archive):
        archive = resolve_url_archive(archive)
    install_path = get_actor_installation_dir(archive)
    if not (os.path.isdir(install_path)):
        os.system("unzip " + archive + " -d " + INSTALL_DIR)

    os.rename(install_path, target_dir)
    return target_dir


def filter_dict(d, d1):
    return {k: d[k] for k in d1.keys()}


def str_dict(d):
    return {k: str(d[k]) for k in d.keys()}


def dict_clash(d1, d2):
    """
    This function checks if there is a key present in both dictionaries
    whose values are different.
    """
    for k in d1.keys():
        if k in d2.keys() and d1[k] != d2[k]:
            return True

    return False


def rename_dict(d, renaming_map):
    return {(renaming_map.get(k, None) or k): d[k] for k in d.keys()}


def collect_variables(exp):
    regex_isinstance = r"(?<=isinstance\()\S+(?=,)"
    regex_in = r"\w+(?= in \[)"
    regex = regex_isinstance + "|" + regex_in
    names = re.findall(regex, exp)

    return names


def infer_types(exp):
    d = {}
    # TODO At the moment it is rudimentory. Putting Artifact for everything
    for name in collect_variables(exp):
        if not name.startswith("RESULT_CLASS"):
            d[name] = Artifact

    return d


def move_exec_xml(file_path):
    filename = file_path.rpartition("/")[2]
    filename = filename.rpartition(".")[0]
    ts = time.strftime("%Y%m%d%H%M%S", time.localtime())

    target_dir = os.path.join(os.getcwd(), LOG_DIR)
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)
    filename = filename + ts + ".xml"

    if os.path.isfile(os.path.join(os.getcwd(), "execution_trace.xml")):
        os.system("mv execution_trace.xml " + os.path.join(target_dir, filename))
