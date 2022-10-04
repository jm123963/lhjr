# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 22:34:54 2022

@author: sak10
"""
import numpy as np
import xlwings as xw
app = xw.App(visible=False, add_book=True)# 程序可见，只打开不新建工作薄
app.display_alerts = False# 警告关闭
app.screen_updating = False# 屏幕更新关闭
wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\fenggezijin0.xls')
sht = wb.sheets[0]
rng = sht.range('c1').expand('table')
nrows = rng.rows.count
a0 = sht.range(f'c{nrows-5}:c{nrows}').value
wb.close()

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\fenggezijin1.xls')
sht = wb.sheets[0]
rng = sht.range('c1').expand('table')
nrows = rng.rows.count
a1 = sht.range(f'c{nrows-5}:c{nrows}').value
wb.close()

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\fenggezijin2.xls')
sht = wb.sheets[0]
rng = sht.range('c1').expand('table')
nrows = rng.rows.count
a2 = sht.range(f'c{nrows-5}:c{nrows}').value
wb.close()
app.kill()

n = ['大盘价值','中盘价值','小盘价值','大盘成长','中盘成长','小盘成长']

from pandas import DataFrame
l1 = n
l2 = a0
l3 = a1
l4 = a2
df = DataFrame({'名称': l1, '1日资金': l2, '2日资金': l3, '3日资金': l4})
df.to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezijin.xls', sheet_name='Sheet1', index=False)

import pandas as pd
data_= pd.read_excel(r'C:\xyzy\1lhjr\1scrb\fenggezijin.xls')
data_['3日资金和'] = round((data_['1日资金'] + data_['2日资金'] + data_['3日资金'])).astype('str')
data_['3日资金和'].to_excel(r'C:\xyzy\1lhjr\1scrb\fenggezijinhebing2.xls', index=False)


# -*- coding: utf-8 -*-

import matplotlib as mpl
import matplotlib.pyplot as plt
import xlrd

# 调节图像大小,清晰度
plt.figure(figsize=(10,8),dpi=300)

#指定字体为SimHei，用于显示中文，如果Ariel,中文会乱码
mpl.rcParams["font.sans-serif"]=["SimHei"]
#用来正常显示负号
mpl.rcParams["axes.unicode_minus"]=False

x1 = ['大盘价值','中盘价值','小盘价值','大盘成长','中盘成长','小盘成长']
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\fenggezijinhebing2.xls')
table = data.sheets()[0]
 
y1=[]   
cap2 = table.col_values(0)
for i in range(1,7):
    y1.append(float('%.0f' % (float(cap2[i])/100000000)))

plt.bar(x1,y1,align="center",hatch=" ",ec='gray',color=np.where(np.array(y1)>0,'r','c'))
plt.xticks(rotation=0,fontsize=20)
plt.yticks(fontsize=20)

#绘制纵向柱状图,hatch定义柱图的斜纹填充，省略该参数表示默认不填充。
#bar柱图函数还有以下参数：
#颜色：color,可以取具体颜色如red(简写为r),也可以用rgb让每条柱子采用不同颜色。
#描边：edgecolor（ec）：边缘颜色；linestyle（ls）：边缘样式；linewidth（lw）：边缘粗细
#填充：hatch，取值：/,|,-,+,x,o,O,.,*
#位置标志：tick_label

for a,b in zip(x1,y1):

    plt.text(a,b,'%.0f' % b, ha='center', va= 'bottom',fontsize=20)

plt.title('3日风格资金（亿元）',fontsize=20)
plt.xlabel(u"")
plt.ylabel(u"")
plt.legend()
plt.savefig(r'C:\xyzy\1lhjr\1scrb\fenggezijin2.png',c = 'k')