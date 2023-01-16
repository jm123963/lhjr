# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *
from datetime import timedelta, datetime
import time as _time
import numpy as np
import pandas as pd
import plotly_express as px
set_token('010c1f80a24030f7bd79d2fdbff8eb969dc88a01')

codes='SHSE.605336','SZSE.002757','SZSE.002191','SZSE.300418','SZSE.002815','SHSE.688230','SZSE.002236','SZSE.000776'
# (22年数据截止Q3)
# 获取当前时间
now = datetime.today().strftime("%Y-%m-%d")
last_date = get_previous_trading_date(exchange='SHSE', date=now)
end_dates='2022-09-30','2021-12-31','2020-12-31','2019-12-31','2018-12-31','2017-12-31','2016-12-31','2015-12-31','2014-12-31',\
    '2013-12-31','2012-12-31','2011-12-31','2010-12-31','2009-12-31','2008-12-31','2007-12-31','2006-12-31',\
    '2005-12-31','2004-12-31','2003-12-31','2002-12-31','2001-12-31','2000-12-31'

for code in codes:
    # PB,PE,CLOSE
    df=get_fundamentals(table='trading_derivative_indicator', symbols='SZSE.000776', start_date='1990-01-01', end_date='2023-01-12',
                     fields='PB,PETTM,TCLOSE', limit=40000, df=True)
    df['date'] = df['end_date'].dt.date
    df=df.iloc[:,2:]
    # 净资产收益率_加权%
    df1=pd.DataFrame()
    for end_date in end_dates:
        data=get_fundamentals_n(table='prim_finance_indicator',symbols=code,end_date=end_date,count=1,
                                fields='ROEWEIGHTED',df=True)
        df1=pd.concat([df1,data],ignore_index=True)

    # 营业总收入增长率% 归母净利润增长率% 资产负债率% 三项费用比重% 营业费用率% 管理费用率% 财务费用率% 销售毛利率% 营业利润率% 销售净利率%
    # 投入资本回报率%  现金比率% 速动比率% 流动比率% 应收账款周转率% 负债结构比率% 固定资产比重% 经营性现金净流量/营业总收入% 
    # 经营活动净现金/归属母公司的净利润% 
    df2=pd.DataFrame()
    for end_date in end_dates:
        data=get_fundamentals_n(table='deriv_finance_indicator',symbols=code,end_date=end_date,count=1,
                                fields='ROIC,TAGRT,SNPMARGINCONMS,CURRENTRT,NPGRT,TATURNRT,ACCRECGTURNRT,ACCPAYRT,ASSLIABRT,SGPMARGIN,QUICKRT,OPNCFTOOPTI,\
                                OPNCFTONP',df=True)
        df2=pd.concat([df2,data],ignore_index=True)

    df2['年份']=df2['end_date'].dt.year
    df=pd.concat([df,df1],axis=1)
    df=pd.concat([df,df2],axis=1)
    df=df.drop(['symbol','pub_date','end_date'], axis=1)
    df.columns=['PB','PETTM','TCLOSE','date','净资产收益率_加权%','投入资本回报率%','销售毛利率%','销售净利率%','营业总收入增长率%','归母净利润增长率%','总资产周转率',\
                '应收账款周转率','应付账款周转率','资产负债率%','流动比率%','速动比率%','经营性现金净流量/营业总收入%',\
                '经营活动净现金/归属母公司的净利润% ','年份']
    #df=df.applymap(lambda x: '%.0f'%x)
    df.to_excel(Fr'C:\xyzy\1lhjr\5gsfx\tzsj\{code[5:]}.xlsx')