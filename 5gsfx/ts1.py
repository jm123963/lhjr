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

df = history(symbol='SHSE.605336', frequency='1d', start_time='1990-01-01',  end_time='2023-01-12', fields='close,eob', adjust=ADJUST_PREV, df= True)
print(df)
