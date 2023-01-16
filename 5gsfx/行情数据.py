from EmQuantAPI import *
from datetime import timedelta, datetime
import time as _time
import traceback
from datetime import *
import numpy as np
import pandas as pd
from pandas import DataFrame
from pylab import mpl
from pandas.plotting import table
#调用登录函数（激活后使用，不需要用户名密码）
loginResult = c.start("ForceLogin=1", '')

codes = '605336.SH','002757.SZ','002191.SZ','300418.SZ','002815.SZ','688230.SH','002236.SZ','000776.SZ'
# 当前时间
date = datetime.today().strftime("%Y-%m-%d")

for code in codes:
    # 沪深股票 市净率(PB,扣除商誉) 市盈率TTM（扣除非经常性损益） 开盘价 收盘价 最高价 最低价 涨跌幅 成交金额 
    df=c.csd(code,"PBDEDUCTBS,PETTMDEDUCTED,PSTTM,CLOSE,AMOUNT","1990-12-24",""+date+"","period=3,adjustflag=3, curtype=1,order=1,market=CNSESH,filldata=1,Rowindex=none,Ispandas=1")
    df=df.dropna()
    df=df.drop('CODES',axis=1)
    df['DATES']=df['DATES'].str[:7]
    print(df)
