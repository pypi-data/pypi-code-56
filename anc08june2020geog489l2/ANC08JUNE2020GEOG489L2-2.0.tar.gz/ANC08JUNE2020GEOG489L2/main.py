####################################################################
# Name: Alexandra Crowe
# Date: 6 June 2020
# Description: This script pulls the widgets created by the
# gui_main.py and the functions and variables from the core_function.py to
# extract features set by parameters selected in the GUI. This is version
# two of Assignment 2 and has been uploaded as a Python Package.
# Install with pip ANC08JUNE2020GEOG489L2.
#####################################################################

import sys, csv

from PyQt5.QtWidgets import QApplication, QMainWindow, QStyle, QFileDialog, QDialog, QMessageBox, QSizePolicy
from PyQt5.QtGui import QStandardItemModel, QStandardItem,  QDoubleValidator, QIntValidator
from PyQt5.QtCore import QVariant
from PyQt5.Qt import Qt

import gui_main
import core_functions


# =======================================
# GUI event handler and related functions
# =======================================

#open file dialog to select exising polygon shapefile
def selectPolygonShapefile():
    fileName, _ = QFileDialog.getOpenFileName(mainWindow,"Select shapefile", "","Shapefile (*.shp)")
    if fileName:
        ui.polygonShapefileLE.setText(fileName)
        updateTargetCountryCB()

#If previous step accepted, update GUI polygon field combo box accordingly
def updatePolygonFieldCB():
    ui.polygonFieldCB.clear()
    polygonShapefile = ui.polygonShapefileLE.text()
    ui.polygonFieldCB.addItems(core_functions.getValidFieldsForShapefile(polygonShapefile))
    ui.targetCountryCB.setEnabled(True)

#update TargetCountryCB combo box with unique values names based on field selection
def updateTargetCountryCB():
    ui.targetCountryCB.clear()
    polygonField = ui.polygonFieldCB.currentText()
    polygonShapefile = ui.polygonShapefileLE.text()
    ui.targetCountryCB.addItems(core_functions.getUniqueValues(polygonShapefile, polygonField))

#open file dialog to select exising point shapefile
def selectPointShapefile():
    fileName, _ = QFileDialog.getOpenFileName(mainWindow,"Select shapefile", "","Shapefile (*.shp)")
    if fileName:
        ui.pointShapefileLE.setText(fileName)
        pointShapefile = ui.pointShapefileLE.text()
        return pointShapefile

#If previous step accepted, enable combo boxes
def showPointFields():
    if ui.shopTypeChB.isChecked():
        ui.pointFieldCB.setEnabled(True)
        ui.shopTypeCB.setEnabled(True)
        updatePointFieldCB()
    else:
        ui.pointFieldCB.setEnabled(False)
        ui.shopTypeCB.setEnabled(False)

#If previous step accepted, update GUI point field combo box accordingly
def updatePointFieldCB():
    ui.pointFieldCB.clear()
    pointShapefile = ui.pointShapefileLE.text()
    ui.pointFieldCB.addItems(core_functions.getValidFieldsForShapefile(pointShapefile))

#update shopTypeCB combo box with unique values names based on field selection
def updateShopTypeCB():
    ui.shopTypeCB.clear()
    pointField = ui.pointFieldCB.currentText()
    pointShapefile = ui.pointShapefileLE.text()
    ui.shopTypeCB.addItems(core_functions.getUniqueValues(pointShapefile, pointField))
    return pointField

#open file dialog to creaete new shapefile and if accepted, update line edit widget accordingly
def selectNewShapefile():
    fileName, _ = QFileDialog.getSaveFileName(mainWindow,"Save new shapefile as", "","Shapefile (*.shp)")
    if fileName:
        ui.newShapefileLE.setText(fileName)

#create new shapefile if enough features match the query terms
def createNewShapefile():
    polygonShapefile = ui.polygonShapefileLE.text()
    pointShapefile = ui.pointShapefileLE.text()
    targetCountry = ui.targetCountryCB.currentText()
    shopType = ui.shopTypeCB.currentText()
    pointField = ui.pointFieldCB.currentText()
    polygonField = ui.polygonFieldCB.currentText()
    countryQuery = polygonField + "='" + targetCountry + "'"
    file = ui.newShapefileLE.text()
    if ui.shopTypeChB.isChecked():
        shopType = ui.shopTypeCB.currentText()
        shopQuery = pointField + "='" + shopType + "'"
    else:
        shopType = " IS NOT NULL"
        shopQuery = pointField + shopType
    ui.statusbar.showMessage('Creating new shapefile of ' + shopType + " shops in " + targetCountry + '...please wait!')
    try:
        core_functions.extractSelectiontoNewShapefile(polygonShapefile, targetCountry, countryQuery, pointShapefile, shopQuery, file)
        count = (core_functions.extractSelectiontoNewShapefile(polygonShapefile, targetCountry, countryQuery, pointShapefile, shopQuery, file))
        print (str(count))
        if count != 0:
            ui.statusbar.showMessage('New shapefile has been created with' + str(count) + ' features.')
        else:
            ui.statusbar.showMessage('No features match this description. Shapefile was not created. Please try again!')
    except Exception as e:
        QMessageBox.information(mainWindow, 'Operation failed', 'Creating new shapefile failed with '+ str(e.__class__) + ': ' + str(e), QMessageBox.Ok )
        ui.statusbar.clearMessage()

#==========================================
# create app and main window + dialog GUI
# =========================================

app = QApplication(sys.argv)

# set up main window
mainWindow = QMainWindow()
ui = gui_main.Ui_MainWindow()
ui.setupUi(mainWindow)
ui.actionExit.setIcon(app.style().standardIcon(QStyle.SP_DialogCancelButton))
ui.polygonShapefileTB.setIcon(app.style().standardIcon(QStyle.SP_DialogOpenButton))
ui.pointShapefileTB.setIcon(app.style().standardIcon(QStyle.SP_DialogOpenButton))


#==========================================
# connect signals
#==========================================

ui.polygonShapefileTB.clicked.connect(selectPolygonShapefile)
ui.polygonShapefileLE.editingFinished.connect(updatePolygonFieldCB)
ui.pointShapefileTB.clicked.connect(selectPointShapefile)
ui.shopTypeChB.clicked.connect(showPointFields)
ui.pointShapefileLE.editingFinished.connect(updateShopTypeCB)
ui.newShapefileTB.clicked.connect(selectNewShapefile)
ui.newShapefilePB.clicked.connect(createNewShapefile)
ui.pointFieldCB.activated.connect(updateShopTypeCB)
ui.polygonFieldCB.activated.connect(updateTargetCountryCB)



#=======================================
# run app
#=======================================

mainWindow.show()
sys.exit(app.exec_())
