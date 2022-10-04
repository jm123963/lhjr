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
import module as md

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
    print(date)
    # 指数 当日涨跌幅
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","DIFFERRANGE","N=-0,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")    
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu0.xls', encoding='utf-8-sig', index=None)
    print(data)
    # 指数 5日涨跌幅
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu5.xls', encoding='utf-8-sig', index=None)
    print(data)
    # 指数 10日涨跌幅
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu10.xls', encoding='utf-8-sig', index=None)   
    print(data) 
    # 指数 20日涨跌幅
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu20.xls', encoding='utf-8-sig', index=None)
    print(data)
    # 指数 60日涨跌幅
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu60.xls', encoding='utf-8-sig', index=None)
    print(data)
    # 指数 120日涨跌幅
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu120.xls', encoding='utf-8-sig', index=None) 
    print(data)   
    # 指数 250日涨跌幅
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu250.xls', encoding='utf-8-sig', index=None)
    print(data)
    # 指数 （日）主力净流入资金
    date = (date.today() + timedelta(days = -0)).strftime("%Y-%m-%d")
    print(date)
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzijin0.xls', encoding='utf-8-sig', index=None)
    print(data)
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzijin1.xls', encoding='utf-8-sig', index=None)
    print(data)
    data=c.css("000985.CSI,000300.SH,000905.SH,000852.SH","NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzijin2.xls', encoding='utf-8-sig', index=None)
    print(data)

    # 风格当日涨跌幅
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","DIFFERRANGEN","N=0,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu0.xls', encoding='utf-8-sig', index=None)
    print(data)
    # 风格5日涨跌幅
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu5.xls', encoding='utf-8-sig', index=None)
    print(data)
    # 风格10日涨跌幅
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu5.xls', encoding='utf-8-sig', index=None)
    print(data)
    # 风格20日涨跌幅
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu5.xls', encoding='utf-8-sig', index=None)
    print(data)
    # 风格60日涨跌幅
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu5.xls', encoding='utf-8-sig', index=None)
    print(data)
    # 风格120日涨跌幅
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu5.xls', encoding='utf-8-sig', index=None)
    print(data)
    # 风格250日涨跌幅
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu5.xls', encoding='utf-8-sig', index=None)
    print(data)
    # 风格资金
    date = (date.today() + timedelta(days = -0)).strftime("%Y-%m-%d")
    print(date)
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezijin0.xls', encoding='utf-8-sig', index=None)
    print(data)
    date = (date.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezijin1.xls', encoding='utf-8-sig', index=None)
    print(data)
    date = (date.today() + timedelta(days = -2)).strftime("%Y-%m-%d")
    data=c.css("399373.SZ,399375.SZ,399377.SZ,399372.SZ,399374.SZ,399376.SZ","NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezijin2.xls', encoding='utf-8-sig', index=None)
    print(data)

    date = datetime.today().strftime("%Y-%m-%d")
    # 行业涨跌幅
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","DIFFERRANGEN","N=0,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu0.xls', encoding='utf-8-sig', index=None)
    print(data)
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu5.xls', encoding='utf-8-sig', index=None)
    print(data)
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu10.xls', encoding='utf-8-sig', index=None)
    print(data)
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu20.xls', encoding='utf-8-sig', index=None)
    print(data)
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu60.xls', encoding='utf-8-sig', index=None)
    print(data)
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu120.xls', encoding='utf-8-sig', index=None)
    print(data)
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.xls', encoding='utf-8-sig', index=None)
    print(data)
    # 行业资金
    date = (date.today() + timedelta(days = -0)).strftime("%Y-%m-%d")
    # 农林牧渔(申万) 基础化工(申万) 钢铁(申万) 有色金属(申万) 电子(申万) 汽车(申万) 家用电器(申万) 食品饮料(申万) 纺织服装(申万) 轻工制造(申万) 医药生物(申万) 公用事业(申万) 交通运输(申万) 房地产(申万) 商贸零售(申万) 休闲服务(申万) 银行(申万) 非银金融(申万) 综合(申万) 建筑材料(申万) 建筑装饰(申万) 电气设备(申万) 机械设备(申万) 国防军工(申万) 计算机(申万) 传媒(申万) 通信(申万) 纺织服饰(申万) 社会服务(申万) 电力设备(申万) 煤炭(申万) 石油石化(申万) 环保(申万) 美容护理(申万) (区间)主力净流入资金(合计) 使用最新成分
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NETINFLOW","TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezijin0.xls', encoding='utf-8-sig', index=None)
    print(data)
    date = (date.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
    # 农林牧渔(申万) 基础化工(申万) 钢铁(申万) 有色金属(申万) 电子(申万) 汽车(申万) 家用电器(申万) 食品饮料(申万) 纺织服装(申万) 轻工制造(申万) 医药生物(申万) 公用事业(申万) 交通运输(申万) 房地产(申万) 商贸零售(申万) 休闲服务(申万) 银行(申万) 非银金融(申万) 综合(申万) 建筑材料(申万) 建筑装饰(申万) 电气设备(申万) 机械设备(申万) 国防军工(申万) 计算机(申万) 传媒(申万) 通信(申万) 纺织服饰(申万) 社会服务(申万) 电力设备(申万) 煤炭(申万) 石油石化(申万) 环保(申万) 美容护理(申万) (区间)主力净流入资金(合计) 使用最新成分
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NETINFLOW","TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezijin1.xls', encoding='utf-8-sig', index=None)
    print(data)
    date = (date.today() + timedelta(days = -2)).strftime("%Y-%m-%d")
    # 农林牧渔(申万) 基础化工(申万) 钢铁(申万) 有色金属(申万) 电子(申万) 汽车(申万) 家用电器(申万) 食品饮料(申万) 纺织服装(申万) 轻工制造(申万) 医药生物(申万) 公用事业(申万) 交通运输(申万) 房地产(申万) 商贸零售(申万) 休闲服务(申万) 银行(申万) 非银金融(申万) 综合(申万) 建筑材料(申万) 建筑装饰(申万) 电气设备(申万) 机械设备(申万) 国防军工(申万) 计算机(申万) 传媒(申万) 通信(申万) 纺织服饰(申万) 社会服务(申万) 电力设备(申万) 煤炭(申万) 石油石化(申万) 环保(申万) 美容护理(申万) (区间)主力净流入资金(合计) 使用最新成分
    data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","NETINFLOW","TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    data.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezijin2.xls', encoding='utf-8-sig', index=None)
    print(data)

#退出
    data = logoutResult = c.stop()
except Exception as ee:
    print("error >>>",ee)
    traceback.print_exc()
else:
    print("demo end")