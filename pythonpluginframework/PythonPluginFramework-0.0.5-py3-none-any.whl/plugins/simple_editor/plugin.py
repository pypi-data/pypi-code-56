

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


context = None
def init(context_):
    global context
    context = context_


class SimpleEditorWidget(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.selAllShort = QShortcut(QKeySequence("Ctrl+s"), self)
        self.selAllShort.activated.connect(self.on_save)

    def on_init(self, node):
        self._node = node
        value = node.get_prop('key2')
        self.setText(value)
        print("on_init:", value)
        return ""
    def on_save(self):
        value = self.toPlainText()
        self._node.set_prop('key2', value)
        print("on_save:", value)
        return ""
    def on_close(self):
        print("on close...")
        return ""

class EditorExtension:
    def data_kind(self):
        return ['Group']
    def is_match_data(self, node):
        if node.get_kind() == 'Group':
            return True
        else:
            return False
    def create_editor(self, parent):
        return SimpleEditorWidget(parent)


config = {
    "extensions" : [
        {
            "name": "PL::Basic::Editor",
            "impl": EditorExtension()
        }
    ]
}