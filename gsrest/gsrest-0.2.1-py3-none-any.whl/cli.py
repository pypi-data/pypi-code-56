#!/usr/bin/env python3
#
# Copyright (c) 2020 Instituto Tecnológico de Canarias, S.A.
#
# This file is part of GsRest
# (see https://github.com/esuarezsantana/gsrest).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""
gsrest command-line interface.
"""

import argparse
import dataclasses
import logging
import sys
from urllib import error as urlerr

from . import client, ops, yaml
from .core import url


@dataclasses.dataclass  # pylint: disable=too-many-instance-attributes
class GsCli:
    "Run simple actions on a geoserver instance"
    host: dataclasses.InitVar[str]
    port: dataclasses.InitVar[int]
    context: dataclasses.InitVar[str]
    user: dataclasses.InitVar[str]
    password: dataclasses.InitVar[str]
    logger: dataclasses.InitVar[logging.Logger]
    yamlpath: str = dataclasses.field(init=False)
    force_purge: bool = dataclasses.field(init=False)

    # pylint: disable=too-many-arguments
    def __post_init__(self, host, port, context, user, password, logger):
        "Post initialization."
        self.logger = logger
        base_url = url.gs_base_url(host=host, port=port, context=context)
        self.client = client.GsClient()
        self.client.base_url = base_url
        self.client.user = user
        self.client.password = password

    def do(self, action):  # pylint: disable=invalid-name
        "Action broker."
        getattr(self, action)()

    def sync(self):
        "Sync up yaml elements."
        self.logger.debug("Loading YAML file.")
        elems = yaml.read(self.yamlpath)
        self.logger.debug("BEGIN SYNC action.")
        elems.sync()
        self.logger.debug("END SYNC action.")

    def delete(self):
        "Delete yaml elements (reverse order)."
        self.logger.debug("Loading YAML file.")
        elems = yaml.read(self.yamlpath)
        self.logger.debug("BEGIN DELETE action.")
        elems.delete()
        self.logger.debug("END DELETE action.")

    def purge(self):  # pylint: disable=no-self-use
        "Purge all instance elements."
        if self.force_purge:
            self.logger.debug("BEGIN PURGE action.")
            ops.Ops.purge()  # implicit 'self' here
            self.logger.debug("END PURGE action.")
        else:
            self.logger.warning("PURGE operation ignored. Use '-f'.")


def setup_logger(logto, verbose):
    """Setup logger."""
    logformat = (
        "%(asctime)s %(name)-20s [%(levelname)-5s] %(message)s"
        if verbose > 1
        else "%(message)s"
    )

    if logto is None:
        logging.basicConfig(format=logformat)
    else:
        logging.basicConfig(filename=logto, format=logformat)

    if verbose:
        logging.getLogger("gsrest").setLevel(logging.DEBUG)
    else:
        logging.getLogger("gsrest").setLevel(logging.WARNING)

    return logging.getLogger(__name__)


def parse_args():
    """Parse arguments.

    Returns:
        Args named tuple.
    """

    parser = argparse.ArgumentParser(description="Geoserver Rest API CLI")
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase verbosity"
    )
    parser.add_argument("-l", "--logto", help="File to log to")
    parser.add_argument(
        "-H", "--host", default="localhost", help="GeoServer host"
    )
    parser.add_argument(
        "-P", "--port", type=int, default=8080, help="GeoServer port"
    )
    parser.add_argument(
        "-c",
        "--context",
        default="geoserver",
        help="GeoServer context (url path)",
    )
    parser.add_argument(
        "-u", "--user", default="admin", help="Geoserver login user"
    )
    parser.add_argument(
        "-p",
        "--password",
        default="geoserver",
        help="GeoServer login password",
    )
    subparsers = parser.add_subparsers()
    parser_sync = subparsers.add_parser("sync", help="Sync up elements")
    parser_sync.add_argument("yaml", help="Path to YAML file.")
    parser_sync.set_defaults(action="sync")
    parser_delete = subparsers.add_parser("delete", help="Delete elements")
    parser_delete.add_argument("yaml", help="Path to YAML file.")
    parser_delete.set_defaults(action="delete")
    parser_purge = subparsers.add_parser("purge", help="Purge instance")
    parser_purge.add_argument(
        "-f", "--force", action="store_true", help="Actually do it."
    )
    parser_purge.set_defaults(action="purge")

    return parser.parse_args()


def main():
    "Main function"

    args = parse_args()
    logger = setup_logger(args.logto, args.verbose)
    logger.info(40 * "-")
    logger.info("GsRest Script STARTED.")
    for key, value in vars(args).items():
        logger.debug("Input arguments: %s = %s.", key, value)

    try:
        broker = GsCli(
            args.host,
            args.port,
            args.context,
            args.user,
            args.password,
            logger,
        )
        broker.yamlpath = getattr(args, "yaml", None)
        broker.force_purge = getattr(args, "force", False)
        broker.do(args.action)
    except urlerr.URLError:
        logger.error("URL Error.")
        logger.info("GsRest Script ABORTED.")
        sys.exit(3)
    except yaml.GsYamlError:
        logger.error("Error loading Yaml file.")
        logger.info("GsRest Script ABORTED.")
        sys.exit(4)
    except client.GsElementDoesNotExist:
        logger.error("Element does not exist.")
        logger.info("GsRest Script ABORTED.")
        sys.exit(5)
    except client.GsException as err:
        logger.error("Geoserver Exception: %s", str(err))
        logger.info("GsRest Script ABORTED.")
        sys.exit(6)
    except:  # noqa: E722
        logger.error("SOMETHING UNEXPECTED WENT WRONG!!!")
        logger.info("GsRest Script ABORTED.")
        raise
    else:
        logger.info("GsRest Script FINISHED.")
    finally:
        logger.info(40 * "-")

    sys.exit(0)


if __name__ == "__main__":
    main()
