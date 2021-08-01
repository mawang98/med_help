import sys
import os

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

from Ui_editer import *


class EditerWin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_editer()
        self.a = self.ui.setupUi(self)
        self.windowCenter()
        self.iniSet()
        self.sinToslot()

    def windowCenter(self): # 使窗口居中
        screen = QtWidgets.QApplication.desktop()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def iniSet(self):
        self.ui.tableWidget.setColumnWidth(0, 300)  # 设置列宽
        self.ui.tableWidget.setColumnWidth(1, 600)

    def sinToslot(self):
        self.ui.pushButton.clicked.connect(self.addItem)
        self.ui.pushButton_2.clicked.connect(self.removeItem)
        self.ui.pushButton_3.clicked.connect(self.saveItems)

    def addItem(self):

        nowRow = self.ui.tableWidget.currentRow()
        self.ui.tableWidget.insertRow(nowRow + 1)
        pass

    def removeItem(self):
        nowRow = self.ui.tableWidget.currentRow()
        self.ui.tableWidget.removeRow(nowRow)

    def saveItems(self):
        contents =
        a = self.checkBlank()
        print(a)
        if a:



    def checkBlank(self):
        r = self.ui.tableWidget.rowCount()
        if r == 0:
            QtWidgets.QMessageBox.warning(self, '列表内容为空', '内容为空，不需要保存！')
            return(False)
        else:
            noblank = True
            for i in range(r):
                a = self.ui.tableWidget.item(i, 0)
                b = self.ui.tableWidget.item(i, 1)
                if a == None or b == None:
                    noblank = False
                    QtWidgets.QMessageBox.warning(self, '存在空白项目', '请将内容完善后再保存')
                else:
                    if a.text().isspace() or b.text().isspace():#判断是否仅为空格
                        noblank = False
                        QtWidgets.QMessageBox.warning(self, '存在空白项目', '请将内容完善后再保存')
                    else:
                        pass
            return(noblank)



def main():
    app = QtWidgets.QApplication(sys.argv)
    b = EditerWin()
    b.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
