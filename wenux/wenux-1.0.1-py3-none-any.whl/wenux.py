#!/usr/bin/python3

import subprocess
import shlex

from Gui.Gui import WenuxGUI
from PyQt5 import QtWidgets
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    subprocess.call(shlex.split(f"./bridge.sh setup {sys.argv[1]} {sys.argv[2]}"))
    application = WenuxGUI()
    application.show()
    sys.exit(app.exec())
