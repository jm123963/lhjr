# -*- coding: utf-8 -*-

from pyexpat.errors import codes
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
    # 指数 涨跌幅
    data=c.csd("801831.SWI","PCTCHANGE","2000-08-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\2clzb\gpb.xls', encoding='utf-8-sig', index=None)

    data=c.csd("801833.SWI","PCTCHANGE","2000-08-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\2clzb\dpb.xls', encoding='utf-8-sig', index=None)

#退出
    data = logoutResult = c.stop()
except Exception as ee:
    print("error >>>",ee)
    traceback.print_exc()
else:
    print("demo end")
    
    
import xlwings as xw

wb = xw.Book(r'C:\xyzy\1lhjr\2clzb\gpb.xls')
sht = wb.sheets[0]
rng = sht.range('c1').expand('table')
nrows = rng.rows.count
gpb = sht.range(f'c2:c{nrows}').value
wb.close()

wb = xw.Book(r'C:\xyzy\1lhjr\2clzb\dpb.xls')
sht = wb.sheets[0]
rng = sht.range('c1').expand('table')
nrows = rng.rows.count
dpb = sht.range(f'c2:c{nrows}').value
wb.close()

from pandas import DataFrame
l1 = gpb
l2 = dpb
df = DataFrame({'gpb': l1, 'dpb': l2})
df.to_excel(r'C:\xyzy\1lhjr\2clzb\gpbdpb.xls', sheet_name='Sheet1', index=False)

import pandas as pd
data_= pd.read_excel(r'C:\xyzy\1lhjr\2clzb\gpbdpb.xls')
data_['gpbcydpb'] = round(data_['gpb'] / data_['dpb']).astype('str')
data_['gpbcydpb'].to_excel(r'C:\xyzy\1lhjr\2clzb\gpbcydpb.xls', index=False)


wb = xw.Book(r'C:\xyzy\1lhjr\2clzb\gpb.xls')
sht = wb.sheets[0]
rng = sht.range('b1').expand('table')
nrows = rng.rows.count
dt = sht.range(f'b1:b{nrows}').value
wb.close()

wb = xw.Book(r'C:\xyzy\1lhjr\2clzb\gpbcydpb.xls')
sht = wb.sheets[0]
rng = sht.range('a1').expand('table')
nrows = rng.rows.count
zs = sht.range(f'a1:a{nrows}').value
wb.close()

from pandas import DataFrame
l1 = dt
l2 = zs
df = DataFrame({'dt': l1, 'zs': l2})
df.to_excel(r'C:\xyzy\1lhjr\2clzb\gpbdpb.xls', sheet_name='Sheet1', index=False)


import pandas as pd
import matplotlib.pyplot as plt
import xlrd
import matplotlib as mpl
import matplotlib.ticker as ticker

#指定字体为SimHei，用于显示中文，如果Ariel,中文会乱码
mpl.rcParams["font.sans-serif"]=["SimHei"]
#用来正常显示负号
mpl.rcParams["axes.unicode_minus"]=False
plt.figure(figsize=(20,8))

x1=[]
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\2clzb\gpbdpb.xls')
table = data.sheets()[0]
st = data.sheet_by_index(0)
cap2 = table.col_values(0)
for i in range(2,st.nrows):
    x1.append(cap2[i][2:7])

y1=[]
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\2clzb\gpbdpb.xls')
table = data.sheets()[0]
st = data.sheet_by_index(0)
cap2 = table.col_values(1)
for i in range(2,st.nrows):
    if float(cap2[i]) <= 10 and float(cap2[i]) >= -10 :
        y1.append(float(cap2[i]))
    elif float(cap2[i]) > 10 or float(cap2[i]) < -10 :
        y1.append(0)

plt.plot(x1,y1)
plt.xticks(rotation=90,fontsize=20)
plt.yticks(fontsize=20)

plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(4))

#绘制纵向柱状图,hatch定义柱图的斜纹填充，省略该参数表示默认不填充。
#bar柱图函数还有以下参数：
#颜色：color,可以取具体颜色如red(简写为r),也可以用rgb让每条柱子采用不同颜色。
#描边：edgecolor（ec）：边缘颜色；linestyle（ls）：边缘样式；linewidth（lw）：边缘粗细
#填充：hatch，取值：/,|,-,+,x,o,O,.,*
#位置标志：tick_label

plt.title('高市净率指数/低市净率指数',fontsize=30)
plt.xlabel(u"")
plt.ylabel(u"")
plt.legend()
plt.savefig(r'C:\xyzy\1lhjr\2clzb\gpbdpb.png',c = 'k')
