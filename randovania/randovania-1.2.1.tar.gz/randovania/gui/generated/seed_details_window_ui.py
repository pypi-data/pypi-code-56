# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/travis/build/randovania/randovania/randovania/gui/ui_files/seed_details_window.ui',
# licensing of '/home/travis/build/randovania/randovania/randovania/gui/ui_files/seed_details_window.ui' applies.
#
# Created: Sat May 30 18:53:44 2020
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SeedDetailsWindow(object):
    def setupUi(self, SeedDetailsWindow):
        SeedDetailsWindow.setObjectName("SeedDetailsWindow")
        SeedDetailsWindow.resize(707, 313)
        self.centralWidget = QtWidgets.QWidget(SeedDetailsWindow)
        self.centralWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layout_info_tab = QtWidgets.QTabWidget(self.centralWidget)
        self.layout_info_tab.setObjectName("layout_info_tab")
        self.details_tab = QtWidgets.QWidget()
        self.details_tab.setObjectName("details_tab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.details_tab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.export_iso_button = QtWidgets.QPushButton(self.details_tab)
        self.export_iso_button.setObjectName("export_iso_button")
        self.gridLayout_3.addWidget(self.export_iso_button, 0, 4, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.faster_credits_check = QtWidgets.QCheckBox(self.details_tab)
        self.faster_credits_check.setObjectName("faster_credits_check")
        self.verticalLayout_4.addWidget(self.faster_credits_check)
        self.remove_hud_popup_check = QtWidgets.QCheckBox(self.details_tab)
        self.remove_hud_popup_check.setObjectName("remove_hud_popup_check")
        self.verticalLayout_4.addWidget(self.remove_hud_popup_check)
        self.open_map_check = QtWidgets.QCheckBox(self.details_tab)
        self.open_map_check.setObjectName("open_map_check")
        self.verticalLayout_4.addWidget(self.open_map_check)
        self.pickup_markers_check = QtWidgets.QCheckBox(self.details_tab)
        self.pickup_markers_check.setObjectName("pickup_markers_check")
        self.verticalLayout_4.addWidget(self.pickup_markers_check)
        self.customize_user_preferences_button = QtWidgets.QPushButton(self.details_tab)
        self.customize_user_preferences_button.setObjectName("customize_user_preferences_button")
        self.verticalLayout_4.addWidget(self.customize_user_preferences_button)
        self.gridLayout_3.addLayout(self.verticalLayout_4, 2, 4, 1, 3)
        self.tool_button = QtWidgets.QToolButton(self.details_tab)
        self.tool_button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.tool_button.setObjectName("tool_button")
        self.gridLayout_3.addWidget(self.tool_button, 0, 6, 1, 1)
        self.export_log_button = QtWidgets.QPushButton(self.details_tab)
        self.export_log_button.setObjectName("export_log_button")
        self.gridLayout_3.addWidget(self.export_log_button, 0, 5, 1, 1)
        self.layout_title_label = QtWidgets.QLabel(self.details_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layout_title_label.sizePolicy().hasHeightForWidth())
        self.layout_title_label.setSizePolicy(sizePolicy)
        self.layout_title_label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.layout_title_label.setObjectName("layout_title_label")
        self.gridLayout_3.addWidget(self.layout_title_label, 0, 0, 1, 4)
        self.layout_description_left_label = QtWidgets.QLabel(self.details_tab)
        self.layout_description_left_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layout_description_left_label.setWordWrap(True)
        self.layout_description_left_label.setObjectName("layout_description_left_label")
        self.gridLayout_3.addWidget(self.layout_description_left_label, 2, 0, 1, 2)
        self.layout_description_right_label = QtWidgets.QLabel(self.details_tab)
        self.layout_description_right_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layout_description_right_label.setWordWrap(True)
        self.layout_description_right_label.setObjectName("layout_description_right_label")
        self.gridLayout_3.addWidget(self.layout_description_right_label, 2, 2, 1, 2)
        self.player_index_combo = QtWidgets.QComboBox(self.details_tab)
        self.player_index_combo.setObjectName("player_index_combo")
        self.gridLayout_3.addWidget(self.player_index_combo, 1, 0, 1, 4)
        self.layout_info_tab.addTab(self.details_tab, "")
        self.pickup_tab = QtWidgets.QWidget()
        self.pickup_tab.setObjectName("pickup_tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.pickup_tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pickup_spoiler_pickup_combobox = QtWidgets.QComboBox(self.pickup_tab)
        self.pickup_spoiler_pickup_combobox.setObjectName("pickup_spoiler_pickup_combobox")
        self.pickup_spoiler_pickup_combobox.addItem("")
        self.gridLayout_2.addWidget(self.pickup_spoiler_pickup_combobox, 2, 2, 1, 1)
        self.pickup_spoiler_label = QtWidgets.QLabel(self.pickup_tab)
        self.pickup_spoiler_label.setObjectName("pickup_spoiler_label")
        self.gridLayout_2.addWidget(self.pickup_spoiler_label, 2, 0, 1, 1)
        self.pickup_spoiler_show_all_button = QtWidgets.QPushButton(self.pickup_tab)
        self.pickup_spoiler_show_all_button.setObjectName("pickup_spoiler_show_all_button")
        self.gridLayout_2.addWidget(self.pickup_spoiler_show_all_button, 2, 1, 1, 1)
        self.pickup_spoiler_scroll_area = QtWidgets.QScrollArea(self.pickup_tab)
        self.pickup_spoiler_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.pickup_spoiler_scroll_area.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.pickup_spoiler_scroll_area.setWidgetResizable(True)
        self.pickup_spoiler_scroll_area.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.pickup_spoiler_scroll_area.setObjectName("pickup_spoiler_scroll_area")
        self.pickup_spoiler_scroll_contents = QtWidgets.QWidget()
        self.pickup_spoiler_scroll_contents.setGeometry(QtCore.QRect(0, 0, 651, 159))
        self.pickup_spoiler_scroll_contents.setObjectName("pickup_spoiler_scroll_contents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.pickup_spoiler_scroll_contents)
        self.verticalLayout_3.setContentsMargins(3, -1, 3, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pickup_spoiler_scroll_content_layout = QtWidgets.QVBoxLayout()
        self.pickup_spoiler_scroll_content_layout.setObjectName("pickup_spoiler_scroll_content_layout")
        self.verticalLayout_3.addLayout(self.pickup_spoiler_scroll_content_layout)
        self.pickup_spoiler_scroll_area.setWidget(self.pickup_spoiler_scroll_contents)
        self.gridLayout_2.addWidget(self.pickup_spoiler_scroll_area, 4, 0, 1, 3)
        self.spoiler_starting_location_label = QtWidgets.QLabel(self.pickup_tab)
        self.spoiler_starting_location_label.setObjectName("spoiler_starting_location_label")
        self.gridLayout_2.addWidget(self.spoiler_starting_location_label, 0, 0, 1, 3)
        self.spoiler_starting_items_label = QtWidgets.QLabel(self.pickup_tab)
        self.spoiler_starting_items_label.setObjectName("spoiler_starting_items_label")
        self.gridLayout_2.addWidget(self.spoiler_starting_items_label, 1, 0, 1, 3)
        self.layout_info_tab.addTab(self.pickup_tab, "")
        self.verticalLayout.addWidget(self.layout_info_tab)
        SeedDetailsWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(SeedDetailsWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 707, 21))
        self.menuBar.setObjectName("menuBar")
        SeedDetailsWindow.setMenuBar(self.menuBar)

        self.retranslateUi(SeedDetailsWindow)
        self.layout_info_tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SeedDetailsWindow)

    def retranslateUi(self, SeedDetailsWindow):
        SeedDetailsWindow.setWindowTitle(QtWidgets.QApplication.translate("SeedDetailsWindow", "Seed Details", None, -1))
        self.export_iso_button.setText(QtWidgets.QApplication.translate("SeedDetailsWindow", "Save ISO", None, -1))
        self.faster_credits_check.setText(QtWidgets.QApplication.translate("SeedDetailsWindow", "Faster Credits", None, -1))
        self.remove_hud_popup_check.setText(QtWidgets.QApplication.translate("SeedDetailsWindow", "Skip Item Acquisition Popups", None, -1))
        self.open_map_check.setText(QtWidgets.QApplication.translate("SeedDetailsWindow", "Open map from start", None, -1))
        self.pickup_markers_check.setText(QtWidgets.QApplication.translate("SeedDetailsWindow", "Replace Translator icons on map with item icons", None, -1))
        self.customize_user_preferences_button.setText(QtWidgets.QApplication.translate("SeedDetailsWindow", "Customize default in-game options", None, -1))
        self.tool_button.setText(QtWidgets.QApplication.translate("SeedDetailsWindow", "...", None, -1))
        self.export_log_button.setText(QtWidgets.QApplication.translate("SeedDetailsWindow", "Save Spoiler", None, -1))
        self.layout_title_label.setText(QtWidgets.QApplication.translate("SeedDetailsWindow", "<html><head/><body><p>Permalink: ????<br/>Seed Hash: ????<br/>Preset Name: ???</p></body></html>", None, -1))
        self.layout_description_left_label.setText(QtWidgets.QApplication.translate("SeedDetailsWindow", "<html><head/><body><p>This content should have been replaced by code.</p></body></html>", None, -1))
        self.layout_description_right_label.setText(QtWidgets.QApplication.translate("SeedDetailsWindow", "<html><head/><body><p>This content should have been replaced by code.</p></body></html>", None, -1))
        self.layout_info_tab.setTabText(self.layout_info_tab.indexOf(self.details_tab), QtWidgets.QApplication.translate("SeedDetailsWindow", "Summary", None, -1))
        self.pickup_spoiler_pickup_combobox.setItemText(0, QtWidgets.QApplication.translate("SeedDetailsWindow", "None", None, -1))
        self.pickup_spoiler_label.setToolTip(QtWidgets.QApplication.translate("SeedDetailsWindow", "Enter text to the right to filter the list below", None, -1))
        self.pickup_spoiler_label.setText(QtWidgets.QApplication.translate("SeedDetailsWindow", "Search Pickup", None, -1))
        self.pickup_spoiler_show_all_button.setText(QtWidgets.QApplication.translate("SeedDetailsWindow", "Show All", None, -1))
        self.spoiler_starting_location_label.setText(QtWidgets.QApplication.translate("SeedDetailsWindow", "Starting Location", None, -1))
        self.spoiler_starting_items_label.setText(QtWidgets.QApplication.translate("SeedDetailsWindow", "Starting Items", None, -1))
        self.layout_info_tab.setTabText(self.layout_info_tab.indexOf(self.pickup_tab), QtWidgets.QApplication.translate("SeedDetailsWindow", "Spoiler: Pickups", None, -1))

