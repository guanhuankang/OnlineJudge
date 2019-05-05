#!coding=utf-8
def checker(stdfile,userfile):
    stdout = []
    userout = []
    with open(stdfile,"r") as f:
        for line in f:
            stdout += [line.strip()]
    with open(userfile,"r") as f:
        for line in f:
            userout += [line.strip()]
    stdlen = len(stdout)
    userlen = len(userout)
    while stdlen>0 and (stdout[stdlen-1]=='\n' or stdout[stdlen-1]=='' or stdout[stdlen-1]==None):
        stdlen -= 1
    while userlen>0 and (userout[userlen-1]=='\n' or userout[userlen-1]=='' or userout[userlen-1]==None):
        userlen -= 1
    if userlen!=stdlen:return False
    for i in range(userlen):
        if userout[i]!=stdout[i]:
            return False
    return True

def toInt(s):
    try:
        x = float(s)
        return int(x)
    except Exception as e:
        return 0

## status mem(bytes)0,cpu(ms)1,normal-2-3,sig-4-5,illegal-6-7,sys-8-9
def checkPre(limitcputime,limitmemory,status,stdfile,userfile):
    status = status.split()
    status[0] = toInt(status[0])
    status[1] = toInt(status[1])
    if status[8]=="1" and status[9]!="1002":
        return ("SystemError",status[1],status[0])
    if status[6]=="1":
        return ("Illegal_%s"%status[7],status[1],status[0])
    if status[4]=="1":
        if status[5]=="11":return ("RE",status[1],status[0])
        if status[5]=="25":return ("OLE",status[1],status[0])
        if status[5]=="24":return ("TLE",status[1],status[0])
        else:return ("LimitError_%s"%status[5],status[1],status[0])
    ## normal exit
    if int(limitcputime)<status[1]:
        return ("TLE",status[1],status[0])
    if int(limitmemory)<int( status[0]/1024 ): ## KB
        return ("MLE",status[1],status[0])
    ac = checker(stdfile,userfile)
    if ac:return ("Accept",status[1],status[0])
    return ("WrongAnswer",status[1],status[0])