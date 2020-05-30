#!/usr/bin/env python3
from matplotlib.backends.backend_qt5agg import\
        FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtPrintSupport
import matplotlib
import numpy as np
import prasopes.datatools as dt
import prasopes.graphtools as gt
import prasopes.filetools as ft
import prasopes.config as cf
import os.path
import logging
matplotlib.use("Qt5Agg")


logger = logging.getLogger('drlLogger')


def floatize(table, row, column, nonneg=True):
    """grabs the tableWidgetItem and transforms its text safely to
    float, if the text is not acceptable as float, returns zero"""
    imptext = table.item(row, column).text().replace(",", ".")
    validator = QtGui.QDoubleValidator()
    if nonneg:
        validator.setBottom(0)
    status = validator.validate(imptext, 0)[0]
    outfloat = float(imptext) if status == QtGui.QValidator.Acceptable\
        else 0
    return outfloat


def get_massargs(pt, row, subset):
    startm = floatize(pt, row, 1) - (floatize(pt, row, 2) / 2)
    endm = floatize(pt, row, 1) + (floatize(pt, row, 2) / 2)
    massargs = dt.argsubselect(subset['masses'], startm, endm)
    return massargs


def get_intensity(row, ds, drls):
    # prevent division by 0
    intensity = np.concatenate([np.divide(np.sum(subset['matrix'].T[
        get_massargs(drls['pt'], row, subset)].T, axis=1),
        np.clip(subset['chrom_dat'][1], np.finfo(np.float32).eps, None))
        for subset in ds])
    return intensity


def get_daughterset(ds, drls):
    """Fuction to acquire the curves of the daugher ions"""
    logger.info("getting set of the daughter ions")
    names = []
    times = np.concatenate([sub['chrom_dat'][0, :] - drls['tshift'].value()
                            for sub in ds])
    intensities = []
    for row in range(drls['dt'].rowCount()):
        if drls['dt'].cellWidget(row, 0).checkState() == 2:
            intensity = get_intensity(row, ds, drls)
            corlist = []
            for i in range(drls['cors'].value()):
                cor = drls['dt'].cellWidget(row, 1+i*2).currentIndex() - 1
                if cor not in (-2, -1):
                    factor = floatize(drls['dt'], row, 2+i*2, False)
                    correction = get_intensity(cor, ds, drls) * factor
                    intensity = intensity - correction
                    corlist.append("{} * {}".format(
                        drls['dt'].item(row, 2+i*2).text(),
                        drls['dt'].cellWidget(row, 1+i*2).currentText()))
            cortext = " + ".join(corlist)
            intensities.append(intensity)
            names.append("{} - ({})".format(
                drls['dt'].item(row, 0).text(), cortext))
    return names, times, intensities


def get_parentset(ds, drls):
    names = []
    times = np.concatenate([sub['chrom_dat'][0, :] for sub in ds])
    intensities = []
    rowlist = []
    for row in range(drls['dt'].rowCount()):
        if drls['dt'].cellWidget(row, 0).checkState() == 2:
            rowlist.append(row)
            for corcol in range(drls['cors'].value()):
                if drls['dt'].cellWidget(
                        row, corcol*2 + 1).currentIndex() > 0\
                        and floatize(drls['dt'], row, 2) != 0:
                    rowlist.append(
                        drls['dt'].cellWidget(row, 1).currentIndex()-1)
    for row in set(rowlist):
        intensity = get_intensity(row, ds, drls)
        intensities.append(intensity)
        names.append(drls['dt'].item(row, 0).text())
    return names, times, intensities


def gettableitemlist(ptable):
    ion_list = []
    for row in range(ptable.rowCount()):
        text = []
        for i in range(3):
            if not isinstance(ptable.item(row, i), type(None)):
                frg = ptable.item(row, i).text()
            else:
                frg = ""
            text.append(frg)
        line = "{} ({}; fw={})".format(*text)
        ion_list.append(line)
    return ion_list
