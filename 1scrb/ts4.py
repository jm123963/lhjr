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

fgcode="399373.SZ,399377.SZ,399372.SZ,399376.SZ"

# 风格PB
df=c.css('801030.SWI','SHORTNAME','2013-01-01',"TradeDate="+date+",DelType=1,Rowindex=none,Ispandas=1")

print(df)