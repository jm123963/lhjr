# -*- coding: utf-8 -*-

from EmQuantAPI import *
from datetime import timedelta, datetime
import time as _time
import traceback
from datetime import *

def mainCallback(quantdata):
    """
    mainCallback 是主回调函数，可捕捉如下错误
    在start函数第三个参数位传入，该函数只有一个为c.EmQuantData类型的参数quantdata
    :param quantdata:c.EmQuantData
    :return:
    """
    print ("mainCallback",str(quantdata))
    #登录掉线或者 登陆数达到上线（即登录被踢下线） 这时所有的服务都会停止
    if str(quantdata.ErrorCode) == "10001011" or str(quantdata.ErrorCode) == "10001009":
        print ("Your account is disconnect. You can force login automatically here if you need.")
    #行情登录验证失败（每次连接行情服务器时需要登录验证）或者行情流量验证失败时，会取消所有订阅，用户需根据具体情况处理
    elif str(quantdata.ErrorCode) == "10001021" or str(quantdata.ErrorCode) == "10001022":
        print ("Your all csq subscribe have stopped.")
    #行情服务器断线自动重连连续6次失败（1分钟左右）不过重连尝试还会继续进行直到成功为止，遇到这种情况需要确认两边的网络状况
    elif str(quantdata.ErrorCode) == "10002009":
        print ("Your all csq subscribe have stopped, reconnect 6 times fail.")
    # 行情订阅遇到一些错误(这些错误会导致重连，错误原因通过日志输出，统一转换成EQERR_QUOTE_RECONNECT在这里通知)，正自动重连并重新订阅,可以做个监控
    elif str(quantdata.ErrorCode) == "10002012":
        print ("csq subscribe break on some error, reconnect and request automatically.")
    # 资讯服务器断线自动重连连续6次失败（1分钟左右）不过重连尝试还会继续进行直到成功为止，遇到这种情况需要确认两边的网络状况
    elif str(quantdata.ErrorCode) == "10002014":
        print ("Your all cnq subscribe have stopped, reconnect 6 times fail.")
    # 资讯订阅遇到一些错误(这些错误会导致重连，错误原因通过日志输出，统一转换成EQERR_INFO_RECONNECT在这里通知)，正自动重连并重新订阅,可以做个监控
    elif str(quantdata.ErrorCode) == "10002013":
        print ("cnq subscribe break on some error, reconnect and request automatically.")
    # 资讯登录验证失败（每次连接资讯服务器时需要登录验证）或者资讯流量验证失败时，会取消所有订阅，用户需根据具体情况处理
    elif str(quantdata.ErrorCode) == "10001024" or str(quantdata.ErrorCode) == "10001025":
        print("Your all cnq subscribe have stopped.")
    else:
        pass

def startCallback(message):
    print("[EmQuantAPI Python]", message)
    return 1
def csqCallback(quantdata):
    """
    csqCallback 是csq订阅时提供的回调函数模板。该函数只有一个为c.EmQuantData类型的参数quantdata
    :param quantdata:c.EmQuantData
    :return:
    """
    print ("csqCallback,", str(quantdata))

def cstCallBack(quantdata):
    '''
    cstCallBack 是日内跳价服务提供的回调函数模板
    '''
    for i in range(0, len(quantdata.Codes)):
        length = len(quantdata.Dates)
        for it in quantdata.Data.keys():
            print(it)
            for k in range(0, length):
                for j in range(0, len(quantdata.Indicators)):
                    print(quantdata.Data[it][j * length + k], " ",end = "")
                print()
def cnqCallback(quantdata):
    """
    cnqCallback 是cnq订阅时提供的回调函数模板。该函数只有一个为c.EmQuantData类型的参数quantdata
    :param quantdata:c.EmQuantData
    :return:
    """
    # print ("cnqCallback,", str(quantdata))
    print("cnqCallback,")
    for code in quantdata.Data:
        total = len(quantdata.Data[code])
        for k in range(0, len(quantdata.Data[code])):
            print(quantdata.Data[code][k])

try:
    #调用登录函数（激活后使用，不需要用户名密码）
    loginResult = c.start("ForceLogin=1", '', mainCallback)
    if(loginResult.ErrorCode != 0):
        print("login in fail")
        exit()

    date = datetime.today().strftime("%Y-%m-%d")
    
    # EMM00183405 进出口金额:当月同比
    data=c.edb("EMM00183405", "IsLatest=0,StartDate=2021-07-01,EndDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\3hgyb\jck.xls', encoding='utf-8-sig', index=None)
    
    # EMM00183416 出口金额:累计同比
    data=c.edb("EMM00183416", "IsLatest=0,StartDate=2021-07-01,EndDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\3hgyb\ck.xls', encoding='utf-8-sig', index=None)
    
    # EMM00183417 进口金额:累计同比
    data=c.edb("EMM00183417", "IsLatest=0,StartDate=2021-07-01,EndDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\3hgyb\jk.xls', encoding='utf-8-sig', index=None)
    
#退出
    data = logoutResult = c.stop()
except Exception as ee:
    print("error >>>",ee)
    traceback.print_exc()
else:
    print("demo end")

#画图
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import xlrd
import matplotlib as mpl
import matplotlib.ticker as ticker

# 设置
pd.options.display.notebook_repr_html=False  # 表格显示
plt.rcParams['figure.dpi'] = 1000  # 图形分辨率
sns.set_theme(style='darkgrid')  # 图形主题

#指定字体为SimHei，用于显示中文，如果Ariel,中文会乱码
mpl.rcParams["font.sans-serif"]=["SimHei"]
#用来正常显示负号
mpl.rcParams["axes.unicode_minus"]=False

# jck
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\3hgyb\jck.xls')
table = data.sheets()[0]
st = data.sheet_by_index(0)

x1=[]
cap2 = table.col_values(1)
for i in range(1,st.nrows):
    x1.append(cap2[i][2:7])
x1 = list(reversed(x1))

y1=[]
cap2 = table.col_values(2)
for i in range(1,st.nrows):
    y1.append(float('%.1f' % (float(cap2[i]))))
y1 = list(reversed(y1))
   
plt.plot(x1, y1, label = "进出口金额:当月同比")
plt.xticks(rotation=90)

# ck
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\3hgyb\ck.xls')
table = data.sheets()[0]
st = data.sheet_by_index(0)

x1=[]
cap2 = table.col_values(1)
for i in range(1,5):
    x1.append(cap2[i][2:7])
for i in range(7,st.nrows):
    x1.append(cap2[i][2:7])
x1 = list(reversed(x1))

y1=[]
cap2 = table.col_values(2)
for i in range(1,5):
    y1.append(float('%.1f' % (float(cap2[i]))))
for i in range(7,st.nrows):
    y1.append(float('%.1f' % (float(cap2[i]))))
y1 = list(reversed(y1))
   
plt.plot(x1, y1, label = "出口金额:累计同比")
plt.xticks(rotation=90)

# jk
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\3hgyb\jk.xls')
table = data.sheets()[0]
st = data.sheet_by_index(0)

x1=[]
cap2 = table.col_values(1)
for i in range(1,5):
    x1.append(cap2[i][2:7])
for i in range(7,st.nrows):
    x1.append(cap2[i][2:7])
x1 = list(reversed(x1))

y1=[]
cap2 = table.col_values(2)
for i in range(1,5):
    y1.append(float('%.1f' % (float(cap2[i]))))
for i in range(7,st.nrows):
    y1.append(float('%.1f' % (float(cap2[i]))))
y1 = list(reversed(y1))
   
plt.plot(x1, y1, label = "进口金额:累计同比")
plt.xticks(rotation=90)

plt.legend(loc='best')
plt.title('我国每月进出口增速（%）')
plt.savefig(r'C:\xyzy\1lhjr\3hgyb\jck.png',c = 'k')
plt.show()
print('png end')

# 5月中国进出口总值3.45万亿元人民币，同比增长9.6%，增速比上月大幅提高9.5个百分点。