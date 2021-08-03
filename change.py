import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
from Ui_change import *
from dabaseTool import *


class ChangeWin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.a = self.ui.setupUi(self)
        self.windowCenter()
        self.slot_to_sig()

    def windowCenter(self): # 使窗口居中
        screen = QtWidgets.QApplication.desktop()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def slot_to_sig(self):
        self.ui.pushButton.clicked.connect(self.save_change)

    def save_change(self): #保存更新
        a = self.check_blank()
        if not a:
            QtWidgets.QMessageBox.warning(self, '存在空白项目', '请完善空白项目')
        else:
            med = self.ui.label.text()
            com = self.ui.lineEdit.text()
            try:
                b = ChangeTableContent()
                b.update_data(med, com)
                c = QtWidgets.QMessageBox.information(self, '成功更改数据', '已成功更改数据')
            except:
                QtWidgets.QMessageBox.warning(self, '更改数据库错误', '更改数据库内容错误！')
            self.close()

    def check_blank(self): #检查空白项
        a = self.ui.label.text()
        b = self.ui.lineEdit.text()
        if len(a) == 0 or len(b) == 0:
            return(False)
        else:
            if a.isspace() or b.isspace():
                return(False)
            else:
                return(True)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = ChangeWin()
    main.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()