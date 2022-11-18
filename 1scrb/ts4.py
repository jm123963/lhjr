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
# 当前交易日
offday=[-1,-5,-10,-20,-60,-120,-250]
fgcode="000985.CSI,399314.SZ,399316.SZ,399370.SZ,399371.SZ"

#df=c.css(fgcode,"DIFFERRANGERECENT1M","")
df=c.css(fgcode,"DIFFERRANGEN","N=5,TradeDate=2022-11-11,AdjustFlag=1,Ispandas=1")
print(df)
fig = px.bar(df,x=df.index,y='DIFFERRANGEN')
fig.show()