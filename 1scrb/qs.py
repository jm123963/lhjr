code='SZSE.002415' 
# (22年数据截止Q3)

# coding=utf-8
#from __future__ import print_function, absolute_import
from gm.api import *
from datetime import timedelta, datetime
import time as _time
import numpy as np
import pandas as pd
import plotly_express as px

import warnings
# 关闭警告信息
warnings.filterwarnings('ignore')

# notebook宽屏显示
from IPython.display import display, HTML
display(HTML('<style>.container{width:100% !important;}</style>'))

set_token('010c1f80a24030f7bd79d2fdbff8eb969dc88a01')
# 获取当前时间
now = datetime.today().strftime("%Y-%m-%d")
last_date = get_previous_trading_date(exchange='SHSE', date=now)
end_dates='2022-09-30','2021-12-31','2020-12-31','2019-12-31','2018-12-31','2017-12-31','2016-12-31','2015-12-31','2014-12-31',\
    '2013-12-31','2012-12-31','2011-12-31','2010-12-31','2009-12-31','2008-12-31','2007-12-31','2006-12-31',\
    '2005-12-31','2004-12-31','2003-12-31','2002-12-31','2001-12-31','2000-12-31'

def bar(table,field,unit,text,image):
    df=pd.DataFrame()
    for end_date in end_dates:
        data=get_fundamentals_n(table=table,symbols=code,end_date=end_date,count=1,
            fields=field,df=True)
        df=pd.concat([df,data],ignore_index=True)
    df['end_date']=df['end_date'].dt.year
    df.iloc[:,3]=df.iloc[:,3]/unit
    print(df)

bar('prim_finance_indicator','ROEWEIGHTED',1,'净资产收益率_加权%','ROE')