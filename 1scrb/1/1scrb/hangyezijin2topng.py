# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 22:34:54 2022

@author: sak10
"""

import xlwings as xw

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\hangyezijin0.xls')
sht = wb.sheets[0]
rng = sht.range('b1').expand('table')
nrows = rng.rows.count
a0 = sht.range(f'b{nrows-30}:b{nrows}').value
wb.close()

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\hangyezijin1.xls')
sht = wb.sheets[0]
rng = sht.range('b1').expand('table')
nrows = rng.rows.count
a1 = sht.range(f'b{nrows-30}:b{nrows}').value
wb.close()

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\hangyezijin2.xls')
sht = wb.sheets[0]
rng = sht.range('b1').expand('table')
nrows = rng.rows.count
a2 = sht.range(f'b{nrows-30}:b{nrows}').value
wb.close()

n = ['农林牧渔','基础化工','钢铁','有色金属','电子','家用电器','食品饮料','纺织服饰','轻工制造','医药生物','公用事业','交通运输','房地产','商业贸易','社会服务','综合','建筑材料','建筑装饰','电力设备','国防军工','计算机','传媒','通信','银行','非银金融','汽车','机械设备','煤炭','石油石化','环保','美容护理']

from pandas import DataFrame
l1 = n
l2 = a0
l3 = a1
l4 = a2
df = DataFrame({'名称': l1, '1日资金': l2, '2日资金': l3, '3日资金': l4})
df.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezijin.xls', sheet_name='Sheet1', index=False)

import pandas as pd
data_= pd.read_excel(r'C:\xyzy\1lhjr\1scrb\hangyezijin.xls')
data_['3日资金和'] = round((data_['1日资金'] + data_['2日资金'] + data_['3日资金'])).astype('str')
data_['3日资金和'].to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezijinhebing2.xls', index=False)

import pandas as pd
stexcel=pd.read_excel(r'C:\xyzy\1lhjr\1scrb\hangyezijinhebing2.xls')
#ascending 默认等于True，按从小到大排列，改为False 按从大到小排
stexcel.sort_values(by='3日资金和',inplace=True,ascending=False)
stexcel.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezijinhebing2.xls', sheet_name='Sheet1', index=False)


import matplotlib as mpl
import matplotlib.pyplot as plt
import xlrd

# 调节图像大小,清晰度
plt.figure(figsize=(12,8),dpi=300)

#指定字体为SimHei，用于显示中文，如果Ariel,中文会乱码
mpl.rcParams["font.sans-serif"]=["SimHei"]
#用来正常显示负号
mpl.rcParams["axes.unicode_minus"]=False

x1 = ['农林牧渔','基础化工','钢铁','有色金属','电子','家用电器','食品饮料','纺织服饰','轻工制造','医药生物','公用事业','交通运输','房地产','商业贸易','社会服务','综合','建筑材料','建筑装饰','电力设备','国防军工','计算机','传媒','通信','银行','非银金融','汽车','机械设备','煤炭','石油石化','环保','美容护理']
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\hangyezijinhebing2.xls')
table = data.sheets()[0]
 
y1=[]   
cap2 = table.col_values(0)
for i in range(1,32):
    y1.append(float('%.0f' % (float(cap2[i])/100000000)))

plt.bar(x1,y1,align="center",hatch=" ",ec='gray',color='c')
plt.xticks(rotation=90,fontsize=15)
plt.yticks(fontsize=20)

#绘制纵向柱状图,hatch定义柱图的斜纹填充，省略该参数表示默认不填充。
#bar柱图函数还有以下参数：
#颜色：color,可以取具体颜色如red(简写为r),也可以用rgb让每条柱子采用不同颜色。
#描边：edgecolor（ec）：边缘颜色；linestyle（ls）：边缘样式；linewidth（lw）：边缘粗细
#填充：hatch，取值：/,|,-,+,x,o,O,.,*
#位置标志：tick_label

for a,b in zip(x1,y1):

    plt.text(a,b,'%.0f' % b, ha='center', va= 'bottom',fontsize=10)

plt.title('3日行业资金（亿元）',fontsize=20)
plt.xlabel(u"")
plt.ylabel(u"")
plt.legend()
plt.savefig(r'C:\xyzy\1lhjr\1scrb\hangyezijin2.png',c = 'k')