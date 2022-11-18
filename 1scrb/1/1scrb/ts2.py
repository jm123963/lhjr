import numpy as np
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
import xlrd
###########################################################################
plt.rcParams['font.sans-serif']=['SimHei']#中文 
plt.rcParams['axes.unicode_minus']=False  #显示负号
# ####################################data#################################
n = ['农林牧渔','基础化工','钢铁','有色金属','电子','家用电器','食品饮料','纺织服饰','轻工制造','医药生物','公用事业','交通运输','房地产','商业贸易','社会服务','综合','建筑材料','建筑装饰','电力设备','国防军工','计算机','传媒','通信','银行','非银金融','汽车','机械设备','煤炭','石油石化','环保','美容护理']

import xlwings as xw

wb = xw.Book(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.xls')
sht = wb.sheets[0]
a = sht.range('b2:b32').value
wb.close()

from pandas import DataFrame
l1 = n
l2 = a
df = DataFrame({'名称': l1, '行业涨幅': l2})
df.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.xls', sheet_name='Sheet1', index=False)

import pandas as pd
stexcel=pd.read_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.xls')
#ascending 默认等于True，按从小到大排列，改为False 按从大到小排
stexcel.sort_values(by='行业涨幅',inplace=True,ascending=False)
stexcel.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.xls', sheet_name='Sheet1', index=False)

#转整数
import xlrd
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.xls')
table = data.sheets()[0]
xin = []
cap2 = table.col_values(1)
for i in range(1,32):
    xin.append('%.0f' % cap2[i])
from pandas import DataFrame
n =['农林牧渔','基础化工','钢铁','有色金属','电子','家用电器','食品饮料','纺织服饰','轻工制造','医药生物','公用事业','交通运输','房地产','商业贸易','社会服务','综合','建筑材料','建筑装饰','电力设备','国防军工','计算机','传媒','通信','银行','非银金融','汽车','机械设备','煤炭','石油石化','环保','美容护理']
l1 = n
l2 = xin
df = DataFrame({'名称': l1, '涨幅': l2})
df.to_excel(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.xls', sheet_name='Sheet1', index=False)
#制图
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import xlrd

#指定字体为SimHei，用于显示中文，如果Ariel,中文会乱码
mpl.rcParams["font.sans-serif"]=["SimHei"]
#用来正常显示负号
mpl.rcParams["axes.unicode_minus"]=False

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.xls')
table = data.sheets()[0]

x1=[]   
cap1 = table.col_values(0)
for i in range(1,32):
    x1.append(cap1[i]) 
    
y1=[]   
cap2 = table.col_values(1)
for i in range(1,32):
    y1.append(float(cap2[i]))

# ####################################draw#################################
fig=plt.figure(figsize=(12,8),dpi=300)#添加画布等
ax=fig.add_axes([0,0,0.9,0.9])

bar1=ax.bar(x1,y1,
            color=np.where(np.array(y1)>0,'c','r'), #判断大于0的为红色，负的为蓝色
            width=0.55,   #柱形宽度
            align='center', #柱形的位置edge/center 
            hatch=" ",
            #alpha=0.8,    #柱形透明度
            #hatch='*',    #柱形表明的形状样式
            edgecolor='gray',#柱形边缘颜色
            #bottom=0.01   #柱形离底部的距离
          )
##########################################################################
#ax.set(xlim=(1999,2021),ylim=(-11,11))   #设置x、y轴的最大最小范围
#ax.set_xticks(np.linspace(2000, 2020, 5)) #设置x轴显示的标签
plt.xticks(rotation=90,fontsize=15)
plt.yticks(fontsize=20)
for a,b in zip(x1,y1):
    plt.text(a,b,'%.0f' % b, ha='center', va= 'bottom',fontsize=10)
ax.text(2010,-3,'某个阈值')             #添加注释
ax.axhline(y=0,c='k',ls=':',lw=1)    #添加水平线，设置颜色，位置，水平线的style
#设置轴的参数，间隔
#ax.tick_params(axis='both',which='both',direction='in')
#ax.yaxis.set_minor_locator(mticker.MultipleLocator(5))
#ax.xaxis.set_minor_locator(mticker.MultipleLocator(5))
# 设置label
ax.set_xlabel(u"")
ax.set_ylabel(u"")
ax.set_title('250日行业涨幅%',fontsize=20)
ax.legend()
plt.show()

