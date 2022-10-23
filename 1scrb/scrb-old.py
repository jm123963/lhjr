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

    date = datetime.today().strftime("%Y-%m-%d")
    # 指数 当日涨跌幅
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGE","N=-0,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")    
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu0.xls')
    # 指数 5日涨跌幅
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu5.xls')
    # 指数 10日涨跌幅
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu10.xls')   
    # 指数 20日涨跌幅
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu20.xls')
    # 指数 60日涨跌幅
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu60.xls')
    # 指数 120日涨跌幅
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu120.xls') 
    # 指数 250日涨跌幅
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu250.xls')
    # 指数 （日）主力净流入资金
    date = (datetime.today() + timedelta(days = -0)).strftime("%Y-%m-%d")
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzijin0.xls')
    date = (datetime.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzijin1.xls')
    date = (datetime.today() + timedelta(days = -2)).strftime("%Y-%m-%d")
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzijin2.xls')

    # 风格当日涨跌幅
    date = datetime.today().strftime("%Y-%m-%d")
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=0,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu0.xls')
    # 风格5日涨跌幅
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu5.xls')
    # 风格10日涨跌幅
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu10.xls')
    # 风格20日涨跌幅
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu20.xls')
    # 风格60日涨跌幅
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu60.xls')
    # 风格120日涨跌幅
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu120.xls')
    # 风格250日涨跌幅
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu250.xls')
    # 风格资金
    date = (datetime.today() + timedelta(days = -0)).strftime("%Y-%m-%d")
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezijin0.xls')
    date = (datetime.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezijin1.xls')
    date = (datetime.today() + timedelta(days = -2)).strftime("%Y-%m-%d")
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezijin2.xls')

    date = datetime.today().strftime("%Y-%m-%d")
    # 指数 股票简称 涨跌幅
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-0,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    #data=data.loc[:,["NAME","DIFFERRANGEN"]]
    data =data.sort_values(by="DIFFERRANGEN",ascending=False)
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu0.xls')
    # 指数 股票简称 涨跌幅
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data =data.sort_values(by="DIFFERRANGEN",ascending=False)
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu5.xls')
    # 指数 股票简称 涨跌幅
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data =data.sort_values(by="DIFFERRANGEN",ascending=False)
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu10.xls')
    # 指数 股票简称 涨跌幅
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data =data.sort_values(by="DIFFERRANGEN",ascending=False)
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu20.xls')
    # 指数 股票简称 涨跌幅
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data =data.sort_values(by="DIFFERRANGEN",ascending=False)
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu60.xls')
    # 指数 股票简称 涨跌幅
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data =data.sort_values(by="DIFFERRANGEN",ascending=False)
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu120.xls')
    # 指数 股票简称 涨跌幅
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data =data.sort_values(by="DIFFERRANGEN",ascending=False)
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.xls')

    # 行业资金
    date = (datetime.today() + timedelta(days = -0)).strftime("%Y-%m-%d")
    # 农林牧渔(申万) 基础化工(申万) 钢铁(申万) 有色金属(申万) 电子(申万) 汽车(申万) 家用电器(申万) 食品饮料(申万) 纺织服装(申万) 轻工制造(申万) 医药生物(申万) 公用事业(申万) 交通运输(申万) 房地产(申万) 商贸零售(申万) 休闲服务(申万) 银行(申万) 非银金融(申万) 综合(申万) 建筑材料(申万) 建筑装饰(申万) 电气设备(申万) 机械设备(申万) 国防军工(申万) 计算机(申万) 传媒(申万) 通信(申万) 纺织服饰(申万) 社会服务(申万) 电力设备(申万) 煤炭(申万) 石油石化(申万) 环保(申万) 美容护理(申万) (区间)主力净流入资金(合计) 使用最新成分
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezijin0.xls')   
    data = data.sort_values(by="NETINFLOW",ascending=False)
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezijin.xls')
        
    date = (datetime.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
    # 农林牧渔(申万) 基础化工(申万) 钢铁(申万) 有色金属(申万) 电子(申万) 汽车(申万) 家用电器(申万) 食品饮料(申万) 纺织服装(申万) 轻工制造(申万) 医药生物(申万) 公用事业(申万) 交通运输(申万) 房地产(申万) 商贸零售(申万) 休闲服务(申万) 银行(申万) 非银金融(申万) 综合(申万) 建筑材料(申万) 建筑装饰(申万) 电气设备(申万) 机械设备(申万) 国防军工(申万) 计算机(申万) 传媒(申万) 通信(申万) 纺织服饰(申万) 社会服务(申万) 电力设备(申万) 煤炭(申万) 石油石化(申万) 环保(申万) 美容护理(申万) (区间)主力净流入资金(合计) 使用最新成分
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezijin1.xls')
  
    date = (datetime.today() + timedelta(days = -2)).strftime("%Y-%m-%d")
    # 农林牧渔(申万) 基础化工(申万) 钢铁(申万) 有色金属(申万) 电子(申万) 汽车(申万) 家用电器(申万) 食品饮料(申万) 纺织服装(申万) 轻工制造(申万) 医药生物(申万) 公用事业(申万) 交通运输(申万) 房地产(申万) 商贸零售(申万) 休闲服务(申万) 银行(申万) 非银金融(申万) 综合(申万) 建筑材料(申万) 建筑装饰(申万) 电气设备(申万) 机械设备(申万) 国防军工(申万) 计算机(申万) 传媒(申万) 通信(申万) 纺织服饰(申万) 社会服务(申万) 电力设备(申万) 煤炭(申万) 石油石化(申万) 环保(申万) 美容护理(申万) (区间)主力净流入资金(合计) 使用最新成分
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezijin2.xls')

#退出
    data = logoutResult = c.stop()
except Exception as ee:
    print("error >>>",ee)
    traceback.print_exc()
else:
    print("demo end")

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu0.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,5):
    x1.append(cap1[i].strip("指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,5):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.1f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "当日指数涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu0.png', scale=2)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu5.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,5):
    x1.append(cap1[i].strip("指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,5):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "5日指数涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu5.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu10.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,5):
    x1.append(cap1[i].strip("指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,5):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "10日指数涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu10.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu20.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,5):
    x1.append(cap1[i].strip("指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,5):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "20日指数涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu20.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu60.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,5):
    x1.append(cap1[i].strip("指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,5):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "60日指数涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu60.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu120.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,5):
    x1.append(cap1[i].strip("指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,5):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "120日指数涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu120.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu250.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,5):
    x1.append(cap1[i].strip("指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,5):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "250日指数涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu250.png',scale=3)

app = xw.App(visible=False, add_book=True)# 程序可见，只打开不新建工作薄
app.display_alerts = False# 警告关闭
app.screen_updating = False# 屏幕更新关闭
app=xw.App(visible=True,add_book=False)
wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu0.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a0a = sht.range(f'e{nrows-3}:e{nrows}').value
a0 = []
for x in a0a:
    x = '%.1f' % (float(x))
    a0.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu5.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a5a = sht.range(f'e{nrows-3}:e{nrows}').value
a5 = []
for x in a5a:
    x = '%.0f' % (float(x))
    a5.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu10.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a10a = sht.range(f'e{nrows-3}:e{nrows}').value
a10 = []
for x in a10a:
    x = '%.0f' % (float(x))
    a10.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu20.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a20a = sht.range(f'e{nrows-3}:e{nrows}').value
a20 = []
for x in a20a:
    x = '%.0f' % (float(x))
    a20.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu60.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a60a = sht.range(f'e{nrows-3}:e{nrows}').value
a60 = []
for x in a60a:
    x = '%.0f' % (float(x))
    a60.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu120.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a120a = sht.range(f'e{nrows-3}:e{nrows}').value
a120 = []
for x in a120a:
    x = '%.0f' % (float(x))
    a120.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu250.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a250a = sht.range(f'e{nrows-3}:e{nrows}').value
a250 = []
for x in a250a:
    x = '%.0f' % (float(x))
    a250.append(x)
app.kill()

n =['中证全指','沪深300','中证500','中证1000']

from pandas import DataFrame
l1 = n
l2 = a0
l3 = a5
l4 = a10
l5 = a20
l6 = a60
l7 = a120
l8 = a250
df = DataFrame({'名称': l1, '当日涨幅': l2, '5日涨幅': l3, '10日涨幅': l4, '20日涨幅': l5, '60日涨幅': l6, '120日涨幅': l7, '250日涨幅': l8})

fig = go.Figure(
    data=[go.Table(
        header=dict(values=list(df.columns),  # 表头取值是data列属性
                    fill_color='paleturquoise',font_size=14,
        height=60),  # 填充色和文本位置
                
        cells=dict(values=[l1,l2,l3,l4,l5,l6,l7,l8],  # 单元格的取值就是每个列属性的Series取值
                   fill_color='lavender',font_size=14,
        height=60)
    )]
)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfubiaoge.png', scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\zhishuzijin0.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,5):
    x1.append(cap1[i].strip("指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,5):
    y1.append((float(cap2[i])/100000000))
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "当日指数资金（亿元）",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=20,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zhishuzijin0.png',scale=3)

data0 = pd.read_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzijin0.xls')
data1 = pd.read_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzijin1.xls')
data2 = pd.read_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzijin2.xls')
data3 = pd.merge(data0,data1,left_index=True,right_index=True)
data = pd.merge(data3,data2,left_index=True,right_index=True)
data["NETINFLOhb"] = data["NETINFLOW_x"] + data["NETINFLOW_y"] + data["NETINFLOW"]
data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzijinhebing.xls', encoding='utf-8-sig', index=None)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\zhishuzijinhebing.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,5):
    x1.append(cap1[i].strip("指数"))
y1=[]   
cap2 = table.col_values(15)
for i in range(1,5):
    y1.append((float(cap2[i])/100000000))
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "3日指数资金（亿元）",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=20,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zhishuzijinhebing.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu0.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,7):
    x1.append(cap1[i].strip("巨潮指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,7):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.1f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "当日风格涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=30,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu0.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu5.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,7):
    x1.append(cap1[i].strip("巨潮指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,7):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "5日风格涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=30,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu5.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu10.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,7):
    x1.append(cap1[i].strip("巨潮指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,7):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "10日风格涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=30,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu10.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu20.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,7):
    x1.append(cap1[i].strip("巨潮指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,7):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "20日风格涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=30,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu20.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu60.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,7):
    x1.append(cap1[i].strip("巨潮指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,7):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "60日风格涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=30,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu60.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu120.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,7):
    x1.append(cap1[i].strip("巨潮指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,7):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "120日风格涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=30,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu120.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu250.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,7):
    x1.append(cap1[i].strip("巨潮指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,7):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "250日风格涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=30,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu250.png',scale=3)

app = xw.App(visible=False, add_book=True)# 程序可见，只打开不新建工作薄
app.display_alerts = False# 警告关闭
app.screen_updating = False# 屏幕更新关闭
wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu0.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a0a = sht.range(f'e{nrows-5}:e{nrows}').value
wb.close()
a0 = []
for x in a0a:
    x = '%.1f' % (float(x))
    a0.append(x)
    
wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu5.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a5a = sht.range(f'e{nrows-5}:e{nrows}').value
wb.close()
a5 = []
for x in a5a:
    x = '%.0f' % (float(x))
    a5.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu10.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a10a = sht.range(f'e{nrows-5}:e{nrows}').value
wb.close()
a10 = []
for x in a10a:
    x = '%.0f' % (float(x))
    a10.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu20.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a20a = sht.range(f'e{nrows-5}:e{nrows}').value
wb.close()
a20 = []
for x in a20a:
    x = '%.0f' % (float(x))
    a20.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu60.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a60a = sht.range(f'e{nrows-5}:e{nrows}').value
wb.close()
a60 = []
for x in a60a:
    x = '%.0f' % (float(x))
    a60.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu120.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a120a = sht.range(f'e{nrows-5}:e{nrows}').value
wb.close()
a120 = []
for x in a120a:
    x = '%.0f' % (float(x))
    a120.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu250.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a250a = sht.range(f'e{nrows-5}:e{nrows}').value
wb.close()
a250 = []
for x in a250a:
    x = '%.0f' % (float(x))
    a250.append(x)
app.kill()

n =['大盘价值','中盘价值','小盘价值','大盘成长','中盘成长','小盘成长']

from pandas import DataFrame
l1 = n
l2 = a0
l3 = a5
l4 = a10
l5 = a20
l6 = a60
l7 = a120
l8 = a250
df = DataFrame({'名称': l1, '当日涨幅': l2, '5日涨幅': l3, '10日涨幅': l4, '20日涨幅': l5, '60日涨幅': l6, '120日涨幅': l7, '250日涨幅': l8})

fig = go.Figure(
    data=[go.Table(
        header=dict(values=list(df.columns),  # 表头取值是data列属性
                    fill_color='paleturquoise',font_size=14,
        height=35),  # 填充色和文本位置
                
        cells=dict(values=[l1,l2,l3,l4,l5,l6,l7,l8],  # 单元格的取值就是每个列属性的Series取值
                   fill_color='lavender',font_size=14,
        height=35)
    )]
)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fenggezhangfubiaoge.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\fenggezijin0.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,7):
    x1.append(cap1[i].strip("巨潮指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,7):
    y1.append((float(cap2[i])/100000000))
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "当日风格资金（亿元）",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=20,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fenggezijin0.png',scale=3)

data0 = pd.read_excel(r'C:\xyzy\1lhjr\1scrb\fenggezijin0.xls')
data1 = pd.read_excel(r'C:\xyzy\1lhjr\1scrb\fenggezijin1.xls')
data2 = pd.read_excel(r'C:\xyzy\1lhjr\1scrb\fenggezijin2.xls')
data3 = pd.merge(data0,data1,left_index=True,right_index=True)
data = pd.merge(data3,data2,left_index=True,right_index=True)
data["NETINFLOhb"] = data["NETINFLOW_x"] + data["NETINFLOW_y"] + data["NETINFLOW"]
data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezijinhebing.xls', encoding='utf-8-sig', index=None)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\fenggezijinhebing.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,7):
    x1.append(cap1[i].strip("巨潮指数"))
y1=[]   
cap2 = table.col_values(15)
for i in range(1,7):
    y1.append((float(cap2[i])/100000000))
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "3日风格资金（亿元）",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=20,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\fenggezijinhebing.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu0.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,32):
    x1.append(cap1[i].strip("申万一级指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,32):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.1f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "当日行业涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=20,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu0.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu5.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,32):
    x1.append(cap1[i].strip("申万一级指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,32):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "5日行业涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=20,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu5.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu10.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,32):
    x1.append(cap1[i].strip("申万一级指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,32):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "10日行业涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=20,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu10.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu20.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,32):
    x1.append(cap1[i].strip("申万一级指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,32):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "20日行业涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=20,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu20.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu60.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,32):
    x1.append(cap1[i].strip("申万一级指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,32):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "60日行业涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=20,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu60.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu120.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,32):
    x1.append(cap1[i].strip("申万一级指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,32):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "120日行业涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=20,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu120.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,32):
    x1.append(cap1[i].strip("申万一级指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,32):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "250日行业涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=20,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.png',scale=3)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\hangyezijin.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,32):
    x1.append(cap1[i].strip("申万一级指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,32):
    y1.append((float(cap2[i])/100000000))
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "当日行业资金（亿元）",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=20,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hangyezijin.png',scale=3)

data0 = pd.read_excel(r'C:\xyzy\1lhjr\1scrb\hangyezijin0.xls')
data1 = pd.read_excel(r'C:\xyzy\1lhjr\1scrb\hangyezijin1.xls')
data2 = pd.read_excel(r'C:\xyzy\1lhjr\1scrb\hangyezijin2.xls')
data3 = pd.merge(data0,data1,left_index=True,right_index=True)
data = pd.merge(data3,data2,left_index=True,right_index=True)
data["NETINFLOhb"] = data["NETINFLOW_x"] + data["NETINFLOW_y"] + data["NETINFLOW"]
data = data.sort_values(by="NETINFLOhb",ascending=False)
data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezijinhebing.xls', encoding='utf-8-sig', index=None)

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\hangyezijinhebing.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,32):
    x1.append(cap1[i].strip("申万一级指数"))
y1=[]   
cap2 = table.col_values(15)
for i in range(1,32):
    y1.append((float(cap2[i])/100000000))
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "3日行业资金（亿元）",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=20,title_font_color='red',xaxis_tickangle=-45,showlegend=False,xaxis_title=None,yaxis_title=None)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\hangyezijinhebing.png',scale=3)

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
        ct.fontSize = 15            # 字体大小
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
        ct.fontSize = 15  # 字体大小
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
        ct.fontSize = 15  # 字体大小
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
        ct.fontSize = 15  # 字体大小
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
    content.append(Graphs.draw_little_title('1、指数涨幅'))
    content.append(Graphs.draw_little_title('2、指数资金'))
    content.append(Graphs.draw_little_title('3、风格涨幅'))
    content.append(Graphs.draw_little_title('4、风格资金'))
    content.append(Graphs.draw_little_title('5、行业涨幅'))
    content.append(Graphs.draw_little_title1('6、行业资金'))
    
    content.append(Graphs.draw_little_title('★1、指数涨幅'))
    content.append(Graphs.draw_img2(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfubiaoge.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu5.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu10.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu20.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu60.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu120.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu250.png'))
    
    content.append(Graphs.draw_little_title('★2、指数资金'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zhishuzijin0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zhishuzijinhebing.png'))

    content.append(Graphs.draw_little_title('★3、风格涨幅'))
    content.append(Graphs.draw_img2(r'C:\xyzy\1lhjr\1scrb\fenggezhangfubiaoge.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu5.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu10.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu20.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu60.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu120.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu250.png'))

    content.append(Graphs.draw_little_title('★4、风格资金'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fenggezijin0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fenggezijinhebing.png'))

    content.append(Graphs.draw_little_title('★5、行业涨幅'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu5.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu10.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu20.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu60.png'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu120.png'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.png'))

    content.append(Graphs.draw_little_title('★6、行业资金'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hangyezijin.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hangyezijinhebing.png'))

    content.append(Graphs.draw_title1('数据来源：Choice  报告工具：Python'))

    # 生成pdf文件
    doc = SimpleDocTemplate(r'C:\xyzy\1lhjr\1scrb\ribao.pdf', pagesize=letter)
    doc.build(content)