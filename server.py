from flask import Flask,request,session,redirect,url_for
from flask import render_template
import datetime,os
from DB import DB

app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.urandom(16))
app.config['PERMANENT_SESSION_LIFTIME'] = 30*60*1000
PAGESIZE = 10

def verify(username,passwd):
    db = DB()
    session["verify"] = False
    sql = "select count(*) from users where uid=%s and password=%s"
    db.execsql(sql,(username,passwd))
    ans = db.fetchone()
    db.close()
    if int(ans[0])>0:
        session["verify"] = True
        session["uid"] = username

def getFiletype(language):
    if language == "c++" or language=="c++14":
        return ".cpp"
    elif language == 'python3' or language=="python2":
        return ".py"
    return ".txt"

def toDigit(x):
    try:
        x=int(x)
        return x
    except Exception as e:
        return 0

@app.route("/status",methods=["GET"])
def status():
    if "verify" not in session or session["verify"]==False:
        return redirect(url_for("login"))
    db = DB()
    sql = "select max(runid) from submit"
    db.execsql(sql)
    maxrid = int(db.fetchone()[0])

    pagedelta = toDigit(request.args.get("delta"))
    if "page" not in session:
        session["page"] = int(maxrid/PAGESIZE)
    session["page"] += pagedelta
    session["page"] = min(session["page"],int(maxrid/PAGESIZE))
    session["page"] = max(session["page"],0)

    thead = ["Run ID","User ID","Submit Time","Judge Status",\
        "Pro.ID","Exe.Time(ms)","Exe.Memory(KB)","Code Len.","Language"]
        
    sql = "select submit.runid,uid,submtime,judgestatus,probid,exetime,exememory,codelen,\
            language from submit join code where submit.runid=code.runid \
            and code.runid >= %s and code.runid < %s order by submit.submtime DESC"
    msg = "Welcome %s !"%(session['uid'],)
    db.execsql(sql, (session["page"]*PAGESIZE, session["page"]*PAGESIZE+PAGESIZE ) )
    _tdata = db.fetchall()
    tdata = []
    for line in _tdata:
        color = "red"
        if line[3]=="WrongAnswer":color="black"
        elif line[3]=="CompileError":color="yellow"
        elif line[3]=="Accept":color="red"
        else :color = "black"
        tline = [("blue","./showcode?runid=%s"%line[0],line[0]),
            ("black","#",line[1]),
            ("black","#",line[2]),
            (color,"./showwarning?runid=%s"%line[0],line[3]),
            ("black","./problem?probid=%s"%line[4],line[4]),
            ("black","#",line[5]),
            ("black","#",line[6]),
            ("blue","./showcode?runid=%s"%line[0],line[7]),
            ("black","#",line[8])
        ]
        tdata += [tline]
    return render_template("./status.html",thead=thead,tdata=tdata,msg = msg)

@app.route("/submit",methods=["POST","GET"])
def submit():
    if "verify" not in session or session["verify"]==False:
        return redirect(url_for("login"))
    try:
        probid = toDigit(str(request.form.get("probid")))
        language = str(request.form.get("language"))
        sql = "insert into submit (uid,probid,language) values (%s,%s,%s)"
        db = DB()
        db.execsql(sql,(session["uid"],probid,language))
        
        rid = db.getID()
        code = request.form.get("code")
        filename = "./code/"+str(rid)+getFiletype(language) ## get code filename
        sql = "insert into code (runid,codelen,codefile) values (%s,%s,%s)"
        db.execsql(sql,(rid,len(code),filename))
        db.close()
        ## save code file to disks
        with open(filename,"w") as f:
            f.write(code)
        session["page"] = 1000000000
        return redirect(url_for("status"))
    except Exception as e:
        return redirect(url_for("status"))

@app.route("/register",methods=["POST","GET"])
def register():
    uid = request.form.get("uid")
    passwd = request.form.get("password")
    passwd1 = request.form.get("password2")
    gender = request.form.get("gender")
    if( not(uid and passwd and passwd1 and gender) ):
        return render_template("./register.html",msg="Please check your input (No null)")
    uid=str(uid);passwd=str(passwd);passwd1=str(passwd1);gender=str(gender)
    if(passwd!=passwd1 or uid=="" or passwd=="" or uid==None or passwd==None):
        return render_template("./register.html",msg="Please check your password & username (inconsitent)")
    
    db = DB()
    sql = "select count(*) from users where uid=%s"
    db.execsql(sql,(uid,))
    rs = db.fetchone()
    if( (rs and rs[0]>0) or rs==None):
        db.close()
        return render_template("./register.html",msg="Username has been existed")
    sql = "insert into users (uid,password,gender) values (%s,%s,%s)"
    db.execsql(sql,(uid,passwd,gender))
    db.close()
    return render_template("./login.html",msg="Register Sucessful")


@app.route("/login",methods=["POST","GET"])
def login():
    session["verify"] = False
    uid = str(request.form.get("uid"))
    passwd = str(request.form.get("password"))
    verify(uid,passwd)
    if session["verify"]==True:
        return redirect(url_for("index"))
    return render_template("./login.html",msg="username or passwd incorrect!")


@app.route("/showwarning",methods=["POST","GET"])
def showwarning():
    if "verify" not in session or session["verify"]==False:
        return redirect(url_for("login"))
    rid = str(request.args.get("runid"))
    uid = str(session['uid'])
    sql = "select warning,judgestatus from code join submit\
     where submit.runid=code.runid and uid=%s and submit.runid=%s"
    db = DB()
    db.execsql(sql,(uid,rid) )
    rs = db.fetchone()
    db.close()
    print(rs)
    if rs and len(rs)>0:
        warning = rs[0]
        if warning=="":warning=rs[1]
        return render_template("./showwarning.html",msg="Code by %s!"%uid,warning=warning)
    return render_template("./showwarning.html",msg="Code by %s!"%uid,warning="Permission deny")

@app.route("/showcode",methods=["POST","GET"])
def showcode():
    if "verify" not in session or session["verify"]==False:
        return redirect(url_for("login"))
    rid = str(request.args.get("runid"))
    uid = str(session['uid'])
    sql = "select codefile from code join submit\
     where submit.runid=code.runid and uid=%s and submit.runid=%s"
    db = DB()
    db.execsql(sql,(uid,rid) )
    rs = db.fetchone()
    db.close()
    if rs and len(rs)>0:
        codefile = rs[0]
        try:
            with open(codefile,"r") as f:
                code = f.read()
                return render_template("./showcode.html",msg="Code by %s!"%uid,code=code)
        except Exception as e:
            pass
    return render_template("./showcode.html",msg="Code by %s!"%uid,code="Permission deny")

@app.route("/problemlist",methods=["POST","GET"])
def problemlist():
    if "verify" not in session or session["verify"]==False:
        return redirect(url_for("login"))
    return render_template("./problemlist.html",msg="welcome %s"%session['uid'])

@app.route("/problem",methods=["POST","GET"])
def problem():
    probid = toDigit(request.args.get("probid"))
    if probid<=1000:probid = 1001
    db = DB()
    sql = "select probid,probtime,title,statement,input,output,sampleinput,\
        sampleoutput,source,link from problem where probid=%s"
    db.execsql(sql,(probid,))
    rs = db.fetchone()
    db.close()
    return render_template("./problem.html",probid=rs[0],probtime=rs[1],title=rs[2],\
    statement=rs[3],input=rs[4],output=rs[5],sampleinput=rs[6],sampleoutput=rs[7],\
    source=rs[8],link=rs[9])

@app.route("/submitpage",methods=["POST","GET"])
def submitpage():
    if "verify" not in session or session["verify"]==False:
        return redirect(url_for("login"))
    proid = toDigit(request.args.get("proid"))
    return render_template("./submit.html",proid=proid)

@app.route("/")
def index():
    if "verify" in session and session["verify"]:
        return redirect(url_for("problemlist"))
    else:
        return render_template("./login.html",msg="Please login first")

if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0',port=5520)
