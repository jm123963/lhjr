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
    # zzqz
    data=c.csd("000985.CSI","PCTCHANGE","2020-01-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")    
    data.to_excel(r'C:\xyzy\1lhjr\3hgyb\zzqz.xls', encoding='utf-8-sig', index=None)
    
    # hs300
    data=c.csd("000300.SH","PCTCHANGE","2020-01-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")    
    data.to_excel(r'C:\xyzy\1lhjr\3hgyb\hs300.xls', encoding='utf-8-sig', index=None)

    # zz500
    data=c.csd("000905.SH","PCTCHANGE","2020-01-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")    
    data.to_excel(r'C:\xyzy\1lhjr\3hgyb\zz500.xls', encoding='utf-8-sig', index=None)

    # zz1000
    data=c.csd("000852.SH","PCTCHANGE","2020-01-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")    
    data.to_excel(r'C:\xyzy\1lhjr\3hgyb\zz1000.xls', encoding='utf-8-sig', index=None)
        
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

# zzqz
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\3hgyb\zzqz.xls')
table = data.sheets()[0]
st = data.sheet_by_index(0)

x1=[]
cap2 = table.col_values(1)
for i in range(1,st.nrows):
    x1.append(cap2[i][2:7])

y1=[]
cap2 = table.col_values(2)
for i in range(1,st.nrows):
    y1.append(float('%.1f' % (float(cap2[i]))))
    
plt.plot(x1, y1, label = "中证全指")
plt.xticks(rotation=90)

# hs300
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\3hgyb\hs300.xls')
table = data.sheets()[0]
st = data.sheet_by_index(0)

x1=[]
cap2 = table.col_values(1)
for i in range(1,st.nrows):
    x1.append(cap2[i][2:7])

y1=[]
cap2 = table.col_values(2)
for i in range(1,st.nrows):
    y1.append(float('%.1f' % (float(cap2[i]))))
    
plt.plot(x1, y1, label = "沪深300")
plt.xticks(rotation=90)

# zz500
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\3hgyb\zz500.xls')
table = data.sheets()[0]
st = data.sheet_by_index(0)

x1=[]
cap2 = table.col_values(1)
for i in range(1,st.nrows):
    x1.append(cap2[i][2:7])

y1=[]
cap2 = table.col_values(2)
for i in range(1,st.nrows):
    y1.append(float('%.1f' % (float(cap2[i]))))
    
plt.plot(x1, y1, label = "中证500")
plt.xticks(rotation=90)

# zz1000
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\3hgyb\zz1000.xls')
table = data.sheets()[0]
st = data.sheet_by_index(0)

x1=[]
cap2 = table.col_values(1)
for i in range(1,st.nrows):
    x1.append(cap2[i][2:7])

y1=[]
cap2 = table.col_values(2)
for i in range(1,st.nrows):
    y1.append(float('%.1f' % (float(cap2[i]))))
    
plt.plot(x1, y1, label = "中证1000")
plt.xticks(rotation=90)

plt.legend(loc='best')
plt.title('A股主要指数走势对比')
plt.savefig(r'C:\xyzy\1lhjr\3hgyb\agzs.png',c = 'k')
plt.show()
print('png end')

# 2022年上半年A股市场总体呈现单边下行态势，5月之后开启反弹。