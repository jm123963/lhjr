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

    data=c.css("CI005001.CI,CI005002.CI,CI005003.CI,CI005004.CI,CI005005.CI,CI005006.CI,CI005007.CI,CI005008.CI,CI005009.CI,CI005010.CI,CI005011.CI,CI005012.CI,CI005013.CI,CI005014.CI,CI005015.CI,CI005016.CI,CI005017.CI,CI005018.CI,CI005019.CI,CI005020.CI,CI005021.CI,CI005022.CI,CI005023.CI,CI005024.CI,CI005025.CI,CI005026.CI,CI005027.CI,CI005028.CI,CI005029.CI,CI005030.CI","PETTM","TradeDate="+date+",DelType=1,AdjustFlag=1,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\2clzb\hype.xls', encoding='utf-8-sig', index=None)

#退出
    data = logoutResult = c.stop()
except Exception as ee:
    print("error >>>",ee)
    traceback.print_exc()
else:
    print("demo end")

#转一位小数
import xlrd

xin=[]
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\2clzb\hype.xls')
table = data.sheets()[0]
st = data.sheet_by_index(0)
cap2 = table.col_values(1)
for i in range(1,st.nrows):
    xin.append(float('%.1f' % (float(cap2[i]))))

from pandas import DataFrame
n =['石油石化','煤炭','有色金属','电力及公用事业','钢铁','基础化工','建筑','建材','轻工制造','机械','电力设备及新能源','国防军工','汽车','商品零售','消费者服务','家电','纺织服装','医药','食品饮料','农林牧渔','银行','非银行金融','房地产','交通运输','电子','通信','计算机','传媒','综合','综合金融']
l1 = n
l2 = xin
df = DataFrame({'名称': l1, '涨幅': l2})
df.to_excel(r'C:\xyzy\1lhjr\2clzb\hype.xls', sheet_name='Sheet1', index=False) 

a=[]
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\2clzb\hype.xls')
table = data.sheets()[0]
st = data.sheet_by_index(0)
cap2 = table.col_values(1)
for i in range(1,st.nrows):
    a.append(cap2[i])

from pandas import DataFrame
l1 = n
l2 = a
df = DataFrame({'名称': l1, '行业涨幅': l2})
df.to_excel(r'C:\xyzy\1lhjr\2clzb\hype.xls', sheet_name='Sheet1', index=False)


#制图
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import xlrd

# 调节图像大小,清晰度
plt.figure(figsize=(25,15),dpi=300)

#指定字体为SimHei，用于显示中文，如果Ariel,中文会乱码
mpl.rcParams["font.sans-serif"]=["SimHei"]
#用来正常显示负号
mpl.rcParams["axes.unicode_minus"]=False

x1=[]
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\2clzb\hype.xls')
table = data.sheets()[0]
st = data.sheet_by_index(0)
cap2 = table.col_values(0)
for i in range(1,st.nrows):
    x1.append(cap2[i])

y1=[]
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\2clzb\hype.xls')
table = data.sheets()[0]
st = data.sheet_by_index(0)
cap2 = table.col_values(1)
for i in range(1,st.nrows):
    if float(cap2[i]) <= 100 and float(cap2[i]) > 0 :
        y1.append(float(cap2[i]))
    elif float(cap2[i]) > 100 or float(cap2[i]) <= 0 :
        y1.append(float(100))

l1 = x1
l2 = y1
df = DataFrame({'名称': l1, '当前PE': l2})
df.to_excel(r'C:\xyzy\1lhjr\2clzb\hype.xls', sheet_name='Sheet1', index=False)

import pandas as pd
stexcel=pd.read_excel(r'C:\xyzy\1lhjr\2clzb\hype.xls')
#ascending 默认等于True，按从小到大排列，改为False 按从大到小排
stexcel.sort_values(by='当前PE',inplace=True,ascending=True)
stexcel.to_excel(r'C:\xyzy\1lhjr\2clzb\hype.xls', sheet_name='Sheet1', index=False)

x1=[]
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\2clzb\hype.xls')
table = data.sheets()[0]
st = data.sheet_by_index(0)
cap2 = table.col_values(0)
for i in range(1,st.nrows):
    x1.append(cap2[i])

y1=[]
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\2clzb\hype.xls')
table = data.sheets()[0]
st = data.sheet_by_index(0)
cap2 = table.col_values(1)
for i in range(1,st.nrows):
        y1.append(float(cap2[i]))

plt.bar(x1,y1,align="center",hatch=" ",ec='gray',color='c')
plt.xticks(rotation=90,fontsize=15)
plt.yticks(fontsize=40)

#绘制纵向柱状图,hatch定义柱图的斜纹填充，省略该参数表示默认不填充。
#bar柱图函数还有以下参数：
#颜色：color,可以取具体颜色如red(简写为r),也可以用rgb让每条柱子采用不同颜色。
#描边：edgecolor（ec）：边缘颜色；linestyle（ls）：边缘样式；linewidth（lw）：边缘粗细
#填充：hatch，取值：/,|,-,+,x,o,O,.,*
#位置标志：tick_label

for a,b in zip(x1,y1):

    plt.text(a,b,'%.0f' %b, ha='center', va= 'bottom',fontsize=25)

plt.title('中信一级行业当前PE',fontsize=40)
plt.xlabel(u"")
plt.ylabel(u"")
plt.legend()
plt.savefig(r'C:\xyzy\1lhjr\2clzb\hype.png',c = 'k')