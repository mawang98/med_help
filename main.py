import sys
import os
import datetime

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

from Ui_main import *
from dabaseTool import *
from editer import *
from about import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        a = self.ui.setupUi(self)
        self.windowCenter()
        self.check_db_file()
        self.ini_set()
        self.refresh_list()

    def windowCenter(self): #   使窗口居中
        screen = QtWidgets.QApplication.desktop()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def ini_set(self): #初始设置
        self.ui.pushButton.clicked.connect(self.refresh_list)
        self.ui.action.triggered.connect(self.set_comment_win)
        self.ui.action_2.triggered.connect(self.show_about_win)
        self.ui.listWidget.itemClicked.connect(self.label_show_comment)
        self.ui.listWidget.currentRowChanged.connect(self.label_show_comment)
        self.ui.listWidget.itemDoubleClicked.connect(self.write_to_textmanager)
        self.ui.pushButton_3.clicked.connect(self.ui.textEdit.clear)
        self.ui.pushButton_4.clicked.connect(self.delete_blank)
        self.ui.pushButton_2.clicked.connect(self.save_to_txt)

    def check_db_file(self):  #检查数据库文件datas.db是否正常
        find_db = 0
        for fileName in os.listdir():
            if fileName == 'datas.db':
                find_db = 1
                print('数据库文件正常')
            else:
                pass
        if find_db == 0:
            QtWidgets.QMessageBox.warning(self, '缺少数据库文件', '缺少数据库文件')
        else:
            pass

    def set_comment_win(self): #菜单栏调取模板设置窗口
        self.ed_win = EditerWin()
        self.ed_win.show()

    def show_about_win(self):
        self.ab_win = AboutWin()
        self.ab_win.show()

    def label_show_comment(self): #在标签中显示条目和内容
        if self.ui.listWidget.currentRow() == -1:
            self.ui.label.clear()
            self.ui.label_2.clear()
        else:
            med_now = self.ui.listWidget.currentItem().text()
            # print(med_now)
            self.ui.label.clear()
            self.ui.label.setText(med_now)
            try:
                a = ReadTable()
                b = a.readDatasWith_medicine_accurate(med_now)
            except:
                QtWidgets.QMessageBox.warning(self, '数据库读取错误', '数据库读取错误！')
            self.ui.label_2.clear()
            self.ui.label_2.setText(b[0][1])

    def write_to_textmanager(self): #将当前cmment内容分行写入textEdit
        a = self.ui.label_2.text()
        if a[-1] in (',?.;!，。？；！'): #删除末尾标点符号
            b = a[0:-1]
            # print(b)
        else:
            b = a
            # print(b)
        self.ui.textEdit.append(b+'；')

    def delete_blank(self): #删除文本中的空白
        a = self.ui.textEdit.toPlainText()
        # print(a)
        b = a.replace('\n', '')
        # print(b)
        self.ui.textEdit.setText(b)


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
            # print(list_content)

    def save_to_txt(self): #将textEdit中的文本保存成txt文件
        now_text = self.ui.textEdit.toPlainText()
        now_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = QtWidgets.QFileDialog.getSaveFileName(self, '保存文件', '医保说明'+'_%s'%now_datetime,'txt files(*.txt)')
        # print(file_path)
        try:
            file = open(file_path[0]+'.txt', 'w')
            file.write(now_text)
            file.close()
        except:
            QtWidgets.QMessageBox.warning(self, '保存文件错误', '文件保存错误！')

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainw = MainWindow()
    mainw.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()