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

data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu0.xls')
table = data.sheets()[0]
x1=[]   
cap1 = table.col_values(3)
for i in range(1,5):
    x1.append(cap1[i].strip("指数"))
y1=[]   
cap2 = table.col_values(4)
for i in range(1,5):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.1f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1200,height=600,title={'text': "当日日指数涨幅%",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=45,font_size=35,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
#fig.write_image(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu0.png',scale=2)
fig.show()

import plotly.io as pio
pio.write_html(fig, file=r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu0.html')