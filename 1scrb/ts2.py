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

import xlwings as xw

app = xw.App(visible=False, add_book=True)# 程序可见，只打开不新建工作薄
app.display_alerts = False# 警告关闭
app.screen_updating = False# 屏幕更新关闭
wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu0.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a0a = sht.range(f'e{nrows-5}:e{nrows}').value
wb.close()
a0 = []
for x in a0a:
    x = '%.1f' % (float(x))
    a0.append(x)
    
wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu5.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a5a = sht.range(f'e{nrows-5}:e{nrows}').value
wb.close()
a5 = []
for x in a5a:
    x = '%.0f' % (float(x))
    a5.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu10.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a10a = sht.range(f'e{nrows-5}:e{nrows}').value
wb.close()
a10 = []
for x in a10a:
    x = '%.0f' % (float(x))
    a10.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu20.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a20a = sht.range(f'e{nrows-5}:e{nrows}').value
wb.close()
a20 = []
for x in a20a:
    x = '%.0f' % (float(x))
    a20.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu60.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a60a = sht.range(f'e{nrows-5}:e{nrows}').value
wb.close()
a60 = []
for x in a60a:
    x = '%.0f' % (float(x))
    a60.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu120.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a120a = sht.range(f'e{nrows-5}:e{nrows}').value
wb.close()
a120 = []
for x in a120a:
    x = '%.0f' % (float(x))
    a120.append(x)

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu250.xls')
sht = wb.sheets[0]
rng = sht.range('e1').expand('table')
nrows = rng.rows.count
a250a = sht.range(f'e{nrows-5}:e{nrows}').value
wb.close()
a250 = []
for x in a250a:
    x = '%.0f' % (float(x))
    a250.append(x)
app.kill()

n =['大盘价值','中盘价值','小盘价值','大盘成长','中盘成长','小盘成长']

from pandas import DataFrame
l1 = n
l2 = a0
l3 = a5
l4 = a10
l5 = a20
l6 = a60
l7 = a120
l8 = a250
df = DataFrame({'名称': l1, '当日涨幅': l2, '5日涨幅': l3, '10日涨幅': l4, '20日涨幅': l5, '60日涨幅': l6, '120日涨幅': l7, '250日涨幅': l8})
df.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu.xls', sheet_name='Sheet1', index=False)

import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table

# 调节图像大小,清晰度
plt.figure(figsize=(20,8),dpi=500)

# 解决 画图中文 方块问题
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']    # 指定默认字体：解决plot不能显示中文问题
mpl.rcParams['axes.unicode_minus'] = False

# figsize 指定figure的宽和高，单位为英寸；
# dpi参数指定绘图对象的分辨率，即每英寸多少个像素，缺省值为80      1英寸等于2.5cm,A4纸是 21*30cm的纸张
fig = plt.figure(figsize=(5, 1.5), dpi=500)

# frameon:是否显示边框
ax = fig.add_subplot(111, frame_on=False,)

# 隐藏x轴 y轴
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis

# 读取excel
datas = pd.read_excel(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu.xls')
datas = datas.iloc[:,:]

# 生成图片
table(ax, datas, loc='center')  # where df is your data frame

# 保存图片
plt.savefig(r'C:\xyzy\1lhjr\1scrb\fenggezhangfubiaoge.png')