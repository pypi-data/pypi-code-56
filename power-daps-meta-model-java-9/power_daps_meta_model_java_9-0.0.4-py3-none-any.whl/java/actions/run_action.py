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

from dap_core import common
from dap_core.base_actions.dap_action_base import DapActionBase
from power_daps.java import java_helper
from power_daps.java.java_command import JavaCommand


class RunAction(DapActionBase):

  def __init__(self):
    super().__init__()

  def run(self):
    super().run()
    main_files = common.find_files_containing("public static void main(")
    common.print_verbose(main_files)

    for main_file in main_files:
      main_class = main_file.replace("./src/", '').replace('.java', '').replace('/', '.')
      JavaCommand(main_class, [], java_helper.production_classpath()).run()

    return 0, ""

def action():
  return RunAction()
