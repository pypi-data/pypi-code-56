# Copyright (C) Martin Singer <martin.singer@web.de>
#
# This file is part of PDF Chain.
#
# PDF Chain is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PDF Chain is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PDF Chain.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Martin Singer

"""
@brief The Package Main Module.
@details
    This module is called when starting the application
    by calling the directory or the ZIP package (zipapp) name.
@par
    The current path as python search path is required
    when the application is executed in an individual path.
    The current path is not required
    when the application is started by the `bin/pdfchain` script.
@par
    This module is usually called during the development.
    Therefore, it is important to prepend the current path
    to the list of search paths,
    so that when the developer package is executed,
    the modules that were modified during development are loaded,
    and not those of a possibly installed version.
"""

import sys
import os


# Get project root directory (alternative - not sure, which one is better)
# PROJECT_ROOT_DIRECTORY = os.path.abspath(
#       os.path.dirname(os.path.realpath(sys.argv[0])))

# Get project root directory
PROJECT_ROOT_DIRECTORY = os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir))

# Prepend project root directory to python search path
sys.path.insert(0, PROJECT_ROOT_DIRECTORY)

# print("sys.path: '{}'".format(sys.path)) #TEST


from pdfchain.main import main


if __name__ == "__main__":
    main()
