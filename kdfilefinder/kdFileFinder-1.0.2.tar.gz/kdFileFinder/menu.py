'''
Created on 2019年3月25日

@author: bkd
'''
from PyQt5.QtWidgets import QAction
from .scriptManager import ScriptManager

# dl_script_manage = ScriptManager()


class toolbar_menu:
    menu_item = [QAction("脚本管理")]

    def __init__(self):
        super().__init__()
        self.dl_script_manage = ScriptManager()

    def handle_action(self, action):
        text = action.text()
        if text == "脚本管理":
            print("脚本管理")
            self.dl_script_manage.exec_()


class file_menu:
    def __init__(self):
        super().__init__()
        self.dl_script_manage = ScriptManager()
        self.menu_item = self.dl_script_manage.get_file_menu_item()

    def get_menu_list(self):
        pass
