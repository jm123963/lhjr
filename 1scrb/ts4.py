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
import plotly_express as px
import plotly.graph_objects as go

app = xw.App(visible=False, add_book=True)# 程序可见，只打开不新建工作薄
app.display_alerts = False# 警告关闭
app.screen_updating = False# 屏幕更新关闭
wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\hyfgzhangfu0.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a0a = sht.range(f'e{nrows-5}:e{nrows}').value
wb.close()
a0 = []
for x in a0a:
    x = '%.1f' % (float(x))
    a0.append(x)
    
wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\hyfgzhangfu5.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a5a = sht.range(f'e{nrows-5}:e{nrows}').value
wb.close()
a5 = []
for x in a5a:
    x = '%.0f' % (float(x))
    a5.append(x)
