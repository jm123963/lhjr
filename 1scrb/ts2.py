#coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *
from datetime import timedelta, datetime
import time as _time
import numpy as np
import pandas as pd
import plotly_express as px
set_token('010c1f80a24030f7bd79d2fdbff8eb969dc88a01')
# 获取当前时间
today = datetime.today().strftime("%Y-%m-%d")

# 通过get_instruments获取所有的上市股票代码，剔除停牌股和st股
#codes = get_instruments(exchanges='SHSE, SZSE', sec_types=SEC_TYPE_STOCK, skip_suspended=True,
                                    #skip_st=True, fields='symbol, delisted_date', df=True)
#codes=codes.symbol

codes='SHSE.600000', 'SZSE.000001', 'SZSE.000002'
dates='2022-09-30','2021-12-31','2020-12-31','2019-12-31','2018-12-31'

df1=pd.DataFrame()
df2=pd.DataFrame()
df3=pd.DataFrame()
df4=pd.DataFrame()
df5=pd.DataFrame()
#主要财务指标
for code in codes:
    for date in dates:
        data=get_fundamentals(table='prim_finance_indicator', symbols=code, start_date=date, end_date=date,
                             fields='ROEWEIGHTEDCUT', df=True)
        df1=pd.concat([df1,data], axis=1)

    df1=df1.drop(labels=['pub_date','end_date'], axis=1)
    #df1=df1.mean(1)
    print(df1)