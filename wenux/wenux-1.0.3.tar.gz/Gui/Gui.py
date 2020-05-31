from Gui.Qt5 import Ui_WEnux
import os
import subprocess
import traceback
import Gui.Logging
import logging

from Tc.TcWrapper import TcWrapper
from Utils.ResourceMonitor import resource_monitor
from PyQt5 import QtWidgets, QtCore, QtGui
from Utils.Subprocess import run
import socket
from PyQt5.QtWidgets import QMessageBox

known_limits = {
    "Modem / Dialup": 56,
    "ADSL Lite": 1500,
    "T1 / DS1": 1544,
    "E1 / E - carrier": 2048,
    "ADSL1": 4000,
    "Ethernet": 10000,
    "Wireless 802.11b": 11000,
    "ADSL2 +": 24000,
    "T3 / DS3": 44736,
    "Wireless 802.11g": 54000,
    "Fast Ethernet": 100000
}

args = {}


class WenuxGUI(QtWidgets.QMainWindow):
    """WenuxGUI is the main part of PyQt5 GUI usage and control of WEnux

    This class is used as setup for the graphical user interface,
    it renders the look of GUI with PyQt5 library and handles the argument
    parsing from the GUI.
    Arguments are validated and later used for the calls to WEnux core.
    Class includes setup of logging, output and control of Qt related objects.

   """

    def __init__(self):
        super(WenuxGUI, self).__init__()
        self.ui = Ui_WEnux()
        self.ui.setupUi(self)

        stdout = Gui.Logging.OutputWrapper(self, True)
        stdout.outputWritten.connect(self.handle_output)
        stderr = Gui.Logging.OutputWrapper(self, False)
        stderr.outputWritten.connect(self.handle_output)
        self.terminal = self.ui.outputBrowser

        self.fill_boxes()
        self.ui.submitButton.clicked.connect(self.submit_clicked)
        self.ui.resetButton.clicked.connect(self.reset_clicked)

        if os.geteuid() != 0:
            logging.error("You need root permissions to run WEnux!")
            exit(3)

    def closeEvent(self, event):
        """Function overrides the default close button UI event

        As user can prematurely quit the application teardown of different
        objects is required. After teardown is done, exit event can be accepted.

       """
        try:
            tc = TcWrapper(**args)
            tc.teardown()
        except:
            logging.info("Quitting the application without configuration.")
        finally:
            run(f"./bridge.sh teardown")
            event.accept()

    def handle_output(self, text, stdout):
        """Setup of text output

        Text printed on standard output either through logging module or printing
        is redirected to the main window serving as a graphical console.

       """
        color = self.terminal.textColor()
        self.terminal.setTextColor(color if stdout else QtCore.Qt.red)
        self.terminal.insertPlainText(text)
        self.terminal.setTextColor(color)

    def fill_boxes(self):
        """Filling out of dynamic graphical elements

        Based on the system used with different interfaces the combo box
        with all interfaces has to be filled out each time application is run.
        Limit selection can be done with predefined limits, which are formatted.

       """
        self.ui.interfaceBox.addItem("test_bridge")
        for interface in os.listdir('/sys/class/net/'):
            self.ui.interfaceBox.addItem(interface)

        for type, limit in known_limits.items():
            if limit > 1000:
                unit = "Mbit/s"
                limit /= 1000
            else:
                unit = "kbit/s"
            self.ui.netemRateBox.addItem(f"{type} - {limit} {unit}")
            self.ui.netemRateBox.setCurrentIndex(5)

    def load_args(self):
        """Parser for arguments with basic checks

        Function inspects each Qt element where could be useful parameters
        for the Tc module. Arguments are checked, and basically sanitized
        to be appropriate types for later use.

        :return bool: result of argument loading, checking and sanitizing
       """
        output = {}

        debug = self.ui.debugBox.isChecked()
        Gui.Logging.set_logging(debug)

        args["nic"] = str(self.ui.interfaceBox.currentText())
        args["delay"] = self.ui.delayValue.value()
        args["jitter"] = self.ui.jitterValue.value()
        args["delay_jitter_corr"] = self.ui.delay_jitter_corrValue.value()
        args["overhead"] = self.ui.netemOverheadValue.value()
        args["limit"] = list(known_limits.values())[self.ui.netemRateBox.currentIndex()]
        args["direction"] = self.ui.directionBox.currentText()
        args["loss_ratio"] = self.ui.lossValue.value()
        args["loss_corr"] = self.ui.loss_corellationValue.value()
        args["dupl_ratio"] = self.ui.duplValue.value()
        args["dupl_corr"] = self.ui.dupl_correlationValue.value()
        args["reorder_ratio"] = self.ui.reorderValue.value()
        args["reorder_corr"] = self.ui.reorder_correlationValue.value()
        args["corrupt_ratio"] = self.ui.corruptValue.value()
        args["corrupt_corr"] = self.ui.corrupt_correlationValue.value()
        args["include"] = []
        args["exclude"] = []
        ret_code = self.args_check()

        for k, v in args.items():
            if v is 0:
                continue
            else:
                output[k] = v

        logging.info(output)
        return ret_code

    def submit_clicked(self):
        if not self.load_args():
            wenux_submit()
        else:
            pass

    def reset_clicked(self):
        wenux_reset()

    def get_args(self):
        return args

    def args_check(self):
        """Argument checker and sanitizer for later use in Tc module

        Parameters that arrive from the GUI frontend are checked if they contain
        correct information, such as IP addresses, ports.
        If they are valid, they are sanitized for later use

        :return bool: result of argument checking and sanitizing

       """
        for item in [self.ui.destinationNetworkLine, self.ui.destinationNetworkLineE,
                     self.ui.sourceNetworkLine, self.ui.sourceNetworkLineE,
                     self.ui.sourcePortLine, self.ui.sourcePortLineE,
                     self.ui.destinationPortLineE, self.ui.destinationPortLine
                     ]:
            if "destination" in item.objectName():
                if "Port" in item.objectName():
                    prefix = "dport="
                else:
                    prefix = "dst="
            else:
                if "Port" in item.objectName():
                    prefix = "sport="
                else:
                    prefix = "src="

            if item.text():
                for attr in item.text().split(","):
                    try:
                        attr = attr.strip()
                    except AttributeError:
                        pass

                    if not validate_addr(attr):
                        if "E" in item.objectName():
                            args["exclude"].append(f"{prefix}" + attr)
                        else:
                            args["include"].append(f"{prefix}" + attr)
                    elif not validate_port(item.text()):
                        if "E" in item.objectName():
                            args["exclude"].append(f"{prefix}" + attr)
                        else:
                            args["include"].append(f"{prefix}" + attr)
                    else:
                        return 1
                    continue


# WEnux

def wenux_submit():
    """Main call to the Tc module that controls the emulation

    TcWrapper that gathers the arguments and controls the emulation
    load the arguments, initializes the setup according to parameters
    and calls appropriate tc module for the emulation.
    If emulation fails, it tears down the setup and quits the application

   """
    try:
        tc = TcWrapper(**args)
        tc.initialize()

        tc.netem("add")
        # tc.tbf("add")

    except subprocess.CalledProcessError:
        traceback.print_exc()
        tc.teardown()
        exit(2)


def wenux_reset():
    try:
        tc = TcWrapper(**args)
        tc.teardown()
    except:
        pass


def popup_error(err_type, text):
    """Popup QMessageBox in case of invalid arguments

    When invalid arguments are presented in the GUI by user,
    popup window shows up and doesn't let user continue

   """
    msg = QMessageBox()
    msg.setWindowTitle(f"Invalid {err_type}")
    msg.setText(text)
    msg.setIcon(QMessageBox.Critical)
    msg.exec_()


def validate_port(port):
    print(port)
    if not 0 <= int(port) <= 65535:
        popup_error("port", "The port you have entered is not a valid port number!")
        return 1
    return 0


def validate_addr(addr):
    """Validation of network address to be used in inclusion or exclusion

    :param addr is first checked whether it is in a network format or
    already in IP addresss notation. It separates mask and address or
    if needed adds a mask.

    Mask is verified based on the IP family it belongs to and appropriate
    text to network structure function is called to verify whether
    the IP adress is correct, if the exception is raised adress is invalid

    :return bool: state of validation

   """
    try:
        if "/" in addr:
            mask = addr.partition("/")[2]
            addr = addr.partition("/")[0]
        else:
            mask = 32

        if not ":" in addr:
            if not 0 <= int(mask) <= 32:
                raise socket.error
            socket.inet_aton(addr)
        else:
            if not 0 <= int(mask) <= 128:
                raise socket.error
            socket.inet_pton(socket.AF_INET6, addr)
    except socket.error:
        popup_error("IP address", "The IP you have entered is not a valid address!")
        return 1
    return 0
