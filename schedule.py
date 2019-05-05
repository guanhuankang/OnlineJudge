#!coding=utf-8
import threading
import time
from DB import DB
from judger import judge

class Schedule:
    def init(self):
        self.currentRunID = 0
        self.finishRunID = -1
        self.threadnum = 10
        self.db = DB()
    def init(self,currid=0,finrid=-1,threadnum=5):
        self.currentRunID = currid
        self.finishRunID = finrid
        self.threadnum = threadnum
        self.db = DB()

    ##set self.currentRunID
    def waitforone(self):
        i = 0
        while i<self.threadnum: 
            if self.threads[i].isAlive()==False:
                return i
            i += 1
            if i==self.threadnum:i=0
        
    def runpart(self):
        if self.judgeQu and len(self.judgeQu)>0:
            for task in self.judgeQu:
                self.currentRunID = max(self.currentRunID,task[0])
                tid = self.waitforone()
                self.threads[ tid ] = threading.Thread( target=judge, args=(task,tid,) )
                self.threads[ tid ].start()
        else:
            self.currentRunID -= 1
        pass
        
    def run(self):
        running  = True
        self.threads = []
        for i in range(self.threadnum):
            self.threads.append(threading.Thread())
        while running:
            sql = "select code.runid,judgestatus,codefile,language,probid from code join submit where \
                 code.runid=submit.runid and code.runid>=%s and code.runid<%s "
            # sql = "select code.runid,judgestatus,codefile,language,probid from code join submit where \
            #      code.runid=submit.runid and code.runid>=%s and code.runid<%s and judgestatus='Waiting' "
            self.db.execsql(sql,(self.currentRunID,self.currentRunID+self.threadnum*10))
            self.judgeQu = self.db.fetchall()
            self.runpart()
            self.currentRunID+=1
            print("Current:",self.currentRunID)
            time.sleep(2)
            running = self.finishRunID==-1 or self.currentRunID<=self.finishRunID
        print("Schedule END")
    def finish(self):
        self.db.close()

sche = Schedule()
sche.init()
sche.run()
