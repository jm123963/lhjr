# -*- coding: utf-8 -*-

import numpy as np
import xlwings as xw

app = xw.App(visible=False, add_book=True)# 程序可见，只打开不新建工作薄
app.display_alerts = False# 警告关闭
app.screen_updating = False# 屏幕更新关闭
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
df = DataFrame({'名称': l1, '当日涨幅': l2, '5日涨幅': l3, '10日涨幅': l4, '20日涨幅': l5, '60日涨幅': l6, '120日涨幅': l7, '250日涨幅': l8})
df.to_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu.xls', sheet_name='Sheet1', index=False)

import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table

# 调节图像大小,清晰度
plt.figure(figsize=(10,8),dpi=300)

# 解决 画图中文 方块问题
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']    # 指定默认字体：解决plot不能显示中文问题
mpl.rcParams['axes.unicode_minus'] = False

# figsize 指定figure的宽和高，单位为英寸；
# dpi参数指定绘图对象的分辨率，即每英寸多少个像素，缺省值为80      1英寸等于2.5cm,A4纸是 21*30cm的纸张
fig = plt.figure(figsize=(5, 1), dpi=500)

# frameon:是否显示边框
ax = fig.add_subplot(111, frame_on=False,)

# 隐藏x轴 y轴
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis

# 读取excel
datas = pd.read_excel(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu.xls')

print(datas)

# 生成图片
table(ax, datas, loc='center')  # where df is your data frame

# 保存图片
plt.savefig(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfubiaoge.png')