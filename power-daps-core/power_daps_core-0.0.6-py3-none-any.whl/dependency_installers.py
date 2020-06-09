#  Copyright 2016-2020 Prasanna Pendse <prasanna.pendse@gmail.com>
#
#  This file is part of power-daps.
#
#  power-daps is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  power-daps is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with power-daps.  If not, see <https://www.gnu.org/licenses/>.

import os, sys, re
import urllib.request
from distutils.version import LooseVersion
from xml.etree import ElementTree
from shutil import which
from dap_core import common


class CommandLineInstaller:
  def __init__(self, command_base):
    self.command_base = command_base
    return

  def install(self, dep_name, dep_version, details):
    exit_code, output = common.run_command(self.command_base + [dep_name])
    common.stop_if_failed(exit_code, output)


class PipInstaller:
  NOT_INSTALLED = 0
  SAME_VERSION_INSTALLED = 1
  OLDER_VERSION_INSTALLED = 2
  NEWER_VERSION_INSTALLED = 3

  def __init__(self):
    return

  def install(self, dep_name, dep_version="latest", details={}):
    package_name = dep_name
    if not dep_version == "latest":
      package_name = dep_name + "==" + str(dep_version)

    status = self.is_already_installed(dep_name, dep_version)
    if status == PipInstaller.NOT_INSTALLED:
      common.print_verbose(dep_name + " not installed. Installing.")
      command_to_run = [which('pip3'), '-q', 'install', package_name]
      exit_code, output = common.run_command(command_to_run)
      common.stop_if_failed(exit_code, output)

    elif status == PipInstaller.OLDER_VERSION_INSTALLED:
      common.print_verbose(dep_name + " is already installed. Upgrading to " + dep_version + " version.")

      command_to_run = [which('pip3'), '-q', 'install', '--upgrade', package_name]
      exit_code, output = common.run_command(command_to_run)
      common.stop_if_failed(exit_code, output)

    elif status == PipInstaller.NEWER_VERSION_INSTALLED:
      common.print_verbose(
        "Newer version of " + dep_name + " installed. Uninstalling and installing " + dep_version + " version.")

      command_to_run = [which('pip3'), '-q', 'uninstall', package_name]
      exit_code, output = common.run_command(command_to_run)
      common.stop_if_failed(exit_code, output)

      command_to_run = [which('pip3'), '-q', 'install', package_name]
      exit_code, output = common.run_command(command_to_run)
      common.stop_if_failed(exit_code, output)
    else:
      common.print_verbose(dep_name + ", " + dep_version + " is already installed. Doing nothing.")

  def is_already_installed(self, dep_name, dep_version):
    exit_code, output = common.run_command_in_shell("pip3 list --format=columns | grep -i " + dep_name)
    if not output:
      return PipInstaller.NOT_INSTALLED
    else:
      installed_version = re.sub(' +', ' ', output).split(" ")[1]

      if dep_version == "latest":
        # Assume older version so dap will try to upgrade automatically
        return PipInstaller.OLDER_VERSION_INSTALLED
      elif LooseVersion(installed_version) == LooseVersion(dep_version):
        return PipInstaller.SAME_VERSION_INSTALLED
      elif LooseVersion(installed_version) < LooseVersion(dep_version):
        return PipInstaller.OLDER_VERSION_INSTALLED
      elif LooseVersion(installed_version) > LooseVersion(dep_version):
        return PipInstaller.NEWER_VERSION_INSTALLED


class SysInstaller:
  def __init__(self):
    return

  def install(self, dep_name, dep_version="latest", details={}):
    if details and details['env_vars']:
      for env_var_name, env_var_value in details['env_vars'].items():
        os.environ[env_var_name] = str(env_var_value)
        common.print_verbose("set " + str(env_var_name) + "=" + str(env_var_value))
    install_command = [self.installer(), "install",
                       self.dependency_with_version(dep_name, dep_version, self.installer())]
    common.print_verbose(install_command)
    return common.run_command(install_command)

  def dependency_with_version(self, dep_name, dep_version, sys_installer):
    if dep_version == "latest":
      return dep_name
    elif sys_installer == "brew":
      return dep_name + "@" + dep_version
    elif sys_installer == "apt-get":
      return dep_name + "=" + dep_version
    elif sys_installer == "yum":
      return dep_name + "-" + dep_version
    else:
      return ""

  def installer(self):
    if sys.platform.startswith('darwin'):
      return 'brew'
    elif sys.platform.startswith('linux'):
      if self.linux_distribution().startswith('debian'):
        return 'apt-get'
      elif self.linux_distribution().startswith('rhel'):
        return 'yum'
      else:
        common.print_error(
          "Cannot install system dependencies because /etc/os-release does not exist. It is required to determine linux distribution.")
    else:
      common.exit_with_error_message("Sorry, only Linux (Ubuntu, CentOS) and Mac OS X are currently supported")

  def linux_distribution(self):
    exit_code, output = common.run_command([which('grep'), 'ID_LIKE', '/etc/os-release'])
    return output.split("=")[1].rstrip()

