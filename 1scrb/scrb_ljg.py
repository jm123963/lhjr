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
    zs0=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGE","N=-0,TradeDate="+date+",AdjustFlag=1,Ispandas=1")    
    zs5=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    zs10=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    zs20=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    zs60=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    zs120=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    zs250=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    # 指数 （日）主力净流入资金
    date = (datetime.today() + timedelta(days = -0)).strftime("%Y-%m-%d")
    zszj0=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    date = (datetime.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
    zszj1=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    date = (datetime.today() + timedelta(days = -2)).strftime("%Y-%m-%d")
    zszj2=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    # 指数走势
    date = datetime.today().strftime("%Y-%m-%d")
    zszs=c.csd("000985.CSI,000300.SH,000905.SH,000852.SH","CLOSE","2005-01-01",""+date+"","period=3,adjustflag=3,curtype=1,order=1,market=CNSESH,Ispandas=1")
    zszs3=c.csd("000985.CSI,000300.SH,000905.SH,000852.SH","CLOSE","2020-01-01",""+date+"","period=1,adjustflag=3,curtype=1,order=1,market=CNSESH,Ispandas=1")
    # 指数估值
    zspb=c.csd("000985.CSI,000300.SH,000905.SH,000852.SH","PBMRQ","2013-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    zspb3=c.csd("000985.CSI,000300.SH,000905.SH,000852.SH","PBMRQ","2020-01-01",""+date+"","DelType=1,period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    zspbclose=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","SHORTNAME,PBMRQ","TradeDate="+date+",DelType=1,Ispandas=1")

    # 风格涨幅
    date = datetime.today().strftime("%Y-%m-%d")
    fg0=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGE","N=0,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    fg5=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    fg10=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    fg20=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    fg60=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    fg120=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    fg250=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    # 风格资金
    date = (datetime.today() + timedelta(days = -0)).strftime("%Y-%m-%d")
    fgzj0=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    date = (datetime.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
    fgzj1=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    date = (datetime.today() + timedelta(days = -2)).strftime("%Y-%m-%d")
    fgzj2=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    # 风格走势
    date = datetime.today().strftime("%Y-%m-%d")
    fgzs=c.csd("399373.SZ,399377.SZ,399372.SZ,399376.SZ","CLOSE","2003-01-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    fgzs3=c.csd("399373.SZ,399377.SZ,399372.SZ,399376.SZ","CLOSE","2020-01-01",""+date+"","period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    # 风格估值
    zspb=c.csd("399373.SZ,399377.SZ,399372.SZ,399376.SZ","PBMRQ","2013-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    zspb3=c.csd("399373.SZ,399377.SZ,399372.SZ,399376.SZ","PBMRQ","2020-01-01",""+date+"","DelType=1,period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    zspbclose=c.css("399373.SZ,399377.SZ,399372.SZ,399376.SZ","SHORTNAME,PBMRQ","TradeDate="+date+",DelType=1,Ispandas=1")

    # 行业风格涨幅
    date = datetime.today().strftime("%Y-%m-%d")
    hyfg0=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,DIFFERRANGE","N=0,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    hyfg5=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    hyfg10=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    hyfg20=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    hyfg60=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    hyfg120=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    hyfg250=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    # 行业风格资金
    date = (datetime.today() + timedelta(days = -0)).strftime("%Y-%m-%d")
    hyfgzj0=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    date = (datetime.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
    hyfgzj1=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    date = (datetime.today() + timedelta(days = -2)).strftime("%Y-%m-%d")
    hyfgzj2=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    # 行业风格走势
    date = datetime.today().strftime("%Y-%m-%d")
    hyfgzs =c.csd("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","CLOSE","2003-01-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    hyfgzs3 =c.csd("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","CLOSE","2020-01-01",""+date+"","period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    # 行业风格估值
    zspb=c.csd("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","PBMRQ","2013-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    zspb3=c.csd("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","PBMRQ","2020-01-01",""+date+"","DelType=1,period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    zspbclose=c.css("CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI","SHORTNAME,PBMRQ","TradeDate="+date+",DelType=1,Ispandas=1")

    # 行业涨幅
    date = datetime.today().strftime("%Y-%m-%d")
    hy0=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGE","N=-0,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    hy0=hy0.sort_values(by="DIFFERRANGE",ascending=False)
    hy5=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    hy5=hy5.sort_values(by="DIFFERRANGEN",ascending=False)
    hy10=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    hy10=hy10.sort_values(by="DIFFERRANGEN",ascending=False)
    hy20=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    hy20=hy20.sort_values(by="DIFFERRANGEN",ascending=False)
    hy60=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    hy60=hy60.sort_values(by="DIFFERRANGEN",ascending=False)
    hy120=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    hy120=hy120.sort_values(by="DIFFERRANGEN",ascending=False)
    hy250=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    hy250=hy250.sort_values(by="DIFFERRANGEN",ascending=False)
    # 行业资金
    date = (datetime.today() + timedelta(days = -0)).strftime("%Y-%m-%d")
    hyzj0=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    hyzj = hyzj0.sort_values(by="NETINFLOW",ascending=False)
    date = (datetime.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
    hyzj1=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    date = (datetime.today() + timedelta(days = -2)).strftime("%Y-%m-%d")
    hyzj2=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    # 行业走势
    date = datetime.today().strftime("%Y-%m-%d")
    hyzs =c.csd("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","CLOSE","2003-01-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    hyzs3 =c.csd("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","CLOSE","2020-01-01",""+date+"","period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    # 行业市净率PB(MRQ) 
    hypb=c.csd("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","PBMRQ","2013-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    hypb3=c.csd("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","PBMRQ","2020-01-01",""+date+"","DelType=1,period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    hypbclose=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","SHORTNAME,PBMRQ","TradeDate="+date+",DelType=1,Ispandas=1")

    # 投资策略
    date = datetime.today().strftime("%Y-%m-%d")
    # 指数PB
    agpb=c.csd("000002.SH","PBLYR","2003-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    agpb3=c.csd("000002.SH","PBLYR","2020-01-01",""+date+"","DelType=1,period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")

    # 指数PE
    agpe=c.csd("000002.SH","PETTM","2003-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    agpe3=c.csd("000002.SH","PETTM","2020-01-01",""+date+"","DelType=1,period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")

    # 小盘大盘比
    xp=c.csd("399316.SZ","CLOSE","2003-01-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    dp=c.csd("399314.SZ","CLOSE","2003-01-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    xp3=c.csd("399316.SZ","CLOSE","2020-01-01",""+date+"","period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    dp3=c.csd("399314.SZ","CLOSE","2020-01-01",""+date+"","period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")

    # 成长价值比
    cz=c.csd("399370.SZ","CLOSE","2003-01-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    jz=c.csd("399371.SZ","CLOSE","2003-01-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    cz3=c.csd("399370.SZ","CLOSE","2020-01-01",""+date+"","period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    jz3=c.csd("399371.SZ","CLOSE","2020-01-01",""+date+"","period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")

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
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24),width=1200,height=600,title={'text': "指数走势",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
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

# 指数估值
# 分位图20年
# 变更特定字符
zspb['CODES'] = zspb['CODES'].str.replace('000985.CSI', '中证全指')
zspb['CODES'] = zspb['CODES'].str.replace('000300.SH', '沪深300')
zspb['CODES'] = zspb['CODES'].str.replace('000905.SH', '中证500')
zspb['CODES'] = zspb['CODES'].str.replace('000852.SH', '中证1000')
# 保留1位小数
zspbclose['PBMRQ'] = zspbclose['PBMRQ'].apply(lambda x:format(x,'.1f'))
y0 = zspbclose.PBMRQ[0]
y1 = zspbclose.PBMRQ[1]
y2 = zspbclose.PBMRQ[2]
y3 = zspbclose.PBMRQ[3]
fig = px.violin(zspb,x="CODES",y="PBMRQ",color="CODES",box=True,points='all')
fig.update_layout(width=1200,height=600,title={'text': "指数PB分位-10年",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                    title_font_size=35,font_size=15,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
#fig.update_yaxes(type='log')
fig.add_annotation(x=0,y=y0,text="现值{}".format(y0),ax=-55,ay=0)
fig.add_annotation(x=1,y=y1,text="现值{}".format(y1),ax=-55,ay=0)
fig.add_annotation(x=2,y=y2,text="现值{}".format(y2),ax=-55,ay=0)
fig.add_annotation(x=3,y=y3,text="现值{}".format(y3),ax=-55,ay=0)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zsPB1.png',scale=3)
# 走势图20年
fig = px.line(zspb,x='DATES', y='PBMRQ', color='CODES')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=1200,height=600,title={'text': "指数PB走势-10年",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zsPB2.png',scale=3)

# 分位图3年
# 变更特定字符
zspb3['CODES'] = zspb3['CODES'].str.replace('000985.CSI', '中证全指')
zspb3['CODES'] = zspb3['CODES'].str.replace('000300.SH', '沪深300')
zspb3['CODES'] = zspb3['CODES'].str.replace('000905.SH', '中证500')
zspb3['CODES'] = zspb3['CODES'].str.replace('000852.SH', '中证1000')

fig = px.violin(zspb3,x="CODES",y="PBMRQ",color="CODES",box=True,points='all')
fig.update_layout(width=1200,height=600,title={'text': "指数PB分位-3年",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                    title_font_size=35,font_size=15,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
#fig.update_yaxes(type='log')
fig.add_annotation(x=0,y=y0,text="现值{}".format(y0),ax=-55,ay=0)
fig.add_annotation(x=1,y=y1,text="现值{}".format(y1),ax=-55,ay=0)
fig.add_annotation(x=2,y=y2,text="现值{}".format(y2),ax=-55,ay=0)
fig.add_annotation(x=3,y=y3,text="现值{}".format(y3),ax=-55,ay=0)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zsPB31.png',scale=3)
# 走势图3年
fig = px.line(zspb3,x='DATES', y='PBMRQ', color='CODES')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 120,),width=1200,height=600,title={'text': "指数PB走势-3年",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zsPB32.png',scale=3)

# 风格涨幅
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

# 行业市净率PB(MRQ)20年
# 变更特定字符
hypb['CODES'] = hypb['CODES'].str.replace('801010.SWI', '农林牧渔')
hypb['CODES'] = hypb['CODES'].str.replace('801030.SWI', '基础化工')
hypb['CODES'] = hypb['CODES'].str.replace('801040.SWI', '钢铁')
hypb['CODES'] = hypb['CODES'].str.replace('801050.SWI', '有色金属')
hypb['CODES'] = hypb['CODES'].str.replace('801080.SWI', '电子')
hypb['CODES'] = hypb['CODES'].str.replace('801110.SWI', '家用电器')
hypb['CODES'] = hypb['CODES'].str.replace('801120.SWI', '食品饮料')
hypb['CODES'] = hypb['CODES'].str.replace('801130.SWI', '纺织服饰')
hypb['CODES'] = hypb['CODES'].str.replace('801140.SWI', '轻工制造')
hypb['CODES'] = hypb['CODES'].str.replace('801150.SWI', '医药生物')
hypb['CODES'] = hypb['CODES'].str.replace('801160.SWI', '公用事业')
hypb['CODES'] = hypb['CODES'].str.replace('801170.SWI', '交通运输')
hypb['CODES'] = hypb['CODES'].str.replace('801180.SWI', '房地产')
hypb['CODES'] = hypb['CODES'].str.replace('801200.SWI', '商贸零售')
hypb['CODES'] = hypb['CODES'].str.replace('801210.SWI', '社会服务')
hypb['CODES'] = hypb['CODES'].str.replace('801230.SWI', '综合')
hypb['CODES'] = hypb['CODES'].str.replace('801710.SWI', '建筑材料')
hypb['CODES'] = hypb['CODES'].str.replace('801720.SWI', '建筑装饰')
hypb['CODES'] = hypb['CODES'].str.replace('801730.SWI', '电力设备')
hypb['CODES'] = hypb['CODES'].str.replace('801740.SWI', '国防军工')
hypb['CODES'] = hypb['CODES'].str.replace('801750.SWI', '计算机')
hypb['CODES'] = hypb['CODES'].str.replace('801760.SWI', '传媒')
hypb['CODES'] = hypb['CODES'].str.replace('801770.SWI', '通信')
hypb['CODES'] = hypb['CODES'].str.replace('801780.SWI', '银行')
hypb['CODES'] = hypb['CODES'].str.replace('801790.SWI', '非银金融')
hypb['CODES'] = hypb['CODES'].str.replace('801880.SWI', '汽车')
hypb['CODES'] = hypb['CODES'].str.replace('801890.SWI', '机械设备')
hypb['CODES'] = hypb['CODES'].str.replace('801950.SWI', '煤炭')
hypb['CODES'] = hypb['CODES'].str.replace('801960.SWI', '石油石化')
hypb['CODES'] = hypb['CODES'].str.replace('801970.SWI', '环保')
hypb['CODES'] = hypb['CODES'].str.replace('801980.SWI', '美容护理')
# 保留1位小数
hypbclose['PBMRQ'] = hypbclose['PBMRQ'].apply(lambda x:format(x,'.1f'))

y0 = hypbclose.PBMRQ[0]
y1 = hypbclose.PBMRQ[1]
y2 = hypbclose.PBMRQ[2]
y3 = hypbclose.PBMRQ[3]
y4 = hypbclose.PBMRQ[4]
y5 = hypbclose.PBMRQ[5]
y6 = hypbclose.PBMRQ[6]
y7 = hypbclose.PBMRQ[7]
y8 = hypbclose.PBMRQ[8]
y9 = hypbclose.PBMRQ[9]
y10 = hypbclose.PBMRQ[10]
y11 = hypbclose.PBMRQ[11]
y12 = hypbclose.PBMRQ[12]
y13 = hypbclose.PBMRQ[13]
y14 = hypbclose.PBMRQ[14]
y15 = hypbclose.PBMRQ[15]
y16 = hypbclose.PBMRQ[16]
y17 = hypbclose.PBMRQ[17]
y18 = hypbclose.PBMRQ[18]
y19 = hypbclose.PBMRQ[19]
y20 = hypbclose.PBMRQ[20]
y21 = hypbclose.PBMRQ[21]
y22 = hypbclose.PBMRQ[22]
y23 = hypbclose.PBMRQ[23]
y24 = hypbclose.PBMRQ[24]
y25 = hypbclose.PBMRQ[25]
y26 = hypbclose.PBMRQ[26]
y27 = hypbclose.PBMRQ[27]
y28 = hypbclose.PBMRQ[28]
y29 = hypbclose.PBMRQ[29]
y30 = hypbclose.PBMRQ[30]

fig = px.violin(hypb,x="CODES",y="PBMRQ",color="CODES",box=True)
fig.update_layout(width=1200,height=600,title={'text': "行业PB分位-20年",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                    title_font_size=35,font_size=18,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)

fig.add_annotation(x=0,y=y0,text="×{}".format(y0),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=1,y=y1,text="×{}".format(y1),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=2,y=y2,text="×{}".format(y2),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=3,y=y3,text="×{}".format(y3),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=4,y=y4,text="×{}".format(y4),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=5,y=y5,text="×{}".format(y5),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=6,y=y6,text="×{}".format(y6),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=7,y=y7,text="×{}".format(y7),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=8,y=y8,text="×{}".format(y8),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=9,y=y9,text="×{}".format(y9),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=10,y=y10,text="×{}".format(y10),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=11,y=y11,text="×{}".format(y11),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=12,y=y12,text="×{}".format(y12),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=13,y=y13,text="×{}".format(y13),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=14,y=y14,text="×{}".format(y14),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=15,y=y15,text="×{}".format(y15),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=16,y=y16,text="×{}".format(y16),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=17,y=y17,text="×{}".format(y17),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=18,y=y18,text="×{}".format(y18),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=19,y=y19,text="×{}".format(y19),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=20,y=y20,text="×{}".format(y20),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=21,y=y21,text="×{}".format(y21),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=22,y=y22,text="×{}".format(y22),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=23,y=y23,text="×{}".format(y23),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=24,y=y24,text="×{}".format(y24),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=25,y=y25,text="×{}".format(y25),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=26,y=y26,text="×{}".format(y26),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=27,y=y27,text="×{}".format(y27),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=28,y=y28,text="×{}".format(y28),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=29,y=y29,text="×{}".format(y29),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=30,y=y30,text="×{}".format(y30),ax=10,ay=0,font={'size': 12})
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hypb.png',scale=3)

# 行业市净率PB(MRQ)3年
# 变更特定字符
hypb3['CODES'] = hypb3['CODES'].str.replace('801010.SWI', '农林牧渔')
hypb3['CODES'] = hypb3['CODES'].str.replace('801030.SWI', '基础化工')
hypb3['CODES'] = hypb3['CODES'].str.replace('801040.SWI', '钢铁')
hypb3['CODES'] = hypb3['CODES'].str.replace('801050.SWI', '有色金属')
hypb3['CODES'] = hypb3['CODES'].str.replace('801080.SWI', '电子')
hypb3['CODES'] = hypb3['CODES'].str.replace('801110.SWI', '家用电器')
hypb3['CODES'] = hypb3['CODES'].str.replace('801120.SWI', '食品饮料')
hypb3['CODES'] = hypb3['CODES'].str.replace('801130.SWI', '纺织服饰')
hypb3['CODES'] = hypb3['CODES'].str.replace('801140.SWI', '轻工制造')
hypb3['CODES'] = hypb3['CODES'].str.replace('801150.SWI', '医药生物')
hypb3['CODES'] = hypb3['CODES'].str.replace('801160.SWI', '公用事业')
hypb3['CODES'] = hypb3['CODES'].str.replace('801170.SWI', '交通运输')
hypb3['CODES'] = hypb3['CODES'].str.replace('801180.SWI', '房地产')
hypb3['CODES'] = hypb3['CODES'].str.replace('801200.SWI', '商贸零售')
hypb3['CODES'] = hypb3['CODES'].str.replace('801210.SWI', '社会服务')
hypb3['CODES'] = hypb3['CODES'].str.replace('801230.SWI', '综合')
hypb3['CODES'] = hypb3['CODES'].str.replace('801710.SWI', '建筑材料')
hypb3['CODES'] = hypb3['CODES'].str.replace('801720.SWI', '建筑装饰')
hypb3['CODES'] = hypb3['CODES'].str.replace('801730.SWI', '电力设备')
hypb3['CODES'] = hypb3['CODES'].str.replace('801740.SWI', '国防军工')
hypb3['CODES'] = hypb3['CODES'].str.replace('801750.SWI', '计算机')
hypb3['CODES'] = hypb3['CODES'].str.replace('801760.SWI', '传媒')
hypb3['CODES'] = hypb3['CODES'].str.replace('801770.SWI', '通信')
hypb3['CODES'] = hypb3['CODES'].str.replace('801780.SWI', '银行')
hypb3['CODES'] = hypb3['CODES'].str.replace('801790.SWI', '非银金融')
hypb3['CODES'] = hypb3['CODES'].str.replace('801880.SWI', '汽车')
hypb3['CODES'] = hypb3['CODES'].str.replace('801890.SWI', '机械设备')
hypb3['CODES'] = hypb3['CODES'].str.replace('801950.SWI', '煤炭')
hypb3['CODES'] = hypb3['CODES'].str.replace('801960.SWI', '石油石化')
hypb3['CODES'] = hypb3['CODES'].str.replace('801970.SWI', '环保')
hypb3['CODES'] = hypb3['CODES'].str.replace('801980.SWI', '美容护理')

y0 = hypbclose.PBMRQ[0]
y1 = hypbclose.PBMRQ[1]
y2 = hypbclose.PBMRQ[2]
y3 = hypbclose.PBMRQ[3]
y4 = hypbclose.PBMRQ[4]
y5 = hypbclose.PBMRQ[5]
y6 = hypbclose.PBMRQ[6]
y7 = hypbclose.PBMRQ[7]
y8 = hypbclose.PBMRQ[8]
y9 = hypbclose.PBMRQ[9]
y10 = hypbclose.PBMRQ[10]
y11 = hypbclose.PBMRQ[11]
y12 = hypbclose.PBMRQ[12]
y13 = hypbclose.PBMRQ[13]
y14 = hypbclose.PBMRQ[14]
y15 = hypbclose.PBMRQ[15]
y16 = hypbclose.PBMRQ[16]
y17 = hypbclose.PBMRQ[17]
y18 = hypbclose.PBMRQ[18]
y19 = hypbclose.PBMRQ[19]
y20 = hypbclose.PBMRQ[20]
y21 = hypbclose.PBMRQ[21]
y22 = hypbclose.PBMRQ[22]
y23 = hypbclose.PBMRQ[23]
y24 = hypbclose.PBMRQ[24]
y25 = hypbclose.PBMRQ[25]
y26 = hypbclose.PBMRQ[26]
y27 = hypbclose.PBMRQ[27]
y28 = hypbclose.PBMRQ[28]
y29 = hypbclose.PBMRQ[29]
y30 = hypbclose.PBMRQ[30]

fig = px.violin(hypb3,x="CODES",y="PBMRQ",color="CODES",box=True)
fig.update_layout(width=1200,height=600,title={'text': "行业PB分位-3年",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                    title_font_size=35,font_size=18,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)

fig.add_annotation(x=0,y=y0,text="×{}".format(y0),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=1,y=y1,text="×{}".format(y1),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=2,y=y2,text="×{}".format(y2),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=3,y=y3,text="×{}".format(y3),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=4,y=y4,text="×{}".format(y4),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=5,y=y5,text="×{}".format(y5),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=6,y=y6,text="×{}".format(y6),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=7,y=y7,text="×{}".format(y7),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=8,y=y8,text="×{}".format(y8),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=9,y=y9,text="×{}".format(y9),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=10,y=y10,text="×{}".format(y10),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=11,y=y11,text="×{}".format(y11),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=12,y=y12,text="×{}".format(y12),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=13,y=y13,text="×{}".format(y13),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=14,y=y14,text="×{}".format(y14),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=15,y=y15,text="×{}".format(y15),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=16,y=y16,text="×{}".format(y16),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=17,y=y17,text="×{}".format(y17),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=18,y=y18,text="×{}".format(y18),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=19,y=y19,text="×{}".format(y19),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=20,y=y20,text="×{}".format(y20),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=21,y=y21,text="×{}".format(y21),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=22,y=y22,text="×{}".format(y22),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=23,y=y23,text="×{}".format(y23),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=24,y=y24,text="×{}".format(y24),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=25,y=y25,text="×{}".format(y25),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=26,y=y26,text="×{}".format(y26),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=27,y=y27,text="×{}".format(y27),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=28,y=y28,text="×{}".format(y28),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=29,y=y29,text="×{}".format(y29),ax=10,ay=0,font={'size': 12})
fig.add_annotation(x=30,y=y30,text="×{}".format(y30),ax=10,ay=0,font={'size': 12})
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hypb3.png',scale=3)

# 投资策略
# PB
fig = px.line(agpb,x='DATES',y='PBLYR')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=1200,height=600,title={'text': "A股PB",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\1agpb.png',scale=3)

# 3年PB
fig = px.line(agpb3,x='DATES',y='PBLYR')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 120,),width=1200,height=600,title={'text': "3年A股PB",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\1agpb3.png',scale=3)

# PE
fig = px.line(agpe,x='DATES',y='PETTM')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=1200,height=600,title={'text': "A股PETTM",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\2agpe.png',scale=3)

# 3年PE
fig = px.line(agpe3,x='DATES',y='PETTM')
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
    content.append(Graphs.draw_little_title('3、指数PB'))
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

    content.append(Graphs.draw_little_title('★4、指数PB'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zsPB1.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zsPB2.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zsPB31.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zsPB32.png'))

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

    content.append(Graphs.draw_little_title('★11、行业走势'))

    content.append(Graphs.draw_little_title('★11、行业估值'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hypb.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hypb3.png'))

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