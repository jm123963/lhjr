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
import exchange_calendars as trade_date
#调用登录函数（激活后使用，不需要用户名密码）
loginResult = c.start("ForceLogin=1", '')

# 当前时间
date = datetime.today().strftime("%Y-%m-%d")
offday=[-1,-5,-10,-20,-60,-120,-250]
fgcode="399373.SZ,399372.SZ,399377.SZ,399376.SZ"
hycode="801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,\
        801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,\
        801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI"

df=c.csd(fgcode,"CLOSE","2005-01-01",""+date+"","period=3,adjustflag=3,curtype=1,order=1,market=CNSESH,Ispandas=1")
print(df)

#zs(fgcode,'2005-01-01',3,'风格20年走势','fgzs20')
#fgzs=c.csd(fgcode,"CLOSE","2003-01-01",""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
