import sys
import os

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QAbstractItemView

from Ui_editer import *
from dabaseTool import *
from change import *


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
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) #设置以行为单位选择
        self.ui.tableWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection) #设置单行选择
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers) #设置不可编辑
        self.refreshTable()

    def sinToslot(self):
        self.ui.pushButton.clicked.connect(self.saveItems)
        self.ui.pushButton_2.clicked.connect(self.removeItem)
        self.ui.tableWidget.itemDoubleClicked.connect(self.changeContentWin)

    def removeItem(self):  #已有条目删除
        que = QtWidgets.QMessageBox.warning(self,
                                             '确认删除',
                                             '是否确认删除此条目？',
                                             QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)
        if que == QtWidgets.QMessageBox.Ok:
            nowRow = self.ui.tableWidget.currentRow()
            a = self.ui.tableWidget.item(nowRow, 0).text()
            b = ChangeTableContent()
            c = b.deleteOneData(a)
            self.ui.tableWidget.removeRow(nowRow)
            self.refreshTable()
            QtWidgets.QMessageBox.information(self, '删除成功', '条目删除成功！')
        else:
            pass

    def refreshTable(self): #刷新表格内容
        try:
            a = ReadTable()
            b = a.readAllDatas()
        except:
            QtWidgets.QMessageBox.warning(self,'数据库读取错误', '数据库读取错误！')
        if len(b) == 0:
            QtWidgets.QMessageBox.warning(self, '读取数据为空', '数据库内容为空！')
        else:
            self.ui.tableWidget.setRowCount(0)
            for i in range(len(b)):
                c = QtWidgets.QTableWidgetItem(b[i][0])
                d = QtWidgets.QTableWidgetItem(b[i][1])
                rows = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(rows)
                self.ui.tableWidget.setItem(i,0,c)
                self.ui.tableWidget.setItem(i,1,d)

    def saveItems(self):
        notBlank = self.checkBlank()
        if notBlank == False:
            QtWidgets.QMessageBox.warning(self, '存在项目空白', '请完整填写项目后保存')
        else:
            notDuplicate = self.checkDuplicate()
            if notDuplicate == False:
                QtWidgets.QMessageBox.warning(self, '数据重复', '要保存的项目已存在！')
            else:
                medcine = self.ui.lineEdit.text()
                comment = self.ui.lineEdit_2.text()
                dataToSave = (medcine,comment)
                # print(dataToSave)
                ques = QtWidgets.QMessageBox.question(self,
                                                      '请确认保存数据', '是否要增加并保存项目？',
                                                      QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel
                                                      )
                if ques == QtWidgets.QMessageBox.Ok:
                    print('ok')
                    try: #向数据库保存数据
                        a = ChangeTableContent()
                        a.insertData(dataToSave)
                        self.refreshTable()
                        QtWidgets.QMessageBox.information(self,
                                                          '数据保存成功',
                                                          '已成功保存数据！')
                    except:
                        QtWidgets.QMessageBox.warning(self,
                                                      '保存数据错误',
                                                      '向数据库保存数据错误，请检查数据库连接')
                else:
                    pass

    def checkBlank(self):  #检查空白项
        a = self.ui.lineEdit.text()
        b = self.ui.lineEdit_2.text()
        # print(type(a),type(b),a,b,len(a),len(b))
        if len(a) == 0 or len(b) == 0:
            return(False)
        else:
            if a.isspace() or b.isspace():
                return(False)
            else:
                return(True)

    def checkDuplicate(self):  #检查重复项目
        a = self.ui.lineEdit.text()
        b = ReadTable()
        try:
            c = b.readDatasWith_medicine_accurate(a)
            if len(c) != 0:
                return (False)
            else:
                return (True)
        except:
            QtWidgets.QMessageBox.warning(self,'数据库错误', '数据库检索错误！')

    def changeContentWin(self):
        cur_row = self.ui.tableWidget.currentRow()
        now_med = self.ui.tableWidget.item(cur_row, 0).text()
        now_comment = self.ui.tableWidget.item(cur_row, 1).text()
        self.change = ChangeWin()
        self.change.show()
        self.change.ui.label.setText(now_med)
        self.change.ui.lineEdit.setText(now_comment)

def main():
    app = QtWidgets.QApplication(sys.argv)
    b = EditerWin()
    b.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
