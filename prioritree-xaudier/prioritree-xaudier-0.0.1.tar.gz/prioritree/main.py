import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from forms import NewTaskForm
import numpy as np
import json
import os
import io
import time


DATA_FILE = os.path.abspath("./data.json")
DATA_TYPE ={"Title":"text", "Description":"text", "Urgency":"int", "Importance":"int", "Priority":"int"}
COLUMN_NAMES = [k for k in DATA_TYPE.keys()]
DEFAULT_DATA = ["Title", "Description", "100", "100", "100"]

    
def adjusted_color(val):
    value = int(val)
    value = int(255 * (min(100, value) / 100)**2)
    return QtGui.QColor(value, 0, 0, value)

def nbRows(model, item_idx):
    nb_rows = model.rowCount(item_idx)
    for row in range(model.rowCount(item_idx)):
        nb_rows += nbRows(model, model.index(row, 0, item_idx))
    return nb_rows

def openNewTaskForm():
    form = NewTaskForm()
    ret = form.exec()
    val = {}
    if ret == QtWidgets.QDialog.Accepted:
        val = form.sendDataBack()
    return val

class TaskModel(QtGui.QStandardItemModel):
    def __init__(self, *args, **kwargs):
        super(TaskModel, self).__init__(*args, **kwargs)
        self.setHorizontalHeaderLabels(COLUMN_NAMES)


    def deleteTasks(self, selection_model):
        selectedRowsIdx = selection_model.selectedRows()
        if not selectedRowsIdx:
            return

        for index in selectedRowsIdx:
            if index.isValid():
                # self.beginRemoveRows(index.parent(), index.row(), index.row())
                self.removeRow(index.row(), index.parent())
                # self.endRemoveRows()

    def rowCountRecursive(self, parent=QtCore.QModelIndex()):
        nb_rows = self.rowCount(parent=parent)
        children_nb_rows_rec = [1 + self.rowCountRecursive(parent=self.index(row, 0, parent)) for row in range(nb_rows)]
        return int(np.sum(children_nb_rows_rec))

    def rowAboveRecursive(self, parent=QtCore.QModelIndex()):
        if not parent.isValid():
            return -1
            
        row_above_parent = 1 + self.rowAboveRecursive(parent=parent.parent())
        siblings_nb_rows_rec = [1 + self.rowCountRecursive(parent=parent.siblingAtRow(row)) for row in range(parent.row())]
        return int(np.sum(siblings_nb_rows_rec) + row_above_parent)

    def rowNumberIndex(self, row_number=0, parent=QtCore.QModelIndex()):
        nb_rows = self.rowCount(parent=parent)

        if not nb_rows:
            return parent

        children_nb_rows_rec = [1 + self.rowCountRecursive(parent=self.index(row, 0, parent)) for row in range(nb_rows)]
        for child_nb, nb_rows in enumerate(children_nb_rows_rec):
            if row_number==0:
                return self.index(child_nb, 0, parent)
            elif row_number < nb_rows:
                return self.rowNumberIndex(row_number=row_number-1, parent=self.index(child_nb, 0, parent))
            else:
                row_number -= nb_rows

        return QtCore.QModelIndex()

    def rowIndices(self, parent=QtCore.QModelIndex()):
        nb_rows = self.rowCount(parent=parent)

        if parent.isValid():
            indexList = [parent]
        else:
            indexList = []

        if not nb_rows:
            return indexList

        for row in range(nb_rows):
            row_idx = self.index(row, 0, parent)
            childrenList = self.rowIndices(parent=row_idx)
            for index in childrenList:
                indexList.append(index)
        return indexList

    def createNewTask(self, selection_model):
        data_dict = openNewTaskForm()
        if not data_dict:
            return

        selectedRowsIdx = selection_model.selectedRows()
        if not selectedRowsIdx:
            index = QtCore.QModelIndex()
        else:
            index = selectedRowsIdx[0]

        itemList = [QtGui.QStandardItem(data_dict[key]) for key in COLUMN_NAMES]
        self.insertRow(0, itemList)

    def data(self, index, role):
        column = index.column()
        background_columns = [COLUMN_NAMES.index(tag) for tag in ["Urgency", "Importance", "Priority"]]
        if column in background_columns and role in [QtCore.Qt.BackgroundColorRole]:
            value = self.data(index, QtCore.Qt.DisplayRole)
            return QtGui.QBrush(adjusted_color(value))
        elif column ==  COLUMN_NAMES.index("Priority") and role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
            return self.priority(index)
        else:
            return super(TaskModel, self).data(index, role)

    def priority(self, index):
        urgency = super(TaskModel, self).data(index.siblingAtColumn(COLUMN_NAMES.index("Urgency")), QtCore.Qt.DisplayRole)
        importance = super(TaskModel, self).data(index.siblingAtColumn(COLUMN_NAMES.index("Importance")), QtCore.Qt.DisplayRole)
        if not urgency:
            urgency = 0
        else:
            urgency = int(urgency)
        if not importance:
            importance = 0
        else:
            importance = int(importance)
        priority = str(int(np.sqrt(urgency * importance)))
        return priority

    def rowToDict(self, item_idx=QtCore.QModelIndex(), header_list=None, recursive=True):
        if not header_list:
            header_list = [self.headerData(section, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole) for section in range(self.columnCount(item_idx))]

        data_dict = {}
        for column, key in enumerate(header_list):
            data_dict[key] = str(self.data(item_idx.siblingAtColumn(column), QtCore.Qt.DisplayRole))

        data_dict["Children"] = str(self.rowCount(item_idx))

        if recursive and self.rowCount(item_idx):
            for row in range(self.rowCount(item_idx)):
                data_dict["Child_{}".format(row)] = self.rowToDict(self.index(row, 0, item_idx), header_list=header_list, recursive=True)

        return data_dict

    def dictToItem(self, data_dict={}, header_list=None, recursive=True):
        if not data_dict:
            return QtGui.QStandardItem()
        if not header_list:
            header_list = [self.headerData(section, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole) for section in range(self.columnCount())]
        
        nb_rows = int(data_dict["Children"])
        nb_columns = len(header_list)

        parentItem = QtGui.QStandardItem(nb_rows, nb_columns)
        for row in range(nb_rows):
            child_data_dict = data_dict["Child_{}".format(row)]
            parentItem.setChild(row, self.dictToItem(child_data_dict, header_list=header_list, recursive=True))

        return parentItem
      
    def fillData(self, data_dict={}, parent_index=QtCore.QModelIndex(), header_list=None, recursive=True):
        if not data_dict:
            return 
        if not header_list:
            header_list = [self.headerData(section, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole) for section in range(self.columnCount())]
        if not parent_index.isValid():
            parent_index = self.indexFromItem(self.invisibleRootItem())
        
        nb_columns = len(header_list)
        for col, key in enumerate(COLUMN_NAMES):
            val = data_dict[key]
            child_idx = parent_index.siblingAtColumn(col)
            self.setData(child_idx, val, QtCore.Qt.DisplayRole)
            self.dataChanged.emit(child_idx, child_idx, [QtCore.Qt.DisplayRole])

        if not recursive:
            return True

        nb_rows = int(data_dict["Children"])
        for row in range(nb_rows):
            child_data_dict = data_dict["Child_{}".format(row)]
            child_idx = self.index(row, 0, parent_index)
            self.fillData(data_dict=child_data_dict, parent_index=child_idx, header_list=header_list, recursive=recursive)
            self.dataChanged.emit(child_idx, child_idx, [QtCore.Qt.DisplayRole])

        return True


    def saveData(self):
        data_dict = self.rowToDict()
        
        with open(DATA_FILE, 'w') as f:
            json.dump(data_dict,f, indent=4)

    def setupData(self):
        if not os.path.exists(DATA_FILE):
            return

        with open(DATA_FILE, 'r') as f:
            data_dict = json.load(f)
        
        if not data_dict or not self.invisibleRootItem():
            return

        nb_rows = int(data_dict["Children"])
        for row in range(nb_rows):
            child_data_dict = data_dict["Child_{}".format(row)]
            self.appendRow(self.dictToItem(child_data_dict, recursive=True))

        self.fillData(data_dict=data_dict)
        self.beginResetModel()

    def flags(self, index):
        baseFlags =  super(TaskModel, self).flags(index)
        default_flags =  QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        return baseFlags | default_flags


class TableAdapterModel(QtCore.QAbstractItemModel):
    def __init__(self, *args, **kwargs):
        super(TableAdapterModel, self).__init__(*args, **kwargs)
        self.sourceModel = None
        self.rowIndices = []

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.sourceModel.invisibleRootItem()
        else:
            parentItem = parent.internalPointer()

        childItem = self.rowIndices[row].siblingAtColumn(column)
        if childItem:
            return self.createIndex(row, column, childItem.internalPointer())
        return QtCore.QModelIndex()
    
    def resetRows(self):
        self.rowIndices = self.sourceModel.rowIndices()
        
    def parent(self, index):
        return QtCore.QModelIndex()

    # def deleteTasks(self, selection_model):
    #     selectedRowsIdx = selection_model.selectedRows()
    #     if not selectedRowsIdx:
    #         return

    #     print(selectedRowsIdx)

    #     # sourceRowsIdx = self.mapSelectionToSource()

    #     for index in selectedRowsIdx:
    #         if index.isValid():
    #             # self.beginRemoveRows(index.parent(), index.row(), index.row())
    #             print("valid index")
    #             self.removeRow(index.row(), index.parent())
    #             # self.endRemoveRows()

    def setSourceModel(self, model):
        self.sourceModel = model
        self.sourceModel.rowsInserted.connect(self.resetRows)
        self.sourceModel.rowsMoved.connect(self.resetRows)
        self.sourceModel.rowsRemoved.connect(self.resetRows)
        self.resetRows()

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Vertical:
            if role==QtCore.Qt.DisplayRole:
                # return QtCore.QVariant(str(section))
                return QtCore.QVariant()
            else:
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Horizontal:
            return self.sourceModel.headerData(section, orientation, role)
        else:
            return None

    def sort(self, column, order):
        self.resetRows()
        values = list(self.sourceModel.data(index.siblingAtColumn(column), QtCore.Qt.DisplayRole) for index in self.rowIndices)
        if column in [COLUMN_NAMES.index(tag) for tag in ["Urgency", "Importance", "Priority"]]:
            values = list(map(np.int, values))
            orderedIndices = [self.rowIndices[int(i)] for i in np.argsort(values)]
        else:
            orderedIndices = [self.rowIndices[int(i)] for i in np.lexsort((values,))]

        if order==QtCore.Qt.DescendingOrder:
            orderedIndices.reverse()
        self.rowIndices = orderedIndices
        self.layoutChanged.emit()

    def columnCount(self, parent_index):
        return self.sourceModel.columnCount(parent_index)
            
    def rowCount(self, parent_index):
        if parent_index.isValid():
            return 0
        else:
            return len(self.rowIndices)

    def mapFromSourceModel(self, sourceIndex):
        if sourceIndex in self.rowIndices:
            row_nb = self.rowIndices.index(sourceIndex)
            return self.index(row_nb, sourceIndex.column(), QtCore.QModelIndex())
        else:
            return QtCore.QModelIndex()

    def mapToSourceModel(self, proxyIndex):
        return self.rowIndices[proxyIndex.row()].siblingAtColumn(proxyIndex.column())

    def data(self, index, role):
        sourceIndex = self.mapToSourceModel(index)
        return self.sourceModel.data(sourceIndex, role)

    def setData(self, index, value, role):
        sourceIndex = self.mapToSourceModel(index)
        return self.sourceModel.setData(sourceIndex, value, role)

    def flags(self, index):
        sourceIndex = self.mapToSourceModel(index)
        # print("flags")
        default_flags =  QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        return self.sourceModel.flags(sourceIndex) | default_flags

class PriorityDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, *args, **kwargs):
        super(PriorityDelegate, self).__init__(*args, **kwargs)

    def sizeHint(self, option, index):
        return QtCore.QSize(20, 20)

    def paint(self, painter, option, index):
        super(PriorityDelegate, self).paint(painter, option, index)

    def createEditor(self, parent, option, index): 
        editor = QtWidgets.QSpinBox(parent)
        editor.setMinimum(0)
        editor.setMaximum(100)
        return editor

    def setEditorData(self, editor, index):
        super(PriorityDelegate, self).setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        super(PriorityDelegate, self).setModelData(editor, model, index)
        color = adjusted_color(editor.value())
        model.setData(index, QtGui.QBrush(color), QtCore.Qt.BackgroundRole)


class SelectionModelAdapter(QtCore.QObject):
    def __init__(self, *args, **kwargs):
        self.treeSelectionModel = None
        self.tableSelectionModel = None
        self.tableAdapterModel = None
        super(SelectionModelAdapter, self).__init__(*args, **kwargs)

    def setSelectionModels(self, treeSelectionModel, tableSelectionModel, tableAdapterModel):
        self.treeSelectionModel = treeSelectionModel
        self.tableSelectionModel = tableSelectionModel
        self.tableAdapterModel = tableAdapterModel

    def connectSignals(self):
        if not self.treeSelectionModel or not self.tableSelectionModel or not self.tableAdapterModel:
            return

        self.tableSelectionModel.currentChanged.connect(self.setCurrrentTreeSelectionFromTableSelection)
        self.treeSelectionModel.currentChanged.connect(self.setCurrrentTableSelectionFromTreeSelection)
        # void 	currentColumnChanged(const QModelIndex &current, const QModelIndex &previous)
        # void 	currentRowChanged(const QModelIndex &current, const QModelIndex &previous)
        # void 	modelChanged(QAbstractItemModel *model)
        # void 	selectionChanged(const QItemSelection &selected, const QItemSelection &deselected)
        
    def setCurrrentTreeSelectionFromTableSelection(self, current, previous):
        sourceIndex = self.tableAdapterModel.mapToSourceModel(current)
        self.treeSelectionModel.setCurrentIndex(sourceIndex, QtCore.QItemSelectionModel.SelectCurrent | QtCore.QItemSelectionModel.Rows)

    def setCurrrentTableSelectionFromTreeSelection(self, current, previous):
        sourceIndex = self.tableAdapterModel.mapFromSourceModel(current)
        self.tableSelectionModel.setCurrentIndex(sourceIndex, QtCore.QItemSelectionModel.SelectCurrent | QtCore.QItemSelectionModel.Rows)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    mainWindow = QtWidgets.QMainWindow()
    mainWindow.resize(1600, 900)

    model = TaskModel(mainWindow)
    model.setupData()

    centralwidget = QtWidgets.QWidget(mainWindow)
    horizontalLayout = QtWidgets.QHBoxLayout(centralwidget)

    priorityDelegate = PriorityDelegate(mainWindow)

    # priorityTreeProxy = PriorityTreeProxy(mainWindow)
    # priorityTreeProxy.setSourceModel(model)
    # priorityTreeProxy.setRecursiveFilteringEnabled(True)

    treeView = QtWidgets.QTreeView(centralwidget)
    treeView.setSortingEnabled(True)
    treeView.setModel(model)
    treeView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
    treeView.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
    treeView.setDefaultDropAction(QtCore.Qt.MoveAction)
    treeView.setDragDropOverwriteMode(False)
    treeView.setAcceptDrops(True)
    treeView.setDropIndicatorShown(True)
    # treeView.setAutoExpandDelay(0.5)
    treeView.setDragEnabled(True)
    treeView.expandAll()
    treeView.setColumnWidth(0, 250)
    for key, val in DATA_TYPE.items():
        if val == "int":
            treeView.setItemDelegateForColumn(COLUMN_NAMES.index(key), priorityDelegate)
    horizontalLayout.addWidget(treeView)

    tableAdapterModel = TableAdapterModel(mainWindow)
    tableAdapterModel.setSourceModel(model)

    # priorityTableProxy = PriorityTableProxy(mainWindow)
    # priorityTableProxy.setSourceModel(model)
    # priorityTableProxy.setRecursiveFilteringEnabled(True)

    tableView = QtWidgets.QTableView(centralwidget)
    tableView.setModel(tableAdapterModel)
    tableView.setSortingEnabled(True)
    tableView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
    tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    tableView.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
    tableView.setColumnWidth(0, 400)
    tableView.setColumnWidth(1, 300)
    tableView.setColumnWidth(2, 50)
    tableView.setColumnWidth(3, 50)
    tableView.setColumnWidth(4, 50)
    for key, val in DATA_TYPE.items():
        if val == "int":
            tableView.setItemDelegateForColumn(COLUMN_NAMES.index(key), priorityDelegate)
        # if key in ["Urgency", "Importance"]:
        #     tableView.setColumnHidden(COLUMN_NAMES.index(key), True)
        
    itemSelectionAdapter = SelectionModelAdapter()
    itemSelectionAdapter.setSelectionModels(treeView.selectionModel(), tableView.selectionModel(), tableAdapterModel)
    itemSelectionAdapter.connectSignals()    


    horizontalLayout.addWidget(tableView)

    mainWindow.setCentralWidget(centralwidget)

    menubar = QtWidgets.QMenuBar(mainWindow)
    menubar.setGeometry(QtCore.QRect(0, 0, 1055, 21))
    menuFile = QtWidgets.QMenu(menubar)
    menuFile.setTitle("File")
    
    statusbar = QtWidgets.QStatusBar(mainWindow)

    actionDelete = QtWidgets.QAction(mainWindow)
    actionDelete.setText("Delete Task(s)")
    actionDelete.setShortcut(QtGui.QKeySequence.Delete)
    actionNew = QtWidgets.QAction(mainWindow)
    actionNew.setText("New Task")
    actionNew.setShortcut("Ctrl+N")
    actionExpandAll = QtWidgets.QAction(mainWindow)
    actionExpandAll.setText("Expand All")
    actionExpandAll.setShortcut("Ctrl+Space")
    actionSave_All = QtWidgets.QAction(mainWindow)
    actionSave_All.setText("Save All")
    actionSave_All.setShortcut("Ctrl+S")
    actionSaveQuit = QtWidgets.QAction(mainWindow)
    actionSaveQuit.setText("Save & Quit")
    actionSaveQuit.setShortcut("Ctrl+Q")
    actionQuit = QtWidgets.QAction(mainWindow)
    actionQuit.setText("Exit")
    actionImport_Data = QtWidgets.QAction(mainWindow)
    actionImport_Data.setText("Import Data")
    actionImport_Data.setShortcut("Ctrl+I")

    menuFile.addAction(actionDelete)
    menuFile.addAction(actionNew)
    menuFile.addAction(actionExpandAll)
    menuFile.addAction(actionImport_Data)
    menuFile.addAction(actionSave_All)
    menuFile.addAction(actionSaveQuit)
    menuFile.addAction(actionQuit)
    
    menubar.addAction(menuFile.menuAction())

    mainWindow.setMenuBar(menubar)
    mainWindow.setStatusBar(statusbar)

    actionDelete.triggered.connect(lambda x: model.deleteTasks(treeView.selectionModel()))
    # actionDelete.triggered.connect(tableView.layou)
    # actionDelete.triggered.connect(lambda x: tableAdapterModel.deleteTasks(tableView.selectionModel()))
    actionNew.triggered.connect(lambda x: model.createNewTask(treeView.selectionModel()))
    actionExpandAll.triggered.connect(treeView.expandAll)
    # actionImport_Data.triggered.connect(tableAdapterModel.resetRows)
    actionSave_All.triggered.connect(model.saveData)
    actionSaveQuit.triggered.connect(model.saveData)
    actionSaveQuit.triggered.connect(mainWindow.close)
    actionQuit.triggered.connect(mainWindow.close)
    
    mainWindow.setWindowTitle("Simple Tree Model")

    # print(model.rowIndices())
    # for idx in model.rowIndices():
    #     print(model.rowAboveRecursive(parent=idx))
    #     print(model.data(idx, QtCore.Qt.DisplayRole))
    # print(len(model.rowIndices()))

    tableView.sortByColumn(COLUMN_NAMES.index("Priority"), QtCore.Qt.DescendingOrder)
    mainWindow.showMaximized()

    sys.exit(app.exec_())




