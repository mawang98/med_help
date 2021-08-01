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
class CreateTable(DatabaseTool):
    def createTableComments(self):
        sql = '''CREATE TABLE IF NOT EXISTS comment (medicine TEXT PRIMARY KEY, comment TEXT)'''
        self.cur.execute(sql)
        self.closeDb()
class ChangeTableContent(DatabaseTool):
    def deleteAll(self):
        sql = 'DELETE FROM comment'
        self.cur.execute(sql)
        self.closeDb()
    def refreshComment(self,values):  #values为字典{'药物名称'：'医保说明'}
        a = tuple(dict.items(values))
        sql = 'INSERT INTO comment VALUES '
        sql2 = sql+str(a)[1:-1]
        print(sql2)
        self.cur.execute(sql2)
        self.closeDb()

class  InsertDatas(DatabaseTool):
    def insertData(self,patientData):#数据为元祖
        data = patientData
        #print(data)
        sql = 'INSERT INTO discharge VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        self.cur.execute(sql,data)
        self.closeDb()

class  ReadTable(DatabaseTool):
    def readTheHead(self):
        #读取表头
        sql = 'PRAGMA table_info(discharge)'
        self.cur.execute(sql)
        a = self.cur.fetchall()
        return(a)
        self.closeDb()

    def readAllDatas(self):
        #读取所有数据 并 返回读取结果
        sql = 'SELECT * FROM discharge'
        self.cur.execute(sql)
        a = self.cur.fetchall()
        return(a)
        self.closeDb()

    def readDatasInDate(self,Interval=30):
        #读取30天内的患者信息
        sql = 'SELECT * FROM discharge Where(checkoutDate BETWEEN ? AND ?)'
        fromTime = (datetime.datetime.now()-datetime.timedelta(days=Interval)).strftime('%Y-%m-%d')
        toTime = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        self.cur.execute(sql,(fromTime,toTime))
        a = self.cur.fetchall()
        return(a)
        self.closeDb()       

    def readDatasWithName(self,name,fromTime,toTime):
        nameA = '%'+name+'%'
        fromTimeA = fromTime
        toTimeA = toTime
        sql ='''SELECT * FROM discharge WHERE (name LIKE '%s') AND (checkoutDate BETWEEN '%s' AND '%s');'''%(nameA,fromTimeA,toTimeA)
        #print(sql)
        self.cur.execute(sql)
        a = self.cur.fetchall()
        return(a)
        self.closeDb()
    
    def readDatasWithAdmnum(self,admNUm,fromTime,toTime):
        admNUmA = admNUm
        fromTimeA = fromTime
        toTimeA = toTime
        sql ='''SELECT * FROM discharge WHERE (admNum = %s) AND (checkoutDate BETWEEN '%s' AND '%s');'''%(admNUmA,fromTimeA,toTimeA)
        #print(sql)
        self.cur.execute(sql)
        a = self.cur.fetchall()
        return(a)
        self.closeDb()
    
    def readDatasWithDiag(self,diagnosis,fromTime,toTime):
        diagnosisA = '%'+diagnosis+'%'
        fromTimeA = fromTime
        toTimeA = toTime
        sql ='''SELECT * FROM discharge WHERE (diagnosis LIKE '%s') AND (checkoutDate BETWEEN '%s' AND '%s');'''%(diagnosisA,fromTimeA,toTimeA)
        #print(sql)
        self.cur.execute(sql)
        a = self.cur.fetchall()
        return(a)
        self.closeDb()
    def readDatasWithIcunum(self,icuNum):
        icuNumA = icuNum
        sql ='''SELECT * FROM discharge WHERE (icuNum = %s) ;'''%(icuNumA)
        #print(sql)
        self.cur.execute(sql)
        a = self.cur.fetchall()
        return(a)
        self.closeDb()
class UpdateTableDischarge(DatabaseTool):    
    def updateDischargeValues(self,icuNum,theValues):
        icuNumA = icuNum
        theValuesA = theValues
        sql = '''UPDATE discharge SET (fromWhere,checkinTip,checkinDate,admNum,name,gender,age,bed,checkoutTo,checkoutTip,checkoutDate,diagnosis,isImportant,finalTip,operateTime)=(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''+'''WHERE icuNum = %s'''%icuNumA
        self.cur.execute(sql,theValuesA)
        self.closeDb()

class DeletePatientData(DatabaseTool):
    def deleteOnePatientData(self,icuNum):
        icuNumA = icuNum
        sql = '''DELETE FROM discharge WHERE icuNum = %s'''%icuNumA
        self.cur.execute(sql)
        self.closeDb()


