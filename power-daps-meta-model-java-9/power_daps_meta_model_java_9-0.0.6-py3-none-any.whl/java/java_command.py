
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

import os
from dap_core import common
from power_daps.java import java_helper

class JavaCommand:
  def __init__(self, main_class, args_to_main_class=[], classpath=""):
    self.main_class = main_class
    self.args_to_main_class = args_to_main_class
    self.classpath = classpath
    self.java_opts = os.getenv("JAVA_OPTS", "")
    common.print_raw("JAVA_OPTS=" + self.java_opts)


  def run(self):
    cp_string = java_helper.classpath_string(self.classpath)
    command_array = []
    command_array.append(common.which('java'))
    command_array.append(cp_string.lstrip())
    if self.java_opts:
      command_array.append(self.java_opts)
    command_array.append(self.main_class)
    command_array.extend(self.args_to_main_class)

    run_unit_test_command = " ".join(command_array).split(" ")

    exit_code, output = common.run_with_io(run_unit_test_command)
    try:
      output = output.decode()
    except (UnicodeDecodeError, AttributeError):
      pass
    # common.print_raw(output)
    return exit_code, output


