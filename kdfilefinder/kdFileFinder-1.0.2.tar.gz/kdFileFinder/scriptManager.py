'''
Created on 2019年3月25日

@author: bkd
'''
import importlib
import logging
import traceback
from os.path import splitext, dirname
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QAction, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from .fileutil import get_file_realpath
from .customer_script import customer_script
from . import kdconfig

logger = logging.getLogger(__name__)


class ScriptManager:
    show_script_result_signal = pyqtSignal(str)

    def initScriptManager(self):
        super().__init__()
        #loadUi(get_file_realpath("scriptManager.ui"), self)
        self.cs = customer_script()
        self.init_dict()
        logger.info(kdconfig.config_file)

        # 存放脚本的临时变量scriptParam的简写
        self.sp = {}

    def init_dict(self):
        self.script_dict = kdconfig.init_dict("script", "customer_script")
        logger.info(self.script_dict)
        sc_items = self.script_dict.items()
        logger.info(sc_items)
        # for sc in sc_items:
        #list_item = QListWidgetItem(sc[0])
        #list_item.setData(-1, sc[1])
        # self.lv_script.addItem(list_item)
        # self.lv_script.itemDoubleClicked.connect(
        # self.on_lv_script_itemDoubleClicked)

    # @pyqtSlot()
    # def on_pb_add_script_clicked(self):
        #reply = self.cs.exec_()
        # if reply:
        # logger.info(self.cs.bg_apply_type.checkedButton().text())
        # self.script_dict[self.cs.le_name.text()] = {"path": self.cs.le_path.text(
        # ), "apply_type": self.cs.bg_apply_type.checkedButton().apply_type, "filetype": self.cs.le_filetype.text()}
        #kdconfig.dict_add("script", "customer_script", self.script_dict)
        # logger.info(self.script_dict)

    # @pyqtSlot()
    # def on_lv_script_itemDoubleClicked(self):
        #cur_item = self.lv_script.currentItem()
        #script = cur_item.data(-1)
        #script["name"] = cur_item.text()
        # self.cs.edit(script)
        # self.on_pb_add_script_clicked()

    def loadPlugin(self, filename, filePath, fileList):
        logger.info("loading plugin:" + 'kdFileFinder.script.' +
                    splitext(filename)[0])
#         plugin=__import__(get_file_realpath("script/"+filename), fromlist=[filename],level=0)

        script_module = importlib.import_module(
            'kdFileFinder.script.' + splitext(filename)[0])
        script_class = getattr(script_module, splitext(filename)[0])
#         plugin=__import__("menu")
#         clazz=plugin.getPluginClass()
        o = script_class()
#         o.setFather(self, self.kdpad)
        self.sp["path"] = filePath
        self.sp["fileList"] = fileList
        try:
            o.execute(self, self.sp)
        except Exception as e:
            logger.error("插件运行异常:" + traceback.format_exc())
            QMessageBox.information(self, "系统异常", str(e), QMessageBox.Ok)
#         if self.script_variable["script_result_body"] :
        logger.info("sp:", self.sp)
#             QMessageBox.information(self,"粘贴文件",self.script_variable["script_result_body"])
#             self.show_script_result_signal.emit(self.script_variable["statusbar_msg"])

    def get_file_menu_item(self):
        sc_items = self.script_dict.items()
        # logger.info(sc_items)
        actions = []
        for index in sorted(self.script_dict):
            sc = self.script_dict[index]
            # logger.info(index)
            # logger.info(sc)
            if sc["apply_type"] == 1:
                action = QAction(index)
                actions.append(action)
        return actions

    def run_script(self, script_name, filePath, fileList):
        scriptPath = self.script_dict[script_name]["path"]
        logger.info("脚本路径：" + scriptPath)
        self.loadPlugin(scriptPath, filePath, fileList)
