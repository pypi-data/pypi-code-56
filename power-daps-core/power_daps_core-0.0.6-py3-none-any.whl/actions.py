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

import yaml
from dap_core import common
from dap_core.meta_model import MetaModel
from dap_core.no_action_error import NoActionError
from dap_core.base_actions.dap_action_base import DapActionBase


class LocalAction(DapActionBase):
  def __init__(self, name, actions={}):
    super().__init__()
    self.actions = actions
    self.n = name

  def name(self):
    return self.n

  def run(self):
    super().run()
    exit_code = 0
    output = ""
    for a in self.actions:
      ec, o = action_for(a).run()
      exit_code += ec
      output += "\n" + output

    return exit_code, output


def local_actions():
  actions_file_location = "./actions.yml"
  actions = []
  try:
    with open(actions_file_location) as f:
      actions_file_contents = f.read()
      for stage in yaml.load(actions_file_contents, Loader=yaml.SafeLoader).items():
        action_name = stage[0]
        list_of_sub_actions = stage[1]
        if action_name != "default":
          actions.append(LocalAction(action_name, list_of_sub_actions))
    f.closed
  except(OSError, IOError) as e:
    common.print_verbose("No actions file found at " + actions_file_location)

  return actions


def action_for(action_name):
  meta_model = MetaModel(common.meta_model())
  the_actions = list(filter(lambda a: common.action_name(a) == action_name, meta_model.actions()))
  if the_actions:
    return the_actions[0]
  else:
    return NoActionError(action_name)
