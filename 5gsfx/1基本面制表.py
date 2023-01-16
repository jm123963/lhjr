# -*- coding:utf-8 -*-
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


#调用登录函数（激活后使用，不需要用户名密码）
loginResult = c.start("ForceLogin=1", '')

# 当前时间
today = datetime.today().strftime("%Y-%m-%d")
dates='2021-12-31','2020-12-31','2019-12-31','2018-12-31'

# 板块成分
data = c.sector("009006084", "2022-12-15", "RowIndex=1,Ispandas=1")
codes=list(data.index)

# 净资产收益率ROETTM(扣除/加权) 
df=c.css(codes,"ROETTMDEDUCTED","TradeDate=2022-12-19,TtmType=2,Ispandas=1")
# 添加 近4年净资产收益率ROE(扣除/加权) 
for da in dates:
    data=c.css(codes,"ROEEXAVG",f"ReportDate={da},Ispandas=1")
    df=pd.concat([df,data], axis=1)
df=df.drop(labels=['DATES'], axis=1)
df['年均ROE']=df.mean(1)
# 添加 销售毛利率(TTM) 销售净利率(TTM) 营业总收入N年增长率 归属母公司股东的净利润—扣除非经常性损益N年增长率 营业总收入同比增长率 归属母公司股东的净利润同比增长率(扣除非经常性损益) 市净率(PB,扣除商誉) 市盈率TTM(扣除非经常性损益) 首发上市日 
data=c.css(codes,"GPMARGINTTM,NPMARGINTTM,NYGROWTHRATEGR,NYGROWTHRATENIDEDUCTED,YOYGR,YOYPNIDEDUCTED,PBDEDUCTBS,PETTMDEDUCTED","TradeDate=2022-12-19,TtmType=2,N=5,ReportDate=2021-12-31,Ispandas=1")
df=pd.concat([df,data], axis=1)
df=df.drop(labels=['DATES'], axis=1)
# 缺失值赋0
df=df.fillna(0)
# 设置小数位
#df=df.applymap(lambda x: '%.0f'%x)
# 添加 总市值(证监会算法) 
data=c.css(codes,"MVBYCSRC","TradeDate=2022-12-19,Ispandas=1")
data=data.drop(labels=['DATES'], axis=1)
data=data/100000000
df=pd.concat([df,data], axis=1)
# 设置小数位
df=df.applymap(lambda x: '%.0f'%x)
# 添加 首发上市日 股票简称 
data=c.css(codes,"LISTDATE,NAME","Ispandas=1")
df=pd.concat([df,data], axis=1)
df=df.drop(labels=['DATES'], axis=1)
# 变更列名
df.columns=['ROETTM','ROE2021年','ROE2020年','ROE2019年','ROE2018年','年均ROE','毛利率','净利率','收入5年增长率','净利润5年增长率','收入同比','净利润同比',
            'PB','PETTM','总市值(亿）','上市日','股票简称']
# 按照列col1降序排列数据
df.sort_values(['ROETTM','ROE2021年'],ascending=[False,False],inplace=True)
df.to_excel(r'C:\xyzy\1lhjr\5gsfx\基本面.xlsx', index=False)