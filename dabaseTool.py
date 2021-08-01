import sqlite3
import datetime

class DatabaseTool():  #表初始化操作
    def __init__(self):
        self.conn = sqlite3.connect('datas.db')
        self.cur = self.conn.cursor()
    def closeDb(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

######## Comments 表操作######################################################################
class CreateTable(DatabaseTool): #创建数据表
    def createTableComments(self):
        sql = '''CREATE TABLE IF NOT EXISTS comment (medicine TEXT PRIMARY KEY, comment TEXT)'''
        self.cur.execute(sql)
        self.closeDb()
class ChangeTableContent(DatabaseTool): #修改数据表内容
    def deleteAll(self):  #全部删除
        sql = 'DELETE FROM comment'
        self.cur.execute(sql)
        self.closeDb()

    def deleteOneData(self, medicine):
        med = medicine
        sql = '''DELETE FROM comment WHERE medicine = '%s' '''%med
        self.cur.execute(sql)
        self.closeDb()

    def insertData(self,data): #插入条目
        sql = 'INSERT INTO comment VALUES(?,?)'
        print(sql,data)
        self.cur.execute(sql,data)
        self.closeDb()
    def update_data(self, medicine, comment):
        medicineA = medicine
        comment_new = comment
        sql = '''UPDATE comment SET comment =? '''+'''WHERE medicine = '%s' '''%medicineA
        self.cur.execute(sql, comment_new)
        self.closeDb()


class  ReadTable(DatabaseTool): #读取数据表内容
    def readTheHead(self): #读取表头
        #读取表头
        sql = 'PRAGMA table_info(comment)'
        self.cur.execute(sql)
        a = self.cur.fetchall()
        return(a)
        self.closeDb()

    def readAllDatas(self): #读取所有数据
        #读取所有数据 并 返回读取结果
        sql = 'SELECT * FROM comment'
        self.cur.execute(sql)
        a = self.cur.fetchall()
        return(a)
        self.closeDb()

    def readDatasWith_medicine_about(self, medicineName):  #模糊检索
        nameA = '%'+medicineName+'%'
        sql ='''SELECT * FROM comment WHERE (medicine LIKE '%s');'''%(nameA)
        #print(sql)
        self.cur.execute(sql)
        a = self.cur.fetchall()
        return(a)
        self.closeDb()
    
    def readDatasWith_medicine_accurate(self,medicineName):  #精确检索
        nameB = medicineName
        sql ='''SELECT * FROM comment WHERE (medicine = '%s') ;'''%(nameB)
        print(sql)
        self.cur.execute(sql)
        a = self.cur.fetchall()
        return(a)
        self.closeDb()
    

