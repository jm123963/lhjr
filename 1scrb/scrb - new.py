# -*- coding: utf-8 -*-
from EmQuantAPI import *
from datetime import timedelta, datetime
import time as _time
import traceback
from datetime import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import xlwings as xw
import xlrd
import numpy as np
import pandas as pd
from pandas import DataFrame
from pylab import mpl
from pandas.plotting import table
import plotly_express as px
import plotly.graph_objects as go

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

    # 市场特征
    date = datetime.today().strftime("%Y-%m-%d")
    # 指数涨幅
    zs0=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGE","N=-0,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")    
    zs5=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    zs10=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    zs20=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    zs60=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    zs120=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    zs250=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    # 指数 （日）主力净流入资金
    date = (datetime.today() + timedelta(days = -0)).strftime("%Y-%m-%d")
    zszj0=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    date = (datetime.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
    zszj1=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    date = (datetime.today() + timedelta(days = -2)).strftime("%Y-%m-%d")
    zszj2=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    # 指数走势
    date = datetime.today().strftime("%Y-%m-%d")
    zszs=c.csd("000985.CSI,000300.SH,000905.SH,000852.SH","CLOSE","2005-01-01",""+date+"","period=3,adjustflag=3,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    zszs3=c.csd("000985.CSI,000300.SH,000905.SH,000852.SH","CLOSE","2020-01-01",""+date+"","period=1,adjustflag=3,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    
    # 风格涨幅
    date = datetime.today().strftime("%Y-%m-%d")
    fg0=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGE","N=0,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    fg5=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    fg10=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    fg20=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    fg60=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    fg120=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    fg250=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    # 风格资金
    date = (datetime.today() + timedelta(days = -0)).strftime("%Y-%m-%d")
    fgzj0=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    date = (datetime.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
    fgzj1=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    date = (datetime.today() + timedelta(days = -2)).strftime("%Y-%m-%d")
    fgzj2=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    # 风格走势
    date = datetime.today().strftime("%Y-%m-%d")
    fgzs=c.csd("399373.SZ,399377.SZ,399372.SZ,399376.SZ","CLOSE","2003-01-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    fgzs3=c.csd("399373.SZ,399377.SZ,399372.SZ,399376.SZ","CLOSE","2020-01-01",""+date+"","period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")

    # 行业风格涨幅
    date = datetime.today().strftime("%Y-%m-%d")
    hyfg0=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,DIFFERRANGE","N=0,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    hyfg5=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    hyfg10=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    hyfg20=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    hyfg60=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    hyfg120=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    hyfg250=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    # 行业风格资金
    date = (datetime.today() + timedelta(days = -0)).strftime("%Y-%m-%d")
    hyfgzj0=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    date = (datetime.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
    hyfgzj1=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    date = (datetime.today() + timedelta(days = -2)).strftime("%Y-%m-%d")
    hyfgzj2=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    # 行业风格走势
    date = datetime.today().strftime("%Y-%m-%d")
    hyfgzs =c.csd("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","CLOSE","2003-01-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    hyfgzs3 =c.csd("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","CLOSE","2020-01-01",""+date+"","period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")

    # 行业涨幅
    date = datetime.today().strftime("%Y-%m-%d")
    hy0=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGE","N=-0,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    hy0=hy0.sort_values(by="DIFFERRANGE",ascending=False)
    hy5=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    hy5=hy5.sort_values(by="DIFFERRANGEN",ascending=False)
    hy10=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    hy10=hy10.sort_values(by="DIFFERRANGEN",ascending=False)
    hy20=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    hy20=hy20.sort_values(by="DIFFERRANGEN",ascending=False)
    hy60=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    hy60=hy60.sort_values(by="DIFFERRANGEN",ascending=False)
    hy120=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    hy120=hy120.sort_values(by="DIFFERRANGEN",ascending=False)
    hy250=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    hy250=hy250.sort_values(by="DIFFERRANGEN",ascending=False)
    # 行业资金
    date = (datetime.today() + timedelta(days = -0)).strftime("%Y-%m-%d")
    hyzj0=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    hyzj = hyzj0.sort_values(by="NETINFLOW",ascending=False)
    date = (datetime.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
    hyzj1=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    date = (datetime.today() + timedelta(days = -2)).strftime("%Y-%m-%d")
    hyzj2=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
 
    # 投资策略
    date = datetime.today().strftime("%Y-%m-%d")
    # 指数PB
    zspb=c.csd("000002.SH","PBLYR","2003-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    zspb3=c.csd("000002.SH","PBLYR","2020-01-01",""+date+"","DelType=1,period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")

    # 指数PE
    zspe=c.csd("000002.SH","PETTM","2003-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    zspe3=c.csd("000002.SH","PETTM","2020-01-01",""+date+"","DelType=1,period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")

    # 小盘大盘比
    xp=c.csd("399316.SZ","CLOSE","2003-01-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    dp=c.csd("399314.SZ","CLOSE","2003-01-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    xp3=c.csd("399316.SZ","CLOSE","2020-01-01",""+date+"","period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    dp3=c.csd("399314.SZ","CLOSE","2020-01-01",""+date+"","period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")

    # 成长价值比
    cz=c.csd("399370.SZ","CLOSE","2003-01-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    jz=c.csd("399371.SZ","CLOSE","2003-01-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    cz3=c.csd("399370.SZ","CLOSE","2020-01-01",""+date+"","period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    jz3=c.csd("399371.SZ","CLOSE","2020-01-01",""+date+"","period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")

#退出
    data = logoutResult = c.stop()
except Exception as ee:
    print("error >>>",ee)
    traceback.print_exc()
else:
    print("demo end")

# 指数涨幅
zs0['NAME'] = zs0['NAME'].str.replace('指数', '')
fig = px.bar(zs0,x='NAME',y='DIFFERRANGE',text='DIFFERRANGE')
fig.update_traces(texttemplate='%{text:.1f}',textposition='inside',marker=dict(color=np.where(np.array(zs0['DIFFERRANGE'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "当日涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zs0.png',scale=3)

zs5['NAME'] = zs5['NAME'].str.replace('指数', '')
fig = px.bar(zs5,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(zs5['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计5日涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zs5.png',scale=3)

zs10['NAME'] = zs10['NAME'].str.replace('指数', '')
fig = px.bar(zs10,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(zs10['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计10日涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zs10.png',scale=3)

zs20['NAME'] = zs20['NAME'].str.replace('指数', '')
fig = px.bar(zs20,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(zs20['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计20日涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zs20.png',scale=3)

zs60['NAME'] = zs60['NAME'].str.replace('指数', '')
fig = px.bar(zs60,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(zs60['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计60日涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zs60.png',scale=3)

zs120['NAME'] = zs120['NAME'].str.replace('指数', '')
fig = px.bar(zs120,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(zs120['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计120日涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zs120.png',scale=3)

zs250['NAME'] = zs250['NAME'].str.replace('指数', '')
fig = px.bar(zs250,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(zs250['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计250日涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zs250.png',scale=3)

# 指数表格
# 数据合并
zshb=pd.concat([zs0,zs5,zs10,zs20,zs60,zs120,zs250],names=None,axis=1,ignore_index=True) 
# 删除无用列
zshb.drop(zshb.columns[[0,1,4,5,6,8,9,10,12,13,14,16,17,18,20,21,22,24,25,26]],axis = 1,inplace = True)
# 变更列名
zshb.columns=['指数', '当日涨幅', '累计5日涨幅', '累计10日涨幅', '累计20日涨幅', '累计60日涨幅', '累计120日涨幅', '累计250日涨幅']
# 删除特定字符
zshb.指数 = zshb.指数.str.replace('指数', '')
# 设置小数位
zshb.当日涨幅=zshb.当日涨幅.map(lambda x:('%.1f')%x)
zshb.累计5日涨幅=zshb.累计5日涨幅.map(lambda x:('%.0f')%x)
zshb.累计10日涨幅=zshb.累计10日涨幅.map(lambda x:('%.0f')%x)
zshb.累计20日涨幅=zshb.累计20日涨幅.map(lambda x:('%.0f')%x)
zshb.累计60日涨幅=zshb.累计60日涨幅.map(lambda x:('%.0f')%x)
zshb.累计120日涨幅=zshb.累计120日涨幅.map(lambda x:('%.0f')%x)
zshb.累计250日涨幅=zshb.累计250日涨幅.map(lambda x:('%.0f')%x)
fig = go.Figure(
    data=[go.Table(
        header=dict(values=list(zshb.columns),  # 表头取值是data列属性
                    fill_color='paleturquoise',align=['center','center'],font_size=17,
        height=60),  # 填充色和文本位置
                
        cells=dict(values=[zshb.指数,zshb.当日涨幅,zshb.累计5日涨幅,zshb.累计10日涨幅,zshb.累计20日涨幅,zshb.累计60日涨幅,zshb.累计120日涨幅,zshb.累计250日涨幅],  # 单元格的取值就是每个列属性的Series取值
                   fill_color='lavender',align=['center','right'],font_size=22,
        height=60)
    )]
)
fig.update_layout(width=1200,height=600)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zshb.png',scale=3)

# 指数资金
# 缺失值赋0
zszj0.fillna(0,inplace=True)
zszj0['NAME'] = zszj0['NAME'].str.replace('指数', '')
zszj0['NETINFLOW'] = zszj0['NETINFLOW']/100000000
fig = px.bar(zszj0,x='NAME',y='NETINFLOW',text='NETINFLOW')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(zszj0['NETINFLOW'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "当日指数资金（亿元）",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zszj0.png',scale=3)

# 资金数据合并
zszj3=pd.concat([zszj0,zszj1,zszj2],names=None,axis=1,ignore_index=True)
zszj3['zszj3']=zszj3[3]+zszj3[7]+zszj3[11]
zszj3['zszj3'] = zszj3['zszj3']/100000000
# 删除无用列
zszj3.drop(zszj3.columns[[0,1,4,5,6,8,9,10]],axis = 1,inplace = True)
# 变更列名
zszj3.columns=['指数', 'zszj0', 'zszj1', 'zszj2', 'zszj3']
# 删除特定字符
zszj3['指数'] = zszj3['指数'].str.replace('指数', '')

fig = px.bar(zszj3,x='指数',y='zszj3',text='zszj3')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(zszj3['zszj3'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "3日指数资金（亿元）",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zszj3.png',scale=3)

# 指数走势
# 变更列名
zszs.columns=['指数','日期','收盘价']
zszs['指数'] = zszs['指数'].str.replace('000985.CSI','中证全指')
zszs['指数'] = zszs['指数'].str.replace('000300.SH','沪深300')
zszs['指数'] = zszs['指数'].str.replace('000905.SH','中证500')
zszs['指数'] = zszs['指数'].str.replace('000852.SH','中证1000')
fig = px.line(zszs,x='日期', y='收盘价',color='指数')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=1200,height=600,title={'text': "指数走势",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zszs.png',scale=3)

# 3年指数走势
# 变更列名
zszs3.columns=['指数','日期','收盘价']
zszs3['指数'] = zszs3['指数'].str.replace('000985.CSI','中证全指')
zszs3['指数'] = zszs3['指数'].str.replace('000300.SH','沪深300')
zszs3['指数'] = zszs3['指数'].str.replace('000905.SH','中证500')
zszs3['指数'] = zszs3['指数'].str.replace('000852.SH','中证1000')
fig = px.line(zszs3,x='日期', y='收盘价',color='指数')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 120,),width=1200,height=600,title={'text': "3年指数走势",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zszs3.png',scale=3)

# 风格涨幅
# 缺失值赋0
fg0.fillna(0,inplace=True)
fg0['NAME'] = fg0['NAME'].str.replace('巨潮', '')
fg0['NAME'] = fg0['NAME'].str.replace('指数', '')
fig = px.bar(fg0,x='NAME',y='DIFFERRANGE',text='DIFFERRANGE')
fig.update_traces(texttemplate='%{text:.1f}',textposition='inside',marker=dict(color=np.where(np.array(fg0['DIFFERRANGE'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "当日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fg0.png',scale=3)

fg5['NAME'] = fg5['NAME'].str.replace('巨潮', '')
fg5['NAME'] = fg5['NAME'].str.replace('指数', '')
fig = px.bar(fg5,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(fg5['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计5日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fg5.png',scale=3)

fg10['NAME'] = fg10['NAME'].str.replace('巨潮', '')
fg10['NAME'] = fg10['NAME'].str.replace('指数', '')
fig = px.bar(fg10,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(fg10['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计10日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fg10.png',scale=3)

fg20['NAME'] = fg20['NAME'].str.replace('巨潮', '')
fg20['NAME'] = fg20['NAME'].str.replace('指数', '')
fig = px.bar(fg20,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(fg20['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计20日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fg20.png',scale=3)

fg60['NAME'] = fg60['NAME'].str.replace('巨潮', '')
fg60['NAME'] = fg60['NAME'].str.replace('指数', '')
fig = px.bar(fg60,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(fg60['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计60日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fg60.png',scale=3)

fg120['NAME'] = fg120['NAME'].str.replace('巨潮', '')
fg120['NAME'] = fg120['NAME'].str.replace('指数', '')
fig = px.bar(fg120,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(fg120['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计120日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fg120.png',scale=3)

fg250['NAME'] = fg250['NAME'].str.replace('巨潮', '')
fg250['NAME'] = fg250['NAME'].str.replace('指数', '')
fig = px.bar(fg250,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(fg250['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计250日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fg250.png',scale=3)

#风格涨幅表格
# 数据合并
fghb=pd.concat([fg0,fg5,fg10,fg20,fg60,fg120,fg250],names=None,axis=1,ignore_index=True) 
# 删除无用列
fghb.drop(fghb.columns[[0,1,4,5,6,8,9,10,12,13,14,16,17,18,20,21,22,24,25,26]],axis = 1,inplace = True)
# 变更列名
fghb.columns=['风格指数', '当日涨幅', '累计5日涨幅', '累计10日涨幅', '累计20日涨幅', '累计60日涨幅', '累计120日涨幅', '累计250日涨幅']
# 删除特定字符
fghb.风格指数 = fghb.风格指数.str.replace('巨潮', '')
fghb.风格指数 = fghb.风格指数.str.replace('指数', '')
# 设置小数位
fghb.当日涨幅=fghb.当日涨幅.map(lambda x:('%.1f')%x)
fghb.累计5日涨幅=fghb.累计5日涨幅.map(lambda x:('%.0f')%x)
fghb.累计10日涨幅=fghb.累计10日涨幅.map(lambda x:('%.0f')%x)
fghb.累计20日涨幅=fghb.累计20日涨幅.map(lambda x:('%.0f')%x)
fghb.累计60日涨幅=fghb.累计60日涨幅.map(lambda x:('%.0f')%x)
fghb.累计120日涨幅=fghb.累计120日涨幅.map(lambda x:('%.0f')%x)
fghb.累计250日涨幅=fghb.累计250日涨幅.map(lambda x:('%.0f')%x)

fig = go.Figure(
data=[go.Table(
    header=dict(values=list(fghb.columns),  # 表头取值是data列属性
                fill_color='paleturquoise',align=['center','center'],font_size=17,
    height=60),  # 填充色和文本位置
            
    cells=dict(values=[fghb.风格指数,fghb.当日涨幅,fghb.累计5日涨幅,fghb.累计10日涨幅,fghb.累计20日涨幅,fghb.累计60日涨幅,fghb.累计120日涨幅,fghb.累计250日涨幅],  # 单元格的取值就是每个列属性的Series取值
                fill_color='lavender',align=['center','right'],font_size=22,
    height=60)
)]
)
fig.update_layout(width=1200,height=600)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fghb.png',scale=3)

# 风格资金
# 缺失值赋0
fgzj0.fillna(0,inplace=True)
fgzj0['NAME'] = fgzj0['NAME'].str.replace('巨潮', '')
fgzj0['NAME'] = fgzj0['NAME'].str.replace('指数', '')
fgzj0['NETINFLOW'] = fgzj0['NETINFLOW']/100000000
fig = px.bar(fgzj0,x='NAME',y='NETINFLOW',text='NETINFLOW')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(fgzj0['NETINFLOW'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "当日风格资金（亿元）",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fgzj0.png',scale=3)

# 资金数据合并
fgzj3=pd.concat([fgzj0,fgzj1,fgzj2],names=None,axis=1,ignore_index=True)
fgzj3['fgzj3']=fgzj3[3]+fgzj3[7]+fgzj3[11]
fgzj3['fgzj3'] = fgzj3['fgzj3']/100000000
# 删除无用列
fgzj3.drop(fgzj3.columns[[0,1,4,5,6,8,9,10]],axis = 1,inplace = True)
# 变更列名
fgzj3.columns=['指数', 'fgzj0', 'fgzj1', 'fgzj2', 'fgzj3']
# 删除特定字符
fgzj3['指数'] = fgzj3['指数'].str.replace('巨潮', '')
fgzj3['指数'] = fgzj3['指数'].str.replace('指数', '')

fig = px.bar(fgzj3,x='指数',y='fgzj3',text='fgzj3')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(fgzj3['fgzj3'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "3日风格资金（亿元）",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fgzj3.png',scale=3)

# 风格走势
# 变更列名
fgzs.columns=['风格','日期','收盘价']
fgzs['风格'] = fgzs['风格'].str.replace('399373.SZ','大盘价值')
fgzs['风格'] = fgzs['风格'].str.replace('399377.SZ','小盘价值')
fgzs['风格'] = fgzs['风格'].str.replace('399372.SZ','大盘成长')
fgzs['风格'] = fgzs['风格'].str.replace('399376.SZ','小盘成长')
fig = px.line(fgzs,x='日期', y='收盘价',color='风格')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=1200,height=600,title={'text': "风格走势",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fgzs.png',scale=3)

# 3年风格走势
# 变更列名
fgzs3.columns=['风格','日期','收盘价']
fgzs3['风格'] = fgzs3['风格'].str.replace('399373.SZ','大盘价值')
fgzs3['风格'] = fgzs3['风格'].str.replace('399377.SZ','小盘价值')
fgzs3['风格'] = fgzs3['风格'].str.replace('399372.SZ','大盘成长')
fgzs3['风格'] = fgzs3['风格'].str.replace('399376.SZ','小盘成长')
fig = px.line(fgzs3,x='日期', y='收盘价',color='风格')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=1200,height=600,title={'text': "3年风格走势",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fgzs3.png',scale=3)

# 行业风格涨幅
# 缺失值赋0
hyfg0.fillna(0,inplace=True)
hyfg0['NAME'] = hyfg0['NAME'].str.replace('(风格.中信)', '')
fig = px.bar(hyfg0,x='NAME',y='DIFFERRANGE',text='DIFFERRANGE')
fig.update_traces(texttemplate='%{text:.1f}',textposition='inside',marker=dict(color=np.where(np.array(hyfg0['DIFFERRANGE'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "当日涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hyfg0.png',scale=3)

hyfg5['NAME'] = hyfg5['NAME'].str.replace('(风格.中信)', '')
fig = px.bar(hyfg5,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(hyfg5['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计5日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hyfg5.png',scale=3)

hyfg10['NAME'] = hyfg10['NAME'].str.replace('(风格.中信)', '')
fig = px.bar(hyfg10,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(hyfg10['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计10日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hyfg10.png',scale=3)

hyfg20['NAME'] = hyfg20['NAME'].str.replace('(风格.中信)', '')
fig = px.bar(hyfg20,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(hyfg20['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计20日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hyfg20.png',scale=3)

hyfg60['NAME'] = hyfg60['NAME'].str.replace('(风格.中信)', '')
fig = px.bar(hyfg60,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(hyfg60['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计60日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hyfg60.png',scale=3)

hyfg120['NAME'] = hyfg120['NAME'].str.replace('(风格.中信)', '')
fig = px.bar(hyfg120,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(hyfg120['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计120日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hyfg120.png',scale=3)

hyfg250['NAME'] = hyfg250['NAME'].str.replace('(风格.中信)', '')
fig = px.bar(hyfg250,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(hyfg250['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计250日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hyfg250.png',scale=3)

# 数据合并
hyfghb=pd.concat([hyfg0,hyfg5,hyfg10,hyfg20,hyfg60,hyfg120,hyfg250],names=None,axis=1,ignore_index=True) 
# 删除无用列
hyfghb.drop(hyfghb.columns[[0,1,4,5,6,8,9,10,12,13,14,16,17,18,20,21,22,24,25,26]],axis = 1,inplace = True)
# 变更列名
hyfghb.columns=['行业风格指数', '当日涨幅', '累计5日涨幅', '累计10日涨幅', '累计20日涨幅', '累计60日涨幅', '累计120日涨幅', '累计250日涨幅']
# 删除特定字符
hyfghb.行业风格指数 = hyfghb.行业风格指数.str.replace('(风格.中信)', '')
# 设置小数位
hyfghb.当日涨幅=hyfghb.当日涨幅.map(lambda x:('%.1f')%x)
hyfghb.累计5日涨幅=hyfghb.累计5日涨幅.map(lambda x:('%.0f')%x)
hyfghb.累计10日涨幅=hyfghb.累计10日涨幅.map(lambda x:('%.0f')%x)
hyfghb.累计20日涨幅=hyfghb.累计20日涨幅.map(lambda x:('%.0f')%x)
hyfghb.累计60日涨幅=hyfghb.累计60日涨幅.map(lambda x:('%.0f')%x)
hyfghb.累计120日涨幅=hyfghb.累计120日涨幅.map(lambda x:('%.0f')%x)
hyfghb.累计250日涨幅=hyfghb.累计250日涨幅.map(lambda x:('%.0f')%x)
print(hyfghb)
fig = go.Figure(
    data=[go.Table(
        header=dict(values=list(hyfghb.columns),  # 表头取值是data列属性
                    fill_color='paleturquoise',align=['center','center'],font_size=17,
        height=60),  # 填充色和文本位置
                
        cells=dict(values=[hyfghb.行业风格指数,hyfghb.当日涨幅,hyfghb.累计5日涨幅,hyfghb.累计10日涨幅,hyfghb.累计20日涨幅,hyfghb.累计60日涨幅,hyfghb.累计120日涨幅,hyfghb.累计250日涨幅],  # 单元格的取值就是每个列属性的Series取值
                   fill_color='lavender',align=['center','right'],font_size=22,
        height=60)
    )]
)
fig.update_layout(width=1200,height=600)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hyfghb.png',scale=3)

# 行业风格资金
# 缺失值赋0
hyfgzj0.fillna(0,inplace=True)
hyfgzj0['NAME'] = hyfgzj0['NAME'].str.replace('(风格.中信)', '')
hyfgzj0['NETINFLOW'] = hyfgzj0['NETINFLOW']/100000000
fig = px.bar(hyfgzj0,x='NAME',y='NETINFLOW',text='NETINFLOW')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(hyfgzj0['NETINFLOW'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "当日行业风格资金（亿元）",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hyfgzj0.png',scale=3)

# 资金数据合并
hyfgzj3=pd.concat([hyfgzj0,hyfgzj1,hyfgzj2],names=None,axis=1,ignore_index=True)
hyfgzj3['hyfgzj3']=hyfgzj3[3]+hyfgzj3[7]+hyfgzj3[11]
hyfgzj3['hyfgzj3'] = hyfgzj3['hyfgzj3']/100000000
# 删除无用列
hyfgzj3.drop(hyfgzj3.columns[[0,1,4,5,6,8,9,10]],axis = 1,inplace = True)
# 变更列名
hyfgzj3.columns=['指数', 'hyfgzj0', 'hyfgzj1', 'hyfgzj2', 'hyfgzj3']
# 删除特定字符
hyfgzj3['指数'] = hyfgzj3['指数'].str.replace('(风格.中信)', '')

fig = px.bar(hyfgzj3,x='指数',y='hyfgzj3',text='hyfgzj3')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(hyfgzj3['hyfgzj3'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "3日行业风格资金（亿元）",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hyfgzj3.png',scale=3)

# 行业风格走势
# 变更列名
hyfgzs.columns=['行业风格','日期','收盘价']
hyfgzs['行业风格'] = hyfgzs['行业风格'].str.replace('CI005917.CI','金融')
hyfgzs['行业风格'] = hyfgzs['行业风格'].str.replace('CI005918.CI','周期')
hyfgzs['行业风格'] = hyfgzs['行业风格'].str.replace('CI005919.CI','消费')
hyfgzs['行业风格'] = hyfgzs['行业风格'].str.replace('CI005920.CI','成长')
hyfgzs['行业风格'] = hyfgzs['行业风格'].str.replace('CI005921.CI','稳定')
fig = px.line(hyfgzs,x='日期', y='收盘价',color='行业风格')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=1200,height=600,title={'text': "行业风格走势",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hyfgzs.png',scale=3)

# 3年行业风格走势
# 变更列名
hyfgzs3.columns=['行业风格','日期','收盘价']
hyfgzs3['行业风格'] = hyfgzs3['行业风格'].str.replace('CI005917.CI','金融')
hyfgzs3['行业风格'] = hyfgzs3['行业风格'].str.replace('CI005918.CI','周期')
hyfgzs3['行业风格'] = hyfgzs3['行业风格'].str.replace('CI005919.CI','消费')
hyfgzs3['行业风格'] = hyfgzs3['行业风格'].str.replace('CI005920.CI','成长')
hyfgzs3['行业风格'] = hyfgzs3['行业风格'].str.replace('CI005921.CI','稳定')
fig = px.line(hyfgzs3,x='日期', y='收盘价',color='行业风格')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 120,),width=1200,height=600,title={'text': "3年行业风格走势",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hyfgzs3.png',scale=3)

# 行业涨幅
# 缺失值赋0
hy0.fillna(0,inplace=True)
hy0['NAME'] = hy0['NAME'].str.replace('申万一级', '')
hy0['NAME'] = hy0['NAME'].str.replace('指数', '')
fig = px.bar(hy0,x='NAME',y='DIFFERRANGE',text='DIFFERRANGE')
fig.update_traces(texttemplate='%{text:.1f}',textposition='inside',marker=dict(color=np.where(np.array(hy0['DIFFERRANGE'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "当日涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=35,font_size=20,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hy0.png',scale=3)

hy5['NAME'] = hy5['NAME'].str.replace('申万一级', '')
hy5['NAME'] = hy5['NAME'].str.replace('指数', '')
fig = px.bar(hy5,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(hy5['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计5日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=35,font_size=20,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hy5.png',scale=3)

hy10['NAME'] = hy10['NAME'].str.replace('申万一级', '')
hy10['NAME'] = hy10['NAME'].str.replace('指数', '')
fig = px.bar(hy10,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(hy10['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计10日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=35,font_size=20,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hy10.png',scale=3)

hy20['NAME'] = hy20['NAME'].str.replace('申万一级', '')
hy20['NAME'] = hy20['NAME'].str.replace('指数', '')
fig = px.bar(hy20,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(hy20['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计20日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=35,font_size=20,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hy20.png',scale=3)

hy60['NAME'] = hy60['NAME'].str.replace('申万一级', '')
hy60['NAME'] = hy60['NAME'].str.replace('指数', '')
fig = px.bar(hy60,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(hy60['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计60日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=35,font_size=20,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hy60.png',scale=3)

hy120['NAME'] = hy120['NAME'].str.replace('申万一级', '')
hy120['NAME'] = hy120['NAME'].str.replace('指数', '')
fig = px.bar(hy120,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(hy120['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计120日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=35,font_size=20,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hy120.png',scale=3)

hy250['NAME'] = hy250['NAME'].str.replace('申万一级', '')
hy250['NAME'] = hy250['NAME'].str.replace('指数', '')
fig = px.bar(hy250,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(hy250['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "累计250日涨幅",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=35,font_size=20,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hy250.png',scale=3)

# 行业资金
# 缺失值赋0
hyzj0.fillna(0,inplace=True)
hyzj0['NAME'] = hyzj0['NAME'].str.replace('申万一级', '')
hyzj0['NAME'] = hyzj0['NAME'].str.replace('指数', '')
hyzj0['NETINFLOW'] = hyzj0['NETINFLOW']/100000000
hyzj0 = hyzj0.sort_values(by="NETINFLOW",ascending=False)
fig = px.bar(hyzj0,x='NAME',y='NETINFLOW',text='NETINFLOW')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(hyzj0['NETINFLOW'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "当日行业风格资金（亿元）",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=35,font_size=20,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hyzj0.png',scale=3)

# 资金数据合并
hyzj3=pd.concat([hyzj0,hyzj1,hyzj2],names=None,axis=1,ignore_index=True)
hyzj3['hyzj3']=hyzj3[3]+hyzj3[7]+hyzj3[11]
hyzj3['hyzj3'] = hyzj3['hyzj3']/100000000
# 删除无用列
hyzj3.drop(hyzj3.columns[[0,1,4,5,6,8,9,10]],axis = 1,inplace = True)
# 变更列名
hyzj3.columns=['指数', 'hyzj0', 'hyzj1', 'hyzj2', 'hyzj3']
# 删除特定字符
hyzj3['指数'] = hyzj3['指数'].str.replace('申万一级', '')
hyzj3['指数'] = hyzj3['指数'].str.replace('指数', '')
# 排序
hyzj3 = hyzj3.sort_values(by="hyzj3",ascending=False)
fig = px.bar(hyzj3,x='指数',y='hyzj3',text='hyzj3')
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(hyzj3['hyzj3'])>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "3日行业风格资金（亿元）",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=35,font_size=20,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hyzj3.png',scale=3)

# 投资策略
# PB
fig = px.line(zspb,x='DATES',y='PBLYR')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=1200,height=600,title={'text': "A股PB",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\1agpb.png',scale=3)

# 3年PB
fig = px.line(zspb3,x='DATES',y='PBLYR')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 120,),width=1200,height=600,title={'text': "3年A股PB",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\1agpb3.png',scale=3)

# PE
fig = px.line(zspe,x='DATES',y='PETTM')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=1200,height=600,title={'text': "A股PETTM",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\2agpe.png',scale=3)

# 3年PE
fig = px.line(zspe3,x='DATES',y='PETTM')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 120,),width=1200,height=600,title={'text': "3年A股PETTM",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\2agpe3.png',scale=3)

# 小盘大盘比
df = pd.concat([xp,dp],names=None,axis=1,ignore_index=True)
# 计算比值
df['xpdp'] = df.iloc[:,2]/df.iloc[:,5]
# 数据重组
df = df.iloc[:,[1,6]]
# 变更列名
df.columns=['日期', '小盘大盘比']
fig = px.line(df,x='日期', y='小盘大盘比')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=1200,height=600,title={'text': "小盘大盘比",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\3xpdp.png',scale=3)

# 小盘大盘比
df = pd.concat([xp3,dp3],names=None,axis=1,ignore_index=True)
# 计算比值
df['xpdp'] = df.iloc[:,2]/df.iloc[:,5]
# 数据重组
df = df.iloc[:,[1,6]]
# 变更列名
df.columns=['日期', '小盘大盘比']
fig = px.line(df,x='日期', y='小盘大盘比')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 120,),width=1200,height=600,title={'text': "3年小盘大盘比",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\3xpdp3.png',scale=3)

# 成长价值比
df = pd.concat([cz,jz],names=None,axis=1,ignore_index=True)
# 计算比值
df['czjz'] = df.iloc[:,2]/df.iloc[:,5]
# 数据重组
df = df.iloc[:,[1,6]]
# 变更列名
df.columns=['日期','成长价值比']
fig = px.line(df,x='日期', y='成长价值比')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=1200,height=600,title={'text': "成长价值比",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.update_traces(texttemplate='%{text:.1f}',textposition='top center')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\4czjz.png',scale=3)

# 3年成长价值比
df = pd.concat([cz3,jz3],names=None,axis=1,ignore_index=True)
# 计算比值
df['czjz'] = df.iloc[:,2]/df.iloc[:,5]
# 数据重组
df = df.iloc[:,[1,6]]
# 变更列名
df.columns=['日期','成长价值比']
fig = px.line(df,x='日期', y='成长价值比')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 120,),width=1200,height=600,title={'text': "3年成长价值比",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.update_traces(texttemplate='%{text:.1f}',textposition='top center')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\4czjz3.png',scale=3)

from reportlab.pdfbase import pdfmetrics   # 注册字体
from reportlab.pdfbase.ttfonts import TTFont # 字体类
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph, Image  # 报告内容相关类
from reportlab.lib.pagesizes import letter  # 页面的标志尺寸(8.5*inch, 11*inch)
from reportlab.lib.styles import getSampleStyleSheet  # 文本样式
from reportlab.lib import colors  # 颜色模块
from reportlab.graphics.charts.barcharts import VerticalBarChart  # 图表类
from reportlab.graphics.charts.legends import Legend  # 图例类
from reportlab.graphics.shapes import Drawing  # 绘图工具
from reportlab.lib.units import cm  # 单位：cm
from datetime import timedelta, datetime
import time as _time
import traceback
from datetime import *

# 注册字体(提前准备好字体文件, 如果同一个文件需要多种字体可以注册多个)
pdfmetrics.registerFont(TTFont('SimSun', 'simsun.ttf'))

class Graphs:
    
    # 绘制标题
    @staticmethod
    def draw_title(title: str):
        # 获取所有样式表
        style = getSampleStyleSheet()
        # 拿到标题样式
        ct = style['Heading1']
        # 单独设置样式相关属性
        ct.fontName = 'SimSun'      # 字体名
        ct.fontSize = 25            # 字体大小
        ct.leading = 30             # 行间距
        ct.textColor = colors.red     # 字体颜色
        ct.alignment = 1    # 居中
        ct.bold = True
        # 创建标题对应的段落，并且返回
        return Paragraph(title,ct)    

    @staticmethod
    def draw_title1(title: str):
        # 获取所有样式表
        style = getSampleStyleSheet()
        # 拿到标题样式
        ct = style['Heading1']
        # 单独设置样式相关属性
        ct.fontName = 'SimSun'      # 字体名
        ct.fontSize = 20            # 字体大小
        ct.leading = 30             # 行间距
        ct.textColor = colors.red     # 字体颜色
        ct.alignment = 2    # 居中
        ct.bold = True
        # 创建标题对应的段落，并且返回
        return Paragraph(title,ct)    

    # 绘制小标题
    @staticmethod
    def draw_little_title(title: str):
        # 获取所有样式表
        style = getSampleStyleSheet()
        # 拿到标题样式
        ct = style['Normal']
        # 单独设置样式相关属性
        ct.fontName = 'SimSun'  # 字体名
        ct.fontSize = 20  # 字体大小
        ct.leading = 20  # 行间距
        ct.textColor = colors.red  # 字体颜色
        # 创建标题对应的段落，并且返回
        return Paragraph(title, ct)
    
    @staticmethod
    def draw_little_title1(title: str):
        # 获取所有样式表
        style = getSampleStyleSheet()
        # 拿到标题样式
        ct = style['Normal']
        # 单独设置样式相关属性
        ct.fontName = 'SimSun'  # 字体名
        ct.fontSize = 20  # 字体大小
        ct.leading = 40  # 行间距
        ct.textColor = colors.red  # 字体颜色
        # 创建标题对应的段落，并且返回
        return Paragraph(title, ct)

    @staticmethod
    def draw_little_title2(title: str):
        # 获取所有样式表
        style = getSampleStyleSheet()
        # 拿到标题样式
        ct = style['Normal']
        # 单独设置样式相关属性
        ct.fontName = 'SimSun'  # 字体名
        ct.fontSize = 20  # 字体大小
        ct.leading = 40  # 行间距
        ct.textColor = colors.red  # 字体颜色
        ct.alignment = 1    # 居中
        # 创建标题对应的段落，并且返回
        return Paragraph(title, ct)

    # 绘制图片
    @staticmethod
    def draw_img(path):
        img = Image(path)       # 读取指定路径下的图片
        img.drawWidth = 22*cm        # 设置图片的宽度
        img.drawHeight = 10*cm       # 设置图片的高度
        return img

    @staticmethod
    def draw_img1(path):
        img1 = Image(path)       # 读取指定路径下的图片
        img1.drawWidth = 22*cm        # 设置图片的宽度
        img1.drawHeight = 11*cm       # 设置图片的高度
        return img1

    @staticmethod
    def draw_img2(path):
        img2 = Image(path)       # 读取指定路径下的图片
        img2.drawWidth = 22*cm        # 设置图片的宽度
        img2.drawHeight = 11*cm       # 设置图片的高度
        return img2

date = (datetime.today() + timedelta(days = -0)).strftime("%Y-%m-%d")

if __name__ == '__main__':
    # 创建内容对应的空列表
    content = list()

    content.append(Graphs.draw_title('金融市场日报'))
    content.append(Graphs.draw_little_title2(date))
    
    content.append(Graphs.draw_little_title('目录'))
    content.append(Graphs.draw_little_title('★一、市场特征'))
    content.append(Graphs.draw_little_title('1、指数涨幅'))
    content.append(Graphs.draw_little_title('2、指数资金'))
    content.append(Graphs.draw_little_title('3、指数走势'))
    content.append(Graphs.draw_little_title('4、风格涨幅'))
    content.append(Graphs.draw_little_title('5、风格资金'))
    content.append(Graphs.draw_little_title('6、风格走势'))
    content.append(Graphs.draw_little_title('7、行业风格涨幅'))
    content.append(Graphs.draw_little_title('8、行业风格资金'))
    content.append(Graphs.draw_little_title('9、行业风格走势'))
    content.append(Graphs.draw_little_title('10、行业涨幅'))
    content.append(Graphs.draw_little_title('11、行业资金'))
    content.append(Graphs.draw_little_title('★二、投资策略'))
    content.append(Graphs.draw_little_title('1、A股PB'))
    content.append(Graphs.draw_little_title('2、A股PE'))
    content.append(Graphs.draw_little_title('3、小盘大盘比'))
    content.append(Graphs.draw_little_title('4、成长价值比'))

    
    content.append(Graphs.draw_little_title('★1、指数涨幅'))
    content.append(Graphs.draw_img2(r'C:\xyzy\1lhjr\1scrb\zshb.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zs0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zs5.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zs10.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zs20.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zs60.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zs120.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zs250.png'))
    
    content.append(Graphs.draw_little_title('★2、指数资金'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zszj0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zszj3.png'))

    content.append(Graphs.draw_little_title('★3、指数走势'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zszs.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zszs3.png'))

    content.append(Graphs.draw_little_title('★4、风格涨幅'))
    content.append(Graphs.draw_img2(r'C:\xyzy\1lhjr\1scrb\fghb.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fg0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fg5.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fg10.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fg20.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fg60.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fg120.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fg250.png'))

    content.append(Graphs.draw_little_title('★5、风格资金'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fgzj0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fgzj3.png'))

    content.append(Graphs.draw_little_title('★6、风格走势'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fgzs.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fgzs3.png'))

    content.append(Graphs.draw_little_title('★7、行业风格涨幅'))
    content.append(Graphs.draw_img2(r'C:\xyzy\1lhjr\1scrb\hyfghb.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hyfg0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hyfg5.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hyfg10.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hyfg20.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hyfg60.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hyfg120.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hyfg250.png'))

    content.append(Graphs.draw_little_title('★8、行业风格资金'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hyfgzj0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hyfgzj3.png'))

    content.append(Graphs.draw_little_title('★9、行业风格走势'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hyfgzs.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hyfgzs3.png'))

    content.append(Graphs.draw_little_title('★10、行业涨幅'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hy0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hy5.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hy10.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hy20.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hy60.png'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\1scrb\hy120.png'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\1scrb\hy250.png'))

    content.append(Graphs.draw_little_title('★11、行业资金'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hyzj0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hyzj3.png'))

    content.append(Graphs.draw_little_title('★二、投资策略'))
    content.append(Graphs.draw_little_title('★1、A股PB'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\1agpb.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\1agpb3.png'))
    content.append(Graphs.draw_little_title('★2、A股PE'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\2agpe.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\2agpe3.png'))
    content.append(Graphs.draw_little_title('★3、小盘大盘比'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\3xpdp.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\3xpdp3.png'))
    content.append(Graphs.draw_little_title('★4、成长价值比'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\4czjz.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\4czjz3.png'))

    content.append(Graphs.draw_title1('数据来源：Choice  报告工具：Python'))

    # 生成pdf文件
    doc = SimpleDocTemplate(r'C:\xyzy\1lhjr\1scrb\ribao.pdf', pagesize=letter)
    doc.build(content)