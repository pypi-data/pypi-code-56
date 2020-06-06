#!/usr/bin/env python3
import logging
import argparse
import sys
from PyQt5 import QtWidgets
import ct.gui.main_win
import ct.ct_global
import os.path


def on_about_to_quit_fired():
    print("on_about_to_quit_fired")
    # anxiety.model.History.close()
    ####rg.model_old.backup_db_file()


def main():
    # Setting the path of the file to the current directory
    abs_path_str = os.path.abspath(__file__)
    dir_name_str = os.path.dirname(abs_path_str)
    os.chdir(dir_name_str)

    # Application setup..
    # ..command line arguments
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--testing", "-t", help="Testing", action="store_true")
    # -for info about "store_true" please search here: https://docs.python.org/3/howto/argparse.html
    args = argument_parser.parse_args()
    ct.ct_global.testing_bool = False
    if args.testing:
        ct.ct_global.testing_bool = True

    logging.basicConfig(level=logging.DEBUG)  # -by default only warnings and higher are shown

    """
    if not os.path.isfile(rg.model.DATABASE_FILE_NAME_STR):
        rg.model.setup_test_data()
    #rg.nn_global.active_rememberance_id =
    """

    application = QtWidgets.QApplication(sys.argv)

    application.setQuitOnLastWindowClosed(True)
    application.aboutToQuit.connect(on_about_to_quit_fired)
    main_window = ct.gui.main_win.MainWin()
    # main_window.showMaximized()

    sys.exit(application.exec_())


if __name__ == "__main__":
    main()


"""
Programming TODO: Add time left to window title (so that the time can be seen in the system tray)
Design TODO: Figuring out ways to show the alarm more clearly. Perhaps also removing the focus on the close button, so that the window is not accidentally closed when the user types
Design TODO: Maybe adding start and stop times, so that the user can track certain activities. Plus adding sliders for tracking what happens at the beginning and end
Programming TODO: Adding photo of a flower on the left side of the popup "notification" window

"""
