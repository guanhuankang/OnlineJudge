#!coding=utf-8
from DB import DB
from checker import checkPre
import os,sys

# runid,judgestatus,codefile,language,probid  judger
## return ( ("",time,mem),msg)
def runcpp(task,judger):
    db = DB()
    sql = "select datain,dataout,checker,limittime,limitmemory from checker where probid = %s"
    db.execsql(sql,(task[4],))
    prob = db.fetchone()
    if prob==None or prob==():
        db.close()
        return (("NoProblem%d"%task[4],0,0),"")
    datain=prob[0];dataout=prob[1];checker=prob[2] ## path(std-in, std-out, checker)
    limitime = prob[3];limitmemory=prob[4] ## ms KB
    rid = task[0];codefile = task[2] ## rid codefile
    inFile = "./judgers/judger%d/data.in"%(judger,) ## infile
    outFile = "./judgers/judger%d/data.out"%(judger,) ## outfile
    walltime = limitime/1000+30 ## walltime
    target = "./judgers/judger%d/%d"%(judger,rid,) ## target prog
    errfile = "./judgers/judger%d/error"%(judger,) ## errfile
    
    stdoutFile = "./judgers/judger%d/%d.stdout"%(judger,rid)

    sql = "update code set judgestatus = %s where runid=%s"
    db.execsql(sql,("Comiling", rid ))

    cmd = "./tool/sandbox -thread 2000 -mem 1024 -cputime 10 -inFile %s -outFile %s -errfile %s -param \
         /usr/bin/g++ g++ -w %s -o %s >/dev/null"%(inFile,outFile,errfile,codefile,target)
    
    os.system(cmd)
    result = ""
    with open(errfile) as f:
        result = f.read()
    if result!="":
        db.close()
        return (("CompileError",0,0),result)

    sql = "update code set judgestatus = %s where runid=%s"
    db.execsql(sql,("Running", rid ));db.close()

    cmd = "./tool/sandbox -walltime %d -cputime %d -mem %d -syscallConfig 1 \
        -inFile %s -outFile %s -configFile ./tool/sandbox.config -errfile %s -param \
         %s %d > %s"%(\
            walltime, limitime/1000+1, limitmemory/512, datain, outFile, errfile,\
            target,rid,stdoutFile)
    os.system(cmd)
    fstdout = open(stdoutFile,"r")
    result = fstdout.readline()
    fstdout.close()
    result = checkPre(limitime,limitmemory,result,dataout,outFile)
    msg = ""
    with open(errfile,"r") as ferr:
        msg = ferr.read()
    os.system("rm -rf ./judgers/judger%d/*"%judger)
    return (result,msg)

def runpy3(task,judger):
    db = DB()
    sql = "select datain,dataout,checker,limittime,limitmemory from checker where probid = %s"
    db.execsql(sql,(task[4],))
    prob = db.fetchone()
    if prob==None or prob==():
        db.close()
        return (("NoProblem%d"%task[4],0,0),"")
    datain=prob[0];dataout=prob[1];checker=prob[2] ## path(std-in, std-out, checker)
    limitime = prob[3];limitmemory=prob[4] ## ms KB
    rid = task[0];codefile = task[2] ## rid codefile
    inFile = "./judgers/judger%d/data.in"%(judger,) ## infile
    outFile = "./judgers/judger%d/data.out"%(judger,) ## outfile
    errfile = "./judgers/judger%d/error"%(judger,) ## errfile
    walltime = limitime/1000+30 ## walltime
    stdoutFile = "./judgers/judger%d/%d.stdout"%(judger,rid) ## read status
    
    sql = "update code set judgestatus = %s where runid=%s"
    db.execsql(sql,("Running", rid ));db.close()

    cmd = "./tool/sandbox -walltime %d -cputime %d -mem %d -syscallConfig 2 \
        -inFile %s -outFile %s -configFile ./tool/sandbox.config -errfile %s -param \
        /usr/bin/python3 python3 %s > %s"%(\
            walltime, limitime/1000+1, limitmemory/512, datain, outFile, errfile,\
            codefile,stdoutFile)
    os.system(cmd)
    fstdout = open(stdoutFile,"r")
    result = fstdout.readline()
    fstdout.close()
    result = checkPre(limitime,limitmemory,result,dataout,outFile)
    msg = ""
    with open(errfile,"r") as ferr:
        msg = ferr.read()
    os.system("rm -rf ./judgers/judger%d/*"%judger)
    return (result,msg)


def judge(task,judger):
    result = (("language_not_support",0,0),"")
    if task[3]=="c++":
        result = runcpp(task,judger)
    elif task[3]=="python3":
        result = runpy3(task,judger)
    sql = "update code set judgestatus = %s, exetime=%s, exememory=%s, warning=%s where runid=%s"
    db = DB()
    db.execsql(sql, (result[0][0],result[0][1],int(result[0][2]/1024),result[1][0:255],task[0]) )
    db.close()
    pass
