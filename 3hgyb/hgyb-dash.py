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

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from jupyter_dash import JupyterDash

#调用登录函数（激活后使用，不需要用户名密码）
loginResult = c.start("ForceLogin=1", '')

# 当前时间
date = datetime.today().strftime("%Y-%m-%d")
def zs(code,sdate,dtick,text,image):
    df=c.edb(code, f"IsLatest=0,StartDate={sdate},EndDate="+date+",Ispandas=1")
    df['DATES']=df['DATES'].str[:7]
    fig = px.line(df,x='DATES',y='RESULT')
    fig.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =dtick,),width=970,height=500,title={'text':text,'y':0.98,'x':0.5,'xanchor': 'center',
                    'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                    legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
    fig.write_image(Fr'C:\xyzy\1lhjr\3hgyb\{image}.png',scale=3)

# GDP同比增速 
df=c.edb('EMM00000012', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig1 = px.line(df,x='DATES',y='RESULT')
fig1.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=970,height=500,title={'text':'GDP同比增速','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# CPI月同比 
df=c.edb('EMM00072301', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig2 = px.line(df,x='DATES',y='RESULT')
fig2.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =36,),width=970,height=500,title={'text':'通货膨胀-CPI月同比','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# PPI月同比 
df=c.edb('EMM00073348', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig3 = px.line(df,x='DATES',y='RESULT')
fig3.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =24,),width=970,height=500,title={'text':'通货膨胀-PPI月同比','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# PMI指数 
df=c.edb('EMM00121996', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig4 = px.line(df,x='DATES',y='RESULT')
fig4.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =24,),width=970,height=500,title={'text':'景气度-采购经理指数','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 失业率 
df=c.edb('EMM00631597', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig5 = px.line(df,x='DATES',y='RESULT')
fig5.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=970,height=500,title={'text':'景气度-失业率','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 固定资产投资完成额累计同比（%）
df=c.edb('EMM00027210', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig6 = px.line(df,x='DATES',y='RESULT')
fig6.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =33,),width=970,height=500,title={'text':'需求-固定资产投资完成额累计同比（%）','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 固定资产投资完成额:制造业:累计同比
df=c.edb('EMM00027220', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig7 = px.line(df,x='DATES',y='RESULT')
fig7.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =33,),width=970,height=500,title={'text':'需求-固定资产投资完成额:制造业:累计同比（%）','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 固定资产投资完成额:建筑业:累计同比
df=c.edb('EMM00027257', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig8 = px.line(df,x='DATES',y='RESULT')
fig8.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =33,),width=970,height=500,title={'text':'需求-固定资产投资完成额:建筑业:累计同比（%）','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 房地产开发投资完成额：累计同比
df=c.edb('EMM00039176', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig9 = px.line(df,x='DATES',y='RESULT')
fig9.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =33,),width=970,height=500,title={'text':'需求-房地产开发投资完成额：累计同比（%）','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 出口金额:累计同比
df=c.edb('EMM00053070', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig10 = px.line(df,x='DATES',y='RESULT')
fig10.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =33,),width=970,height=500,title={'text':'需求-出口金额:累计同比（%）','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 进口金额:累计同比
df=c.edb('EMM00053094', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig11 = px.line(df,x='DATES',y='RESULT')
fig11.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =33,),width=970,height=500,title={'text':'需求-进口金额:累计同比（%）','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 社会消费品零售总额累计同比（%）
df=c.edb('EMM00063225', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig12 = px.line(df,x='DATES',y='RESULT')
fig12.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =33,),width=970,height=500,title={'text':'需求-社会消费品零售总额累计同比（%）','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 工业增加值:累计同比（%）
df=c.edb('EMM00008464', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig13 = px.line(df,x='DATES',y='RESULT')
fig13.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =33,),width=970,height=500,title={'text':'供给-工业增加值:累计同比（%）','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 离岸人民币汇率
df=c.edb('EMM00618963', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig14 = px.line(df,x='DATES',y='RESULT')
fig14.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=970,height=500,title={'text':'信贷-离岸人民币汇率','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 国债到期收益率:10年
df=c.edb('E1001827', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig15 = px.line(df,x='DATES',y='RESULT')
fig15.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=970,height=500,title={'text':'信贷-国债到期收益率:10年','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 国债到期收益率:5年
df=c.edb('E1001823', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig16 = px.line(df,x='DATES',y='RESULT')
fig16.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=970,height=500,title={'text':'信贷-国债到期收益率:5年','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 国债到期收益率:1年
df=c.edb('E1001819', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig17 = px.line(df,x='DATES',y='RESULT')
fig17.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=970,height=500,title={'text':'信贷-国债到期收益率:1年','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 社会融资增量:累计值(亿)
df=c.edb('EMM00088692', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig18 = px.line(df,x='DATES',y='RESULT')
fig18.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=970,height=500,title={'text':'信贷-社会融资增量:累计值(亿)','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 社会融资增量:新增人民币贷款:累计值(亿)
df=c.edb('EMM00088693', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig19 = px.line(df,x='DATES',y='RESULT')
fig19.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=970,height=500,title={'text':'信贷-社会融资增量:新增人民币贷款:累计值(亿)','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# M1:同比
df=c.edb('EMM00087084', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig20 = px.line(df,x='DATES',y='RESULT')
fig20.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=970,height=500,title={'text':'信贷-M1:同比','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# M2:同比
df=c.edb('EMM00087086', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig21 = px.line(df,x='DATES',y='RESULT')
fig21.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=970,height=500,title={'text':'信贷-M2:同比','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 实体经济部门杠杆率
df=c.edb('EMM01244359', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig22 = px.line(df,x='DATES',y='RESULT')
fig22.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=970,height=500,title={'text':'信贷-实体经济部门杠杆率','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 政府部门杠杆率
df=c.edb('EMM01244356', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig23 = px.line(df,x='DATES',y='RESULT')
fig23.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=970,height=500,title={'text':'信贷-政府部门杠杆率','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 居民部门杠杆率
df=c.edb('EMM01244354', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig24 = px.line(df,x='DATES',y='RESULT')
fig24.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=970,height=500,title={'text':'信贷-居民部门杠杆率','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 公共财政收入:累计同比(%)
df=c.edb('EMM00058449', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig25 = px.line(df,x='DATES',y='RESULT')
fig25.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =36,),width=970,height=500,title={'text':'财政-公共财政收入:累计同比(%)','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 公共财政支出:累计同比(%)-
df=c.edb('EMM00058496', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig26 = px.line(df,x='DATES',y='RESULT')
fig26.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =36,),width=970,height=500,title={'text':'财政-公共财政支出:累计同比(%)','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 地方政府债券平均发行利率（%）
df=c.edb('EMM01259592', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig27 = px.line(df,x='DATES',y='RESULT')
fig27.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=970,height=500,title={'text':'财政-地方政府债券平均发行利率（%）','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 地方政府债券发行额:累计值（亿）
df=c.edb('EMM01259582', "IsLatest=0,StartDate=1990-01-01,EndDate="+date+",Ispandas=1")
df['DATES']=df['DATES'].str[:7]
fig28 = px.line(df,x='DATES',y='RESULT')
fig28.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=970,height=500,title={'text':'财政-地方政府债券发行额:累计值（亿）','y':0.98,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

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
    html.Div([
        dcc.Graph(
            id='graph23',
            figure=fig23
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph24',
            figure=fig24
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph25',
            figure=fig25
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph26',
            figure=fig26
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph27',
            figure=fig27
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph28',
            figure=fig28
        ),  
    ], className='row'),
])

if __name__ == '__main__':
    app.run_server(port=3333)