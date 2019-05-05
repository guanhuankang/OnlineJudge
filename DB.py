import json
import pymysql
import hashlib
class DB:
    def __init__(self):
        with open("db.json") as f:
            self.config = json.loads(f.read())
            self.connect()
    def connect(self):
        self.db = pymysql.connect(host=self.config["host"],
            user=self.config["user"],password=self.config["password"],
            port=self.config["port"],db=self.config["db"])
    def close(self):
        self.db.close()
    def setConfig(self,config):
        self.config = config
    def getConfig(self):
        return self.config
    def execsql(self,sql,tup=()):
        self.cur = self.db.cursor()
        self.cur.execute(sql,tup)
        self.db.commit()
        return self.cur
    def getHash(self,s):
        self.md5 = hashlib.md5()
        self.md5.update(s.encode("utf8"))
        return self.md5.hexdigest()
    def fetchall(self):
        return self.cur.fetchall()
    def fetchone(self):
        return self.cur.fetchone()
    def disp(self):
        print(self.cur.fetchone())
    def getTable(self):
        sql = "select * from EntityLib"
        self.execsql(sql)
        self.table = self.cur.fetchall()
    def getID(self):
        return self.cur.lastrowid
        pass



# db = DB()
# url = "http://whu/edu/cn"
# md5 = db.getHash(url)
# print(md5,url)

# sql = "select * from EntityArc"
# db.execsql(sql)
# db.disp()
# db.close()