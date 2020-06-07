# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'treeview.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_TreeView(object):
    def setupUi(self, TreeView):
        if not TreeView.objectName():
            TreeView.setObjectName(u"TreeView")
        TreeView.resize(1094, 644)
        self.verticalLayout = QVBoxLayout(TreeView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(TreeView)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(5)
        self.fieldtree = QTreeWidget(self.splitter)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.fieldtree.setHeaderItem(__qtreewidgetitem)
        self.fieldtree.setObjectName(u"fieldtree")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fieldtree.sizePolicy().hasHeightForWidth())
        self.fieldtree.setSizePolicy(sizePolicy)
        self.fieldtree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.fieldtree.setStyleSheet(u"QTreeView::item {  padding-right:15px; }")
        self.fieldtree.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.fieldtree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.fieldtree.setUniformRowHeights(True)
        self.fieldtree.setAnimated(True)
        self.splitter.addWidget(self.fieldtree)
        self.fieldtree.header().setVisible(True)
        self.fieldtree.header().setMinimumSectionSize(42)

        self.verticalLayout.addWidget(self.splitter)


        self.retranslateUi(TreeView)
    # setupUi

    def retranslateUi(self, TreeView):
        TreeView.setWindowTitle(QCoreApplication.translate("TreeView", u"Frame", None))
        ___qtreewidgetitem = self.fieldtree.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("TreeView", u"data", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("TreeView", u"name", None));
    # retranslateUi

