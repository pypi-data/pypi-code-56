import json
import logging
import os
import tarfile

from dataclasses import dataclass
from ftplib import FTP

import click


logger = logging.getLogger(__name__)


@dataclass
class CarlaeSettings:
    hostname: str
    port: int
    username: str
    password: str


def _get_channel_subdir(filename):
    with tarfile.open(filename, mode="r|bz2") as tar:
        index = [
            json.load(tar.extractfile(f)) for f in tar if f.name == "info/index.json"
        ][0]
        return index["subdir"]


def upload(
    config: CarlaeSettings,
    conda_packages,
    channel_name=None,
    label="main",
    conflict="fail",
):
    channel_name = channel_name if channel_name else config.username

    proposed_packages = {
        f"{_get_channel_subdir(package)}/{os.path.basename(package)}": package
        for package in conda_packages
    }

    ftp = FTP()
    ftp.connect(config.hostname, config.port)
    ftp.login(config.username, config.password)

    ftp.cwd(channel_name)
    ftp.cwd("label")

    # Create label if it does not exist (main always exists)
    if label != "main" and label not in (e[0] for e in ftp.mlsd()):
        ftp.voidcmd(f"SITE MKLABEL {label}")
    ftp.cwd(label)

    # Create all subdirs
    existing_subdirs = {e[0] for e in ftp.mlsd(facts=["type"]) if e[1]["type"] == "dir"}
    new_subdirs = {k.split("/")[0] for k in proposed_packages.keys()}
    for subdir in new_subdirs - existing_subdirs:
        ftp.mkd(subdir)

    if conflict != "overwrite":
        # TODO: This does not scale as number of packages goes up,
        #       need to look into SITE EXEC or OPTIONS
        # Get a list of existing files
        existing_files = {
            f"{subdir}/{filename}"
            for subdir in existing_subdirs | new_subdirs
            for filename, facts in ftp.mlsd(subdir, facts=["type"])
        }
        conflict_files = existing_files & proposed_packages.keys()
        if conflict == "skip":
            for p in conflict_files:
                logger.debug(f"skipping {p}")
                del proposed_packages[p]
        elif conflict == "ask":
            for p in conflict_files:
                if not click.confirm(
                    f"{p} already exists on the server. Would you like to overwrite?",
                    default=False,
                    show_default=True,
                ):
                    del proposed_packages[p]
        elif conflict == "fail" and conflict_files:
            conflict_files = sorted(conflict_files)
            raise KeyError(
                f"The following package(s) already exist on the server: {conflict_files}"
            )

    # Upload packages to correct location
    for path, package in proposed_packages.items():
        with open(package, mode="rb") as f:
            ftp.storbinary(f"STOR {path}", fp=f)
