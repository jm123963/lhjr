from EmQuantAPI import *
from datetime import timedelta, datetime
import time as _time
import traceback
from datetime import *
#import matplotlib as mpl
#import matplotlib.pyplot as plt
#import xlwings as xw
#import xlrd
import numpy as np
import pandas as pd
from pandas import DataFrame
from pylab import mpl
from pandas.plotting import table
import plotly_express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from jupyter_dash import JupyterDash

# 当前时间
date = datetime.today().strftime("%Y-%m-%d")
zscode="000985.CSI,000300.SH,000905.SH,399303.SZ"
fgcode="399373.SZ,399377.SZ,399372.SZ,399376.SZ"
hfcode="CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI"
hycode="801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,\
        801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,\
        801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI"
replace={'000985.CSI':'中证全指','000300.SH':'沪深300','000905.SH':'中证500','399303.SZ':'国证2000','399373.SZ':'大盘价值',
        '399373.SZ':'大盘价值','399377.SZ':'小盘价值','399372.SZ':'大盘成长','399376.SZ':'小盘成长','CI005917.CI':'金融',
        'CI005918.CI':'周期','CI005919.CI':'消费','CI005920.CI':'成长','CI005921.CI':'稳定'}

#调用登录函数（激活后使用，不需要用户名密码）
loginResult = c.start("ForceLogin=1", '')

# 中证全指PB
df=c.csd('000985.CSI','PBMRQ','2005-01-01',""+date+"",f"DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
df['DATES']=df['DATES'].str[:7]
df.CODES = df.CODES.replace(replace)
fig1 = px.line(df,x='DATES',y='PBMRQ',color=df.CODES)
fig1.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=950, height=450,title={'text':'中证全指PB20年走势','y':0.98,'x':0.5,
                'xanchor': 'center','yanchor': 'top'},title_font_size=25,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                 legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
fig1.update_yaxes(type='log')

df=c.csd('000985.CSI','PBMRQ','2013-01-01',""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
df['DATES']=df['DATES'].str[:7]
df.CODES = df.CODES.replace(replace)
fig2 = px.line(df,x='DATES',y='PBMRQ',color=df.CODES)
fig2.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=950, height=450,title={'text':'中证全指PB10年走势','y':0.98,'x':0.5,
                'xanchor': 'center','yanchor': 'top'},title_font_size=25,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                 legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
fig2.update_yaxes(type='log')

# 中证全指PE
df=c.csd('000985.CSI','PETTM','2005-01-01',""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
df['DATES']=df['DATES'].str[:7]
df.CODES = df.CODES.replace(replace)
fig3 = px.line(df,x='DATES',y='PETTM',color=df.CODES)
fig3.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=950, height=450,title={'text':'中证全指PE20年走势','y':0.98,'x':0.5,
                'xanchor': 'center','yanchor': 'top'},title_font_size=25,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                 legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
fig3.update_yaxes(type='log')

df=c.csd('000985.CSI','PETTM','2013-01-01',""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
df['DATES']=df['DATES'].str[:7]
df.CODES = df.CODES.replace(replace)
fig4 = px.line(df,x='DATES',y='PETTM',color=df.CODES)
fig4.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=950, height=450,title={'text':'中证全指PE10年走势','y':0.98,'x':0.5,
                'xanchor': 'center','yanchor': 'top'},title_font_size=25,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                 legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
fig4.update_yaxes(type='log')

# 指数PB
df=c.csd(zscode,'PBMRQ','2005-01-01',""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
df['DATES']=df['DATES'].str[:7]
df.CODES = df.CODES.replace(replace)
fig5 = px.line(df,x='DATES',y='PBMRQ',color=df.CODES)
fig5.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=950, height=450,title={'text':'指数PB20年走势','y':0.98,'x':0.45,
                'xanchor': 'center','yanchor': 'top'},title_font_size=25,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                 legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
fig5.update_yaxes(type='log')

df=c.csd(zscode,"PBMRQ","2005-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
dc=c.css(zscode,"SHORTNAME,PBMRQ","TradeDate="+date+",DelType=1,Rowindex=none,Ispandas=1").dropna()
data=c.css(zscode,"SHORTNAME","Ispandas=1").dropna()
# 变更特定字符
for a,b in zip(data.index,data.SHORTNAME):
    df.CODES = df.CODES.str.replace(a,b)
df.CODES = df.CODES.str.replace("\(申万\)","")
df.CODES = df.CODES.str.replace("\(风格.中信\)","")
# 保留1位小数
dc["PBMRQ"] = dc["PBMRQ"].apply(lambda x:format(x,'.1f'))
fig6 = px.violin(df,x=df.CODES,y="PBMRQ",color=df.CODES,box=True,points='all')
fig6.update_layout(width=950, height=450,title={'text': "指数PB20年分位",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                    title_font_size=25,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
for i in range(0,4):
    y = dc.PBMRQ[i]
    fig6.add_annotation(x=i,y=y,text=f"×{y}",ax=10,ay=0,font={'size': 12})

df=c.csd(zscode,"PBMRQ","2013-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
dc=c.css(zscode,"SHORTNAME,PBMRQ","TradeDate="+date+",DelType=1,Rowindex=none,Ispandas=1").dropna()
data=c.css(zscode,"SHORTNAME","Ispandas=1").dropna()
# 变更特定字符
for a,b in zip(data.index,data.SHORTNAME):
    df.CODES = df.CODES.str.replace(a,b)
df.CODES = df.CODES.str.replace("\(申万\)","")
df.CODES = df.CODES.str.replace("\(风格.中信\)","")
# 保留1位小数
dc["PBMRQ"] = dc["PBMRQ"].apply(lambda x:format(x,'.1f'))
fig7 = px.violin(df,x=df.CODES,y="PBMRQ",color=df.CODES,box=True,points='all')
fig7.update_layout(width=950, height=450,title={'text': "指数PB10年分位",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                    title_font_size=25,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
for i in range(0,4):
    y = dc.PBMRQ[i]
    fig7.add_annotation(x=i,y=y,text=f"×{y}",ax=10,ay=0,font={'size': 12})

# 指数PE
df=c.csd(zscode,'PBMRQ','2005-01-01',""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
df['DATES']=df['DATES'].str[:7]
df.CODES = df.CODES.replace(replace)
fig8 = px.line(df,x='DATES',y='PBMRQ',color=df.CODES)
fig8.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=950, height=450,title={'text':'指数PE20年走势','y':0.98,'x':0.45,
                'xanchor': 'center','yanchor': 'top'},title_font_size=25,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                 legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
fig8.update_yaxes(type='log')

df=c.csd(zscode,"PETTM","2005-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
dc=c.css(zscode,"SHORTNAME,PETTM","TradeDate="+date+",DelType=1,Rowindex=none,Ispandas=1").dropna()
data=c.css(zscode,"SHORTNAME","Ispandas=1").dropna()
# 变更特定字符
for a,b in zip(data.index,data.SHORTNAME):
    df.CODES = df.CODES.str.replace(a,b)
df.CODES = df.CODES.str.replace("\(申万\)","")
df.CODES = df.CODES.str.replace("\(风格.中信\)","")
# 保留1位小数
dc["PETTM"] = dc["PETTM"].apply(lambda x:format(x,'.1f'))
fig9 = px.violin(df,x=df.CODES,y="PETTM",color=df.CODES,box=True,points='all')
fig9.update_layout(width=950, height=450,title={'text': "指数PE20年分位",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                    title_font_size=25,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
for i in range(0,4):
    y = dc.PETTM[i]
    fig9.add_annotation(x=i,y=y,text=f"×{y}",ax=10,ay=0,font={'size': 12})

df=c.csd(zscode,"PETTM","2013-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
dc=c.css(zscode,"SHORTNAME,PETTM","TradeDate="+date+",DelType=1,Rowindex=none,Ispandas=1").dropna()
data=c.css(zscode,"SHORTNAME","Ispandas=1").dropna()
# 变更特定字符
for a,b in zip(data.index,data.SHORTNAME):
    df.CODES = df.CODES.str.replace(a,b)
df.CODES = df.CODES.str.replace("\(申万\)","")
df.CODES = df.CODES.str.replace("\(风格.中信\)","")
# 保留1位小数
dc["PETTM"] = dc["PETTM"].apply(lambda x:format(x,'.1f'))
fig10 = px.violin(df,x=df.CODES,y="PETTM",color=df.CODES,box=True,points='all')
fig10.update_layout(width=950, height=450,title={'text': "指数PE10年分位",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                    title_font_size=25,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
for i in range(0,4):
    y = dc.PETTM[i]
    fig10.add_annotation(x=i,y=y,text=f"×{y}",ax=10,ay=0,font={'size': 12})

# 风格PB
df=c.csd(fgcode,'PBMRQ','2010-01-01',""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
df['DATES']=df['DATES'].str[:7]
df.CODES = df.CODES.replace(replace)
fig11 = px.line(df,x='DATES',y='PBMRQ',color=df.CODES)
fig11.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=950, height=450,title={'text':'风格PB13年走势','y':0.98,'x':0.45,
                'xanchor': 'center','yanchor': 'top'},title_font_size=25,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                 legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
fig11.update_yaxes(type='log')

df=c.csd(fgcode,"PBMRQ","2005-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
dc=c.css(fgcode,"SHORTNAME,PBMRQ","TradeDate="+date+",DelType=1,Rowindex=none,Ispandas=1").dropna()
data=c.css(fgcode,"SHORTNAME","Ispandas=1").dropna()
# 变更特定字符
for a,b in zip(data.index,data.SHORTNAME):
    df.CODES = df.CODES.str.replace(a,b)
df.CODES = df.CODES.str.replace("\(申万\)","")
df.CODES = df.CODES.str.replace("\(风格.中信\)","")
# 保留1位小数
dc["PBMRQ"] = dc["PBMRQ"].apply(lambda x:format(x,'.1f'))
fig12 = px.violin(df,x=df.CODES,y="PBMRQ",color=df.CODES,box=True,points='all')
fig12.update_layout(width=950, height=450,title={'text': "风格PB13年分位",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                    title_font_size=25,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
for i in range(0,4):
    y = dc.PBMRQ[i]
    fig12.add_annotation(x=i,y=y,text=f"×{y}",ax=10,ay=0,font={'size': 12})

# 风格PE
df=c.csd(fgcode,'PETTM','2005-01-01',""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
df['DATES']=df['DATES'].str[:7]
df.CODES = df.CODES.replace(replace)
fig13 = px.line(df,x='DATES',y='PETTM',color=df.CODES)
fig13.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=950, height=450,title={'text':'风格PE13年走势','y':0.98,'x':0.45,
                'xanchor': 'center','yanchor': 'top'},title_font_size=25,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                 legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
fig13.update_yaxes(type='log')

df=c.csd(fgcode,"PETTM","2005-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
dc=c.css(fgcode,"SHORTNAME,PETTM","TradeDate="+date+",DelType=1,Rowindex=none,Ispandas=1").dropna()
data=c.css(fgcode,"SHORTNAME","Ispandas=1").dropna()
# 变更特定字符
for a,b in zip(data.index,data.SHORTNAME):
    df.CODES = df.CODES.str.replace(a,b)
df.CODES = df.CODES.str.replace("\(申万\)","")
df.CODES = df.CODES.str.replace("\(风格.中信\)","")
# 保留1位小数
dc["PETTM"] = dc["PETTM"].apply(lambda x:format(x,'.1f'))
fig14 = px.violin(df,x=df.CODES,y="PETTM",color=df.CODES,box=True,points='all')
fig14.update_layout(width=950, height=450,title={'text': "风格PE13年分位",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                    title_font_size=25,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
for i in range(0,4):
    y = dc.PETTM[i]
    fig14.add_annotation(x=i,y=y,text=f"×{y}",ax=10,ay=0,font={'size': 12})

# 行业风格PB
df=c.csd(hfcode,'PBMRQ','2010-01-01',""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
df['DATES']=df['DATES'].str[:7]
df.CODES = df.CODES.replace(replace)
fig15 = px.line(df,x='DATES',y='PBMRQ',color=df.CODES)
fig15.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=950, height=450,title={'text':'行业风格PB13年走势','y':0.98,'x':0.45,
                'xanchor': 'center','yanchor': 'top'},title_font_size=25,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                 legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
fig15.update_yaxes(type='log')

df=c.csd(hfcode,"PBMRQ","2010-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
dc=c.css(hfcode,"SHORTNAME,PBMRQ","TradeDate="+date+",DelType=1,Rowindex=none,Ispandas=1").dropna()
data=c.css(hfcode,"SHORTNAME","Ispandas=1").dropna()
# 变更特定字符
for a,b in zip(data.index,data.SHORTNAME):
    df.CODES = df.CODES.str.replace(a,b)
df.CODES = df.CODES.str.replace("\(申万\)","")
df.CODES = df.CODES.str.replace("\(风格.中信\)","")
# 保留1位小数
dc["PBMRQ"] = dc["PBMRQ"].apply(lambda x:format(x,'.1f'))
fig16 = px.violin(df,x=df.CODES,y="PBMRQ",color=df.CODES,box=True,points='all')
fig16.update_layout(width=950, height=450,title={'text': "行业风格PB13年分位",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                    title_font_size=25,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
for i in range(0,5):
    y = dc.PBMRQ[i]
    fig16.add_annotation(x=i,y=y,text=f"×{y}",ax=10,ay=0,font={'size': 12})

# 行业风格PE
df=c.csd(hfcode,'PETTM','2010-01-01',""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
df['DATES']=df['DATES'].str[:7]
df.CODES = df.CODES.replace(replace)
fig17 = px.line(df,x='DATES',y='PETTM',color=df.CODES)
fig17.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=950, height=450,title={'text':'行业风格PE13年走势','y':0.98,'x':0.45,
                'xanchor': 'center','yanchor': 'top'},title_font_size=25,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                 legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
fig17.update_yaxes(type='log')

df=c.csd(hfcode,"PETTM","2010-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
dc=c.css(hfcode,"SHORTNAME,PETTM","TradeDate="+date+",DelType=1,Rowindex=none,Ispandas=1").dropna()
data=c.css(hfcode,"SHORTNAME","Ispandas=1").dropna()
# 变更特定字符
for a,b in zip(data.index,data.SHORTNAME):
    df.CODES = df.CODES.str.replace(a,b)
df.CODES = df.CODES.str.replace("\(申万\)","")
df.CODES = df.CODES.str.replace("\(风格.中信\)","")
# 保留1位小数
dc["PETTM"] = dc["PETTM"].apply(lambda x:format(x,'.1f'))
fig18 = px.violin(df,x=df.CODES,y="PETTM",color=df.CODES,box=True,points='all')
fig18.update_layout(width=950, height=450,title={'text': "行业风格PE13年分位",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                    title_font_size=25,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
for i in range(0,5):
    y = dc.PETTM[i]
    fig18.add_annotation(x=i,y=y,text=f"×{y}",ax=10,ay=0,font={'size': 12})

# 行业市净率PBMRQ
dc=c.css(hycode,"SHORTNAME,PBMRQ","TradeDate="+date+",DelType=1,Rowindex=none,Ispandas=1").dropna()
dc=dc.sort_values(by="PBMRQ",ascending=True)
dc=dc.reset_index(drop=True)
newcode=dc.iloc[:,0].to_list()
df=c.csd(newcode,'PBMRQ',"2005-01-01",""+date+"",f"DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
print(df)
data=c.css(newcode,"SHORTNAME","Ispandas=1").dropna()
# 变更特定字符
for a,b in zip(data.index,data.SHORTNAME):
    df.CODES = df.CODES.str.replace(a,b)
df.CODES = df.CODES.str.replace("\(申万\)","")
df.CODES = df.CODES.str.replace("\(风格.中信\)","")
# 保留1位小数
dc['PBMRQ'] = dc['PBMRQ'].apply(lambda x:format(x,'.1f'))

fig19 = px.violin(df,x=df.CODES,y='PBMRQ',color=df.CODES,box=True)
fig19.update_layout(width=950, height=450,title={'text': "行业PB20年分位",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                    title_font_size=25,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)
for i in range(0,31):
    y = dc.PBMRQ[i]
    fig19.add_annotation(x=i,y=y,text=f"×{y}",ax=10,ay=0,font={'size': 12})

dc=c.css(hycode,"SHORTNAME,PBMRQ","TradeDate="+date+",DelType=1,Rowindex=none,Ispandas=1").dropna()
dc=dc.sort_values(by="PBMRQ",ascending=True)
dc=dc.reset_index(drop=True)
newcode=dc.iloc[:,0].to_list()
df=c.csd(newcode,'PBMRQ',"2013-01-01",""+date+"",f"DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
data=c.css(newcode,"SHORTNAME","Ispandas=1").dropna()
# 变更特定字符
for a,b in zip(data.index,data.SHORTNAME):
    df.CODES = df.CODES.str.replace(a,b)
df.CODES = df.CODES.str.replace("\(申万\)","")
df.CODES = df.CODES.str.replace("\(风格.中信\)","")
# 保留1位小数
dc['PBMRQ'] = dc['PBMRQ'].apply(lambda x:format(x,'.1f'))

fig20 = px.violin(df,x=df.CODES,y='PBMRQ',color=df.CODES,box=True)
fig20.update_layout(width=950, height=450,title={'text': "行业PB10年分位",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                    title_font_size=25,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)
for i in range(0,31):
    y = dc.PBMRQ[i]
    fig20.add_annotation(x=i,y=y,text=f"×{y}",ax=10,ay=0,font={'size': 12})

# 行业市盈率PETTM
def extreme_percentile(series,min = 0.01,max = 0.99):
  # 百分位法去极值
  series = series.sort_values()
  q = series.quantile([min,max])
  return np.clip(series,q.iloc[0],q.iloc[1])

dc=c.css(hycode,"SHORTNAME,PETTM","TradeDate="+date+",DelType=1,Rowindex=none,Ispandas=1").dropna()
dc=dc.sort_values(by="PETTM",ascending=True)
dc=dc.reset_index(drop=True)
# 负值置尾
dc=dc.reindex([5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,4,3,2,1,0])
dc=dc.reset_index(drop=True)
newcode=dc.iloc[:,0].to_list()
df=c.csd(newcode,'PETTM',"2005-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
df['PETTM'] = extreme_percentile(df['PETTM'])
data=c.css(newcode,"SHORTNAME","Ispandas=1").dropna()
# 变更特定字符
for a,b in zip(data.index,data.SHORTNAME):
    df.CODES = df.CODES.str.replace(a,b)
df.CODES = df.CODES.str.replace("\(申万\)","")
df.CODES = df.CODES.str.replace("\(风格.中信\)","")
# 保留1位小数
dc['PETTM'] = dc['PETTM'].apply(lambda x:format(x,'.1f'))

fig21 = px.violin(df,x=df.CODES,y='PETTM',color=df.CODES,box=True)
fig21.update_layout(width=950, height=450,title={'text': "行业PE20年分位",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                    title_font_size=25,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)
for i in range(0,31):
    y = dc.PETTM[i]
    fig21.add_annotation(x=i,y=y,text=f"×{y}",ax=10,ay=0,font={'size': 12})

dc=c.css(hycode,"SHORTNAME,PETTM","TradeDate="+date+",DelType=1,Rowindex=none,Ispandas=1").dropna()
dc=dc.sort_values(by="PETTM",ascending=True)
dc=dc.reset_index(drop=True)
# 负值置尾
dc=dc.reindex([5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,4,3,2,1,0])
dc=dc.reset_index(drop=True)
newcode=dc.iloc[:,0].to_list()
df=c.csd(newcode,'PETTM',"2013-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
df['PETTM'] = extreme_percentile(df['PETTM'])
data=c.css(newcode,"SHORTNAME","Ispandas=1").dropna()
# 变更特定字符
for a,b in zip(data.index,data.SHORTNAME):
    df.CODES = df.CODES.str.replace(a,b)
df.CODES = df.CODES.str.replace("\(申万\)","")
df.CODES = df.CODES.str.replace("\(风格.中信\)","")
# 保留1位小数
dc['PETTM'] = dc['PETTM'].apply(lambda x:format(x,'.1f'))

fig22 = px.violin(df,x=df.CODES,y='PETTM',color=df.CODES,box=True)
fig22.update_layout(width=950, height=450,title={'text': "行业PE10年分位",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                    title_font_size=25,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)
for i in range(0,31):
    y = dc.PETTM[i]
    fig22.add_annotation(x=i,y=y,text=f"×{y}",ax=10,ay=0,font={'size': 12})

# dash可视化
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        dcc.Graph(
            id='graph1',
            figure=fig1
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph2',
            figure=fig2
        ),  
    ], className='row'), 
    html.Div([
        dcc.Graph(
            id='graph3',
            figure=fig3
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph4',
            figure=fig4
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph5',
            figure=fig5
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph6',
            figure=fig6
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph7',
            figure=fig7
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph8',
            figure=fig8
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph9',
            figure=fig9
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph10',
            figure=fig10
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph11',
            figure=fig11
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph12',
            figure=fig12
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph13',
            figure=fig13
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph14',
            figure=fig14
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph15',
            figure=fig15
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph16',
            figure=fig16
        ),  
    ], className='row'),
        html.Div([
        dcc.Graph(
            id='graph17',
            figure=fig17
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph18',
            figure=fig18
        ),  
    ], className='row'),
        html.Div([
        dcc.Graph(
            id='graph19',
            figure=fig19
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph20',
            figure=fig20
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph21',
            figure=fig21
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph22',
            figure=fig22
        ),  
    ], className='row'),
])

if __name__ == '__main__':
    app.run_server(port=2222)