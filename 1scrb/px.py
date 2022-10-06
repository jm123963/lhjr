# -*- coding: utf-8 -*-
from EmQuantAPI import *
from datetime import timedelta, datetime
import time as _time
import traceback
import numpy as np
import pandas as pd
import plotly_express as px
import xlrd 

x1=['中证全指','沪深300','中证500','中证1000']
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu10.xls')
table = data.sheets()[0]
y1=[]   
cap2 = table.col_values(2)
for i in range(1,5):
    y1.append(cap2[i])
fig = px.bar(data,x=x1,y=y1,text=y1)
fig.update_traces(texttemplate='%{text:.1f}',textposition='inside',marker=dict(color=np.where(np.array(y1)>0,'red','limegreen'))) 
fig.update_layout(width=1500,height=700,title={'text': "10日指数涨幅",'y':0.94,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=25,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
#fig.write_image(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu10.png')
fig.show()