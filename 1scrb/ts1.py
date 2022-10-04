# -*- coding: utf-8 -*-

from pyexpat.errors import codes
from EmQuantAPI import *
from datetime import timedelta, datetime
import time as _time
import traceback
from datetime import *
import numpy as np


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
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.xls', encoding='utf-8-sig', index=None)
    print(data)

#退出
    data = logoutResult = c.stop()
except Exception as ee:
    print("error >>>",ee)
    traceback.print_exc()
else:
    print("demo end")

n = ['农林牧渔','基础化工','钢铁','有色金属','电子','家用电器','食品饮料','纺织服饰','轻工制造','医药生物','公用事业','交通运输','房地产','商业贸易','社会服务','综合','建筑材料','建筑装饰','电力设备','国防军工','计算机','传媒','通信','银行','非银金融','汽车','机械设备','煤炭','石油石化','环保','美容护理']

import xlwings as xw

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.xls')
sht = wb.sheets[0]
a = sht.range('b2:b32').value
wb.close()

from pandas import DataFrame
l1 = n
l2 = a
df = DataFrame({'名称': l1, '行业涨幅': l2})
df.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.xls', sheet_name='Sheet1', index=False)

import pandas as pd
stexcel=pd.read_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.xls')
#ascending 默认等于True，按从小到大排列，改为False 按从大到小排
stexcel.sort_values(by='行业涨幅',inplace=True,ascending=False)
stexcel.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.xls', sheet_name='Sheet1', index=False)

#转整数
import xlrd
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.xls')
table = data.sheets()[0]
xin = []
cap2 = table.col_values(1)
for i in range(1,32):
    xin.append('%.0f' % cap2[i])
from pandas import DataFrame
n =['农林牧渔','基础化工','钢铁','有色金属','电子','家用电器','食品饮料','纺织服饰','轻工制造','医药生物','公用事业','交通运输','房地产','商业贸易','社会服务','综合','建筑材料','建筑装饰','电力设备','国防军工','计算机','传媒','通信','银行','非银金融','汽车','机械设备','煤炭','石油石化','环保','美容护理']
l1 = n
l2 = xin
df = DataFrame({'名称': l1, '涨幅': l2})
df.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.xls', sheet_name='Sheet1', index=False)
#制图
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import xlrd

# 调节图像大小,清晰度
plt.figure(figsize=(12,8),dpi=300)

#指定字体为SimHei，用于显示中文，如果Ariel,中文会乱码
mpl.rcParams["font.sans-serif"]=["SimHei"]
#用来正常显示负号
mpl.rcParams["axes.unicode_minus"]=False

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.xls')
table = data.sheets()[0]

x1=[]   
cap1 = table.col_values(0)
for i in range(1,32):
    x1.append(cap1[i]) 
    
y1=[]   
cap2 = table.col_values(1)
for i in range(1,32):
    y1.append(float(cap2[i]))

plt.bar(x1,y1,
            color=np.where(np.array(y1)>0,'r','c'), #判断大于0的为红色，负的为蓝色
            #width=0.8,   #柱形宽度
            align='center', #柱形的位置edge/center 
            hatch=" ",
            #alpha=0.8,    #柱形透明度
            #hatch='*',    #柱形表明的形状样式
            edgecolor='gray',#柱形边缘颜色
            #bottom=0.1   #柱形离底部的距离
          )
plt.xticks(rotation=90,fontsize=15)
plt.yticks(fontsize=20)

for a,b in zip(x1,y1):
    plt.text(a,b,'%.0f' % b, ha='center', va= 'bottom',fontsize=10)
plt.title('250日行业涨幅%',fontsize=20)
plt.xlabel(u"")
plt.ylabel(u"")
plt.legend()
plt.savefig(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.png',c = 'k')