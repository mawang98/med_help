import sys
import os

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

from Ui_main import *
from dabaseTool import *

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        a = self.ui.setupUi(self)
        self.windowCenter()
        self.refresh_list()

    def windowCenter(self): #   使窗口居中
        screen = QtWidgets.QApplication.desktop()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def ini_set(self):
        self.ui.pushButton.clicked.connect(self.refresh_list)
        self.ui.action.clicked.connect()

    def set_comment_win(self):
        pass

    def refresh_list(self):  #更新列表内容
        list_content = []
        try:
            a = ReadTable()
            b = a.readAllDatas()
        except:
            QtWidgets.QMessageBox.warning(self, '数据库读取错误', '数据库读取过程错误！')
        if len(b)==0:
            QtWidgets.QMessageBox.warning(self,'检索数据为空','没有检索到数据，请检查数据库')
        else:
            self.ui.listWidget.clear()
            for i in range(len(b)):
                list_content.append(b[i][0])
                self.ui.listWidget.insertItem(i,b[i][0])
            print(list_content)





def main():
    app = QtWidgets.QApplication(sys.argv)
    mainw = MainWindow()
    mainw.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()