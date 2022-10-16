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
app=xw.App(visible=True,add_book=False)
wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu0.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a0a = sht.range(f'e{nrows-3}:e{nrows}').value
a0 = []
for x in a0a:
    x = '%.1f' % (float(x))
    a0.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu5.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a5a = sht.range(f'e{nrows-3}:e{nrows}').value
a5 = []
for x in a5a:
    x = '%.0f' % (float(x))
    a5.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu10.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a10a = sht.range(f'e{nrows-3}:e{nrows}').value
a10 = []
for x in a10a:
    x = '%.0f' % (float(x))
    a10.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu20.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a20a = sht.range(f'e{nrows-3}:e{nrows}').value
a20 = []
for x in a20a:
    x = '%.0f' % (float(x))
    a20.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu60.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a60a = sht.range(f'e{nrows-3}:e{nrows}').value
a60 = []
for x in a60a:
    x = '%.0f' % (float(x))
    a60.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu120.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a120a = sht.range(f'e{nrows-3}:e{nrows}').value
a120 = []
for x in a120a:
    x = '%.0f' % (float(x))
    a120.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu250.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a250a = sht.range(f'e{nrows-3}:e{nrows}').value
a250 = []
for x in a250a:
    x = '%.0f' % (float(x))
    a250.append(x)
app.kill()

n =['中证全指','沪深300','中证500','中证1000']

from pandas import DataFrame
l1 = n
l2 = a0
l3 = a5
l4 = a10
l5 = a20
l6 = a60
l7 = a120
l8 = a250
df = pd.DataFrame({'名称': l1, '当日涨幅': l2, '5日涨幅': l3, '10日涨幅': l4, '20日涨幅': l5, '60日涨幅': l6, '120日涨幅': l7, '250日涨幅': l8})
#df.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu.xls', sheet_name='Sheet1', index=False)
print(df)

fig = go.Figure(
    data=[go.Table(
        header=dict(values=list(df.columns),  # 表头取值是data列属性
                    fill_color='paleturquoise',font_size=14,
        height=60),  # 填充色和文本位置
                
        cells=dict(values=[l1,l2,l3,l4,l5,l6,l7,l8],  # 单元格的取值就是每个列属性的Series取值
                   fill_color='lavender',font_size=14,
        height=60)
    )]
)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfubiaoge.png')