# POJS简介
POJS（PtraceOnlineJudgeSystem）是Online Judge系统。POJS基于Ptrace系统调用的在线判题系统。用户提交多种语言（c++,python3等等）源代码，系统对源代码进行编译和执行，并通过预先设计的测试数据来检验程序源代码的正确性。Online Judge系统最初使用于ACM-ICPC国际大学生程序设计竞赛和OI信息学奥林匹克竞赛中的自动判题和排名。目前著名的OJ系统有Codeforce，UVA，POJ，HDUOJ等

# POJS需求说明
一个用户提交的程序在Online Judge系统下执行时将受到比较严格的限制，包括运行时间限制，内存使用限制和安全限制等。用户程序执行的结果将被Online Judge系统捕捉并保存，然后再转交给一个裁判程序（checker）。该裁判程序或者比较用户程序的输出数据和标准输出样例的差别，或者检验用户程序的输出数据是否满足一定的逻辑条件。最后系统返回给用户一个状态：通过（Accepted,AC）、答案错误(Wrong Answer,WA)、超时(Time Limit Exceed,TLE)、超过输出限制（Output Limit Exceed,OLE)、超内存（Memory Limit Exceed,MLE）、运行时错误（Runtime Error,RE）、格式错误（Presentation Error,PE)、或是无法编译（Compile Error,CE），并返回程序使用的内存、运行时间等信息。
POJS支持用户模块，题目模块，判题模块，裁判模块（多行匹配，SPJ，交互），比赛模块，管理模块（包含题目录入模块，用户管理模块）。





# POJS进度计划
时间点	完成任务
迭代一	判题模块，裁判模块（多行匹配）
迭代二	题目模块，基本界面设计
迭代三	文档完善，用户模块，功能完善
未来	完善裁判和管理模块，比赛模块

# POJS总体设计
总体采用前后端设计。前端是python flask编写，后端包含判题模块，后台处理模块。前端显示页面，后台把用户代码保存到代码库，把提交信息录入数据库。判题模块不断查询数据库，查询等待判题的提交，从代码库和题目库中抽取对应文件进行判题，把结果写回数据库。前端查询提交状态，后台查询数据库返回查询结果。





# POJS 接口说明
该系统各个模块功能说明，如下(尖括号内是路径，dir表示这是一个文件夹)：
Server.py</server.py>	服务器核心代码
完成响应用户所有请求
框架：python3+flask
Schedule.py</schedule.py>	判题调度模块
完成查询数据库，调度线程进行判题
Judger.py</judger.py>	判题单元
由判题调度模块分配一个任务，开启该任务工作，负责完成判题任务，把结果写回数据库结果
Checker.py</checker.py>	检查器
由判题单元调用，负责多行匹配功能，只要用于答案匹配
DB.py</DB.py>	数据库模块
负责数据库连接，查询等
Db.json</db.json>	数据库配置文件
Sandbox</tool/sandbox>	沙盒
判题的核心部分，负责装入用户代码，完成用户程序执行，安全检查，资源限制，重定向输入输出等功能，由判题单元调用，结果以重定向到文件形式返回。帮助选项-help
Sandbox.h</tool/sandbox.h>	沙盒头文件
Sandbox.config</tool/sandbox.config>	沙盒配置文件
Sysconfig=1 c++配置
Sysconfig=2 python3配置
配置该文件可以限制用户代码系统调用次数，从而达到安全限制
Code<dir>	代码库
Problem<dir>	问题输入，标准输出，标准程序
Judgers<dir>	判题进程临时工作空间
Templates<dir>	前端模板



# POJS测试
测试代码，目前已经通过初步测试，支持返回结果：AC,WA,RE,TLE,MLE,OLE等结果和可以检测一系列非法操作，可以有效保护系统免受攻击。内测地址：http://193.112.81.45:5520/
评测结果显示：


# POJS部署
Ubuntu环境安装python3.5.2, flask, pymysql, mysql。
解压文件，导入数据库oj.sql。运行server.py 和 schedule.py。

# POJS更新记录
更新日志

# POJS维护记录
维护记录，修补bug
