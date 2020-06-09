# Lattice Explorer
# Copyright (C) 2020  Dominik Vilsmeier

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import logging
import sys

from arguable import Arguable
from PyQt5.QtWidgets import QApplication

from .explorer import LatticeExplorer
from .widgets import ConfigWidget


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
    )

    Arguable.super_parser.add_argument('script')
    args = Arguable.super_parser.parse_args()  # Check excess arguments and process --help.

    app = QApplication([])
    window = LatticeExplorer(args.script)
    window.show()
    sys.exit(app.exec_())
