# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 17:01:53 2022

@author: sak10
"""

import xlwings as xw

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu0.xls')
sht = wb.sheets[0]
rng = sht.range('c1').expand('table')
nrows = rng.rows.count
a0a = sht.range(f'c{nrows-3}:c{nrows}').value
a0 = []
for x in a0a:
    x = '%.1f' % (float(x))
    a0.append(x)

app=xw.App(visible=True,add_book=False)
wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu5.xls')
sht = wb.sheets[0]
rng = sht.range('c1').expand('table')
nrows = rng.rows.count
a5a = sht.range(f'c{nrows-3}:c{nrows}').value
a5 = []
for x in a5a:
    x = '%.0f' % (float(x))
    a5.append(x)

app=xw.App(visible=True,add_book=False)
wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu10.xls')
sht = wb.sheets[0]
rng = sht.range('c1').expand('table')
nrows = rng.rows.count
a10a = sht.range(f'c{nrows-3}:c{nrows}').value
a10 = []
for x in a10a:
    x = '%.0f' % (float(x))
    a10.append(x)

app=xw.App(visible=True,add_book=False)
wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu20.xls')
sht = wb.sheets[0]
rng = sht.range('c1').expand('table')
nrows = rng.rows.count
a20a = sht.range(f'c{nrows-3}:c{nrows}').value
a20 = []
for x in a20a:
    x = '%.0f' % (float(x))
    a20.append(x)

app=xw.App(visible=True,add_book=False)
wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu60.xls')
sht = wb.sheets[0]
rng = sht.range('c1').expand('table')
nrows = rng.rows.count
a60a = sht.range(f'c{nrows-3}:c{nrows}').value
a60 = []
for x in a60a:
    x = '%.0f' % (float(x))
    a60.append(x)

app=xw.App(visible=True,add_book=False)
wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu120.xls')
sht = wb.sheets[0]
rng = sht.range('c1').expand('table')
nrows = rng.rows.count
a120a = sht.range(f'c{nrows-3}:c{nrows}').value
a120 = []
for x in a120a:
    x = '%.0f' % (float(x))
    a120.append(x)

app=xw.App(visible=True,add_book=False)
wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu250.xls')
sht = wb.sheets[0]
rng = sht.range('c1').expand('table')
nrows = rng.rows.count
a250a = sht.range(f'c{nrows-3}:c{nrows}').value
a250 = []
for x in a250a:
    x = '%.0f' % (float(x))
    a250.append(x)

n =['????????????','??????300','??????500','??????1000']

from pandas import DataFrame
l1 = n
l2 = a0
l3 = a5
l4 = a10
l5 = a20
l6 = a60
l7 = a120
l8 = a250
df = DataFrame({'??????': l1, '????????????': l2, '5?????????': l3, '10?????????': l4, '20?????????': l5, '60?????????': l6, '120?????????': l7, '250?????????': l8})
df.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu.xls', sheet_name='Sheet1', index=False)

import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table

# ??????????????????,?????????
plt.figure(figsize=(10,8),dpi=300)

# ?????? ???????????? ????????????
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']    # ???????????????????????????plot????????????????????????
mpl.rcParams['axes.unicode_minus'] = False

# figsize ??????figure?????????????????????????????????
# dpi?????????????????????????????????????????????????????????????????????????????????80      1????????????2.5cm,A4?????? 21*30cm?????????
fig = plt.figure(figsize=(5, 1), dpi=500)

# frameon:??????????????????
ax = fig.add_subplot(111, frame_on=False,)

# ??????x??? y???
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis

# ??????excel
datas = pd.read_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu.xls')

print(datas)

# ????????????
table(ax, datas, loc='center')  # where df is your data frame

# ????????????
plt.savefig(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfubiaoge.png')