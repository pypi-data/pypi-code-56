import os
import sys

import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.pyplot import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

import md_dihedrals
from md_dihedrals.__pkginfo__ import __version__
from md_dihedrals.readers.dihedrals_file import parse_dihedrals_directory
from md_dihedrals.readers.xvg_reader import XVGReader
from md_dihedrals.dihedrals_analysis.histogram import chi_histogram


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.init_ui()

        self.setWindowTitle("md_dihedrals version ({})".format(__version__))

        icon_path = os.path.join(md_dihedrals.__path__[0], "icons", "icon.jpg")
        self.setWindowIcon(QtGui.QIcon(icon_path))

        # Update the status bar
        self.statusBar().showMessage("md_dihedrals version {}".format(__version__))

    def build_events(self):
        """Set the signal:slots of the main window
        """

        # Signals/slots
        self._residues.currentRowChanged.connect(self.on_select_residue)
        self._run.clicked.connect(self.on_run)

    def build_layout(self):
        """Build the layout of the main window.
        """

        self._vl = QtWidgets.QVBoxLayout()

        select_layout = QtWidgets.QHBoxLayout()
        select_layout.addWidget(self._residues)
        select_layout.addWidget(self._chis)

        self._vl.addLayout(select_layout)

        n_bins_layout = QtWidgets.QHBoxLayout()
        n_bins_layout.addWidget(self._n_bins_label)
        n_bins_layout.addWidget(self._n_bins)

        self._vl.addLayout(n_bins_layout)

        self._vl.addWidget(self._run)

        self._vl.addWidget(self._canvas)
        self._vl.addWidget(self._toolbar)

        self._main_frame.setLayout(self._vl)

    def build_menu(self):
        """Build the menu of the main window.
        """

        file_action = QtWidgets.QAction(QtGui.QIcon('file.png'), '&File', self)
        file_action.setShortcut('Ctrl+O')
        file_action.setStatusTip('Open dihedrals directory')
        file_action.triggered.connect(self.on_open_dihedrals_directory)

        exit_action = QtWidgets.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.on_quit_application)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')

        file_menu.addAction(file_action)
        file_menu.addAction(exit_action)

    def build_widgets(self):
        """Build the widgets of the main window.
        """

        self._main_frame = QtWidgets.QFrame(self)

        self._residues = QtWidgets.QListWidget()
        self._residues.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self._chis = QtWidgets.QListWidget()
        self._chis.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self._n_bins_label = QtWidgets.QLabel()
        self._n_bins_label.setText('Number of bins')
        self._n_bins = QtWidgets.QSpinBox()
        self._n_bins.setMinimum(1)
        self._n_bins.setMaximum(10000)
        self._n_bins.setValue(100)

        self._run = QtWidgets.QPushButton()
        self._run.setText('Run')

        self._figure = Figure()
        self._axes = self._figure.add_subplot(111)
        self._canvas = FigureCanvasQTAgg(self._figure)
        self._toolbar = NavigationToolbar2QT(self._canvas, self)

        self.setCentralWidget(self._main_frame)

        self.setGeometry(0, 0, 800, 800)

        self.statusBar().showMessage("md_dihedrals version {}".format(__version__))

        self.show()

    def init_ui(self):
        """Set the widgets of the main window
        """

        self._reader = None

        self.build_menu()

        self.build_widgets()

        self.build_layout()

        self.build_events()

    def on_open_dihedrals_directory(self):
        """Event called when the open dihedrals directory menu item is clicked.
        """

        dihedrals_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select dihedrals directory", options=QtWidgets.QFileDialog.DontUseNativeDialog)

        if not dihedrals_dir:
            return

        self._dihedrals_dir = dihedrals_dir

        self._xvg_contents = parse_dihedrals_directory(self._dihedrals_dir)

        self._residues.clear()
        self._residues.addItems(self._xvg_contents.keys())

        self.statusBar().showMessage("dihedrals directory: {}".format(self._dihedrals_dir))

    def plot_1d(self, chi_file):

        reader = XVGReader(chi_file)

        self._axes.clear()
        self._axes.set_xlabel('frame (a.u.)')
        self._axes.set_ylabel('angle (deg)')
        self._axes.set_ylim([-180.0, 180.0])

        self._axes.plot(reader.x, reader.y)

        self._canvas.draw()

    def plot_2d(self, chi_file_1, chi_file_2):

        selected_chis = self._chis.selectedItems()
        selected_chis = [v.text() for v in selected_chis]

        reader1 = XVGReader(chi_file_1)
        reader2 = XVGReader(chi_file_2)

        n_bins = self._n_bins.value()

        hist = chi_histogram(-180.00, 180.00, n_bins, reader1.y, reader2.y)

        self._axes.clear()
        plot = self._axes.imshow(hist, aspect='equal', origin='lower')
        self._axes.set_xlabel('{} (deg)'.format(selected_chis[0]))
        self._axes.set_ylabel('{} (deg)'.format(selected_chis[1]))
        ticks = range(-180, 181, 20)
        self._axes.set_xticks(np.linspace(0, n_bins, len(ticks)))
        self._axes.set_xticklabels(ticks, rotation=45)
        self._axes.set_yticks(np.linspace(0, n_bins, len(ticks)))
        self._axes.set_yticklabels(ticks)
        self._figure.colorbar(plot)

        self._canvas.draw()

    def on_quit_application(self):
        """Event handler when the application is exited.
        """

        choice = QtWidgets.QMessageBox.question(self, 'Quit',
                                                "Do you really want to quit?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            sys.exit()

    def on_run(self):

        current_residue = self._residues.currentItem().text()
        if not current_residue:
            error_message = QtWidgets.QMessageBox()
            error_message.setIcon(QtWidgets.QMessageBox.Warning)
            error_message.setText('No residue selected')
            error_message.exec()
            return

        selected_chis = self._chis.selectedItems()
        n_selected_chis = len(selected_chis)

        if n_selected_chis == 1:
            chi_file = '{}{}.xvg'.format(selected_chis[0].text(), current_residue)
            chi_file = os.path.join(self._dihedrals_dir, chi_file)
            self.plot_1d(chi_file)
        elif n_selected_chis == 2:
            chi_file_1 = '{}{}.xvg'.format(selected_chis[0].text(), current_residue)
            chi_file_1 = os.path.join(self._dihedrals_dir, chi_file_1)

            chi_file_2 = '{}{}.xvg'.format(selected_chis[1].text(), current_residue)
            chi_file_2 = os.path.join(self._dihedrals_dir, chi_file_2)
            self.plot_2d(chi_file_1, chi_file_2)
        else:
            error_message = QtWidgets.QMessageBox()
            error_message.setIcon(QtWidgets.QMessageBox.Warning)
            error_message.setText('Invalid chi selection: you must select only 1 or 2 chis')
            error_message.exec()
            return

    def on_select_residue(self):
        """Event handler called when a residue is selected.
        """

        current_residue = self._residues.currentItem().text()
        self._chis.clear()
        self._chis.addItems(self._xvg_contents[current_residue])

