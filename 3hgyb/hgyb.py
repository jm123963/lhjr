# -*- coding:utf-8 -*-
from EmQuantAPI import *
from datetime import timedelta, datetime
import pandas as pd
from dash import Dash, Input, Output, ctx, html, dcc
import plotly.express as px
import plotly.graph_objects as go

#调用登录函数（激活后使用，不需要用户名密码）
loginResult = c.start("ForceLogin=1", '')
# 当前时间
date = datetime.today().strftime("%Y-%m-%d")

# GDP同比增速 
df1=c.edb('EMM00000012', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df1['DATES']=df1['DATES'].str[:7]
# 缺失值赋0
df1=df1.fillna(method='ffill')
fig1 = px.line(df1,x='DATES',y='RESULT')
fig1.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=1300,height=620,title={'text':'GDP同比增速','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
# CPI月同比 
df2=c.edb('EMM00072301', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df2['DATES']=df2['DATES'].str[:7]
# 缺失值赋0
df2=df2.fillna(method='ffill')
fig2 = px.line(df2,x='DATES',y='RESULT')
fig2.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =36,),width=1300,height=620,title={'text':'通货膨胀-CPI月同比','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
# PPI月同比
df3=c.edb('EMM00073348', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df3['DATES']=df3['DATES'].str[:7]
# 缺失值赋0
df3=df3.fillna(method='ffill')
fig3 = px.line(df3,x='DATES',y='RESULT')
fig3.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =24,),width=1300,height=620,title={'text':'通货膨胀-PPI月同比','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
# PMI指数 
df4=c.edb('EMM00121996', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df4['DATES']=df4['DATES'].str[:7]
# 缺失值赋0
df4=df4.fillna(method='ffill')
fig4 = px.line(df4,x='DATES',y='RESULT')
fig4.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =24,),width=1300,height=620,title={'text':'景气度-采购经理人指数','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
# 失业率 
df5=c.edb('EMM00631597', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df5['DATES']=df5['DATES'].str[:7]
# 缺失值赋0
df5=df5.fillna(method='ffill')
fig5 = px.line(df5,x='DATES',y='RESULT')
fig5.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=1300,height=620,title={'text':'景气度-失业率','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 固定资产投资完成额累计同比（%）
df6=c.edb('EMM00027210', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df6['DATES']=df6['DATES'].str[:7]
# 缺失值赋0
df6=df6.fillna(method='ffill')
fig6 = px.line(df6,x='DATES',y='RESULT')
fig6.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =24,),width=1300,height=620,title={'text':'需求-固定资产投资完成额累计同比（%）','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 固定资产投资完成额:制造业:累计同比
df7=c.edb('EMM00027220', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df7['DATES']=df7['DATES'].str[:7]
# 缺失值赋0
df7=df7.fillna(method='ffill')
fig7 = px.line(df7,x='DATES',y='RESULT')
fig7.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =24,),width=1300,height=620,title={'text':'需求-固定资产投资完成额:制造业:累计同比（%）','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 固定资产投资完成额:建筑业:累计同比
df8=c.edb('EMM00027257', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df8['DATES']=df8['DATES'].str[:7]
# 缺失值赋0
df8=df8.fillna(method='ffill')
fig8 = px.line(df8,x='DATES',y='RESULT')
fig8.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =24,),width=1300,height=620,title={'text':'需求-固定资产投资完成额:建筑业:累计同比（%）','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 房地产开发投资完成额：累计同比
df9=c.edb('EMM00039176', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df9['DATES']=df9['DATES'].str[:7]
# 缺失值赋0
df9=df9.fillna(method='ffill')
fig9 = px.line(df9,x='DATES',y='RESULT')
fig9.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =24,),width=1300,height=620,title={'text':'需求-房地产开发投资完成额：累计同比（%）','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 出口金额:累计同比
df10=c.edb('EMM00053070', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df10['DATES']=df10['DATES'].str[:7]
# 缺失值赋0
df10=df5.fillna(method='ffill')
fig10 = px.line(df10,x='DATES',y='RESULT')
fig10.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =24,),width=1300,height=620,title={'text':'需求-出口金额:累计同比（%）','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
   
# 进口金额:累计同比
df11=c.edb('EMM00053094', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df11['DATES']=df11['DATES'].str[:7]
# 缺失值赋0
df11=df11.fillna(method='ffill')
fig11 = px.line(df11,x='DATES',y='RESULT')
fig11.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =24,),width=1300,height=620,title={'text':'需求-进口金额:累计同比（%）','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 社会消费品零售总额累计同比（%）
df12=c.edb('EMM00063225', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df12['DATES']=df12['DATES'].str[:7]
# 缺失值赋0
df12=df12.fillna(method='ffill')
fig12 = px.line(df12,x='DATES',y='RESULT')
fig12.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =24,),width=1300,height=620,title={'text':'需求-社会消费品零售总额累计同比（%）','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 工业增加值:累计同比（%）
df13=c.edb('EMM00008464', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df13['DATES']=df13['DATES'].str[:7]
# 缺失值赋0
df13=df13.fillna(method='ffill')
fig13 = px.line(df5,x='DATES',y='RESULT')
fig13.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =24,),width=1300,height=620,title={'text':'供给-工业增加值:累计同比（%）','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 离岸人民币汇率
df14=c.edb('EMM00618963', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df14['DATES']=df14['DATES'].str[:7]
# 缺失值赋0
df14=df14.fillna(method='ffill')
fig14 = px.line(df14,x='DATES',y='RESULT')
fig14.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=1300,height=620,title={'text':'离岸人民币汇率','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 国债到期收益率:10年
df15=c.edb('E1001827', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df15['DATES']=df15['DATES'].str[:7]
# 缺失值赋0
df15=df15.fillna(method='ffill')
fig15 = px.line(df15,x='DATES',y='RESULT')
fig15.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=1300,height=620,title={'text':'国债到期收益率:10年','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 国债到期收益率:5年
df16=c.edb('E1001823', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df16['DATES']=df16['DATES'].str[:7]
# 缺失值赋0
df16=df16.fillna(method='ffill')
fig16 = px.line(df16,x='DATES',y='RESULT')
fig16.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=1300,height=620,title={'text':'国债到期收益率:5年','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 国债到期收益率:1年
df17=c.edb('E1001819', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df17['DATES']=df17['DATES'].str[:7]
# 缺失值赋0
df17=df5.fillna(method='ffill')
fig17 = px.line(df17,x='DATES',y='RESULT')
fig17.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=1300,height=620,title={'text':'国债到期收益率:1年','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 社会融资增量:累计值(亿)
df18=c.edb('EMM00088692', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df18['DATES']=df18['DATES'].str[:7]
# 缺失值赋0
df18=df18.fillna(method='ffill')
fig18 = px.line(df18,x='DATES',y='RESULT')
fig18.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =24,),width=1300,height=620,title={'text':'社会融资增量:累计值(亿)','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 社会融资增量:新增人民币贷款:累计值(亿)
df19=c.edb('EMM00088693', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df19['DATES']=df19['DATES'].str[:7]
# 缺失值赋0
df19=df19.fillna(method='ffill')
fig19 = px.line(df19,x='DATES',y='RESULT')
fig19.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =24,),width=1300,height=620,title={'text':'社会融资增量:新增人民币贷款:累计值(亿)','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# M1:同比
df20=c.edb('EMM00087084', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df20['DATES']=df20['DATES'].str[:7]
# 缺失值赋0
df20=df20.fillna(method='ffill')
fig20 = px.line(df20,x='DATES',y='RESULT')
fig20.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =24,),width=1300,height=620,title={'text':'M1:同比','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# M2:同比
df21=c.edb('EMM00087086', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df21['DATES']=df21['DATES'].str[:7]
# 缺失值赋0
df21=df21.fillna(method='ffill')
fig21 = px.line(df21,x='DATES',y='RESULT')
fig21.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =24,),width=1300,height=620,title={'text':'M2:同比','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 实体经济部门杠杆率
df22=c.edb('EMM01244359', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df22['DATES']=df22['DATES'].str[:7]
# 缺失值赋0
df22=df22.fillna(method='ffill')
fig22 = px.line(df22,x='DATES',y='RESULT')
fig22.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=1300,height=620,title={'text':'实体经济部门杠杆率','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 政府部门杠杆率
df23=c.edb('EMM01244356', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df23['DATES']=df23['DATES'].str[:7]
# 缺失值赋0
df23=df23.fillna(method='ffill')
fig23 = px.line(df23,x='DATES',y='RESULT')
fig23.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=1300,height=620,title={'text':'政府部门杠杆率','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 居民部门杠杆率
df24=c.edb('EMM01244354', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df24['DATES']=df24['DATES'].str[:7]
# 缺失值赋0
df24=df24.fillna(method='ffill')
fig24 = px.line(df24,x='DATES',y='RESULT')
fig24.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=1300,height=620,title={'text':'居民部门杠杆率','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 公共财政收入:累计同比(%)
df25=c.edb('EMM00058449', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df25['DATES']=df25['DATES'].str[:7]
# 缺失值赋0
df25=df25.fillna(method='ffill')
fig25 = px.line(df25,x='DATES',y='RESULT')
fig25.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =24,),width=1300,height=620,title={'text':'公共财政收入:累计同比(%)','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 公共财政支出:累计同比(%)-
df26=c.edb('EMM00058496', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df26['DATES']=df26['DATES'].str[:7]
# 缺失值赋0
df26=df26.fillna(method='ffill')
fig26 = px.line(df26,x='DATES',y='RESULT')
fig26.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =24,),width=1300,height=620,title={'text':'公共财政支出:累计同比(%)','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 地方政府债券平均发行利率（%）
df27=c.edb('EMM01259592', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df27['DATES']=df27['DATES'].str[:7]
# 缺失值赋0
df27=df27.fillna(method='ffill')
fig27 = px.line(df27,x='DATES',y='RESULT')
fig27.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=1300,height=620,title={'text':'地方政府债券平均发行利率（%）','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

# 地方政府债券发行额:累计值（亿）
df28=c.edb('EMM01259582', "IsLatest=0,StartDate=1990/01/01,EndDate="+date+",Ispandas=1")
df28['DATES']=df28['DATES'].str[:7]
# 缺失值赋0
df28=df28.fillna(method='ffill')
fig28 = px.line(df28,x='DATES',y='RESULT')
fig28.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =12,),width=1300,height=620,title={'text':'地方政府债券发行额:累计值（亿）','y':0.96,'x':0.5,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))

app = Dash(__name__)

app.layout = html.Div([
    html.Button('GDP', id='gdp'),
    html.Button('CPI', id='cpi'),
    html.Button('PPI', id='ppi'),
    html.Button('采购指数', id='pmi'),
    html.Button('失业率', id='syl'),
    html.Button('投资', id='tzwc'),
    html.Button('制造', id='zzy'),
    html.Button('建筑', id='jzy'),
    html.Button('房产', id='fdc'),
    html.Button('出口', id='ck'),
    html.Button('进口', id='jk'),
    html.Button('社消', id='sx'),
    html.Button('工业', id='gy'),
    html.Button('汇率', id='hl'),
    html.Button('10年国债', id='gz10'),
    html.Button('5年国债', id='gz5'),
    html.Button('1年国债', id='gz1'),
    html.Button('社融', id='sr'),
    html.Button('贷款', id='dk'),
    html.Button('M1', id='m1'),
    html.Button('M2', id='m2'),
    html.Button('实体', id='stgg'),
    html.Button('政府', id='zfgg'),
    html.Button('居民', id='jmgg'),
    html.Button('财收', id='czsr'),
    html.Button('财付', id='czzc'),
    html.Button('政债利率', id='zfzqll'),
    html.Button('政债额', id='zfzqe'),
    dcc.Graph(id='graph')
])

@app.callback(
    Output('graph', 'figure'),
    Input('gdp', 'n_clicks'),
    Input('cpi', 'n_clicks'),
    Input('ppi', 'n_clicks'),
    Input('pmi', 'n_clicks'),
    Input('syl', 'n_clicks'),
    Input('tzwc', 'n_clicks'),
    Input('zzy', 'n_clicks'),
    Input('jzy', 'n_clicks'),
    Input('fdc', 'n_clicks'),
    Input('ck', 'n_clicks'),
    Input('jk', 'n_clicks'),
    Input('sx', 'n_clicks'),
    Input('gy', 'n_clicks'),
    Input('hl', 'n_clicks'),
    Input('gz10', 'n_clicks'),
    Input('gz5', 'n_clicks'),
    Input('gz1', 'n_clicks'),
    Input('sr', 'n_clicks'),
    Input('dk', 'n_clicks'),
    Input('m1', 'n_clicks'),
    Input('m2', 'n_clicks'),
    Input('stgg', 'n_clicks'),
    Input('zfgg', 'n_clicks'),
    Input('jmgg', 'n_clicks'),
    Input('czsr', 'n_clicks'),
    Input('czzc', 'n_clicks'),
    Input('zfzqll', 'n_clicks'),
    Input('zfzqe', 'n_clicks'),
    prevent_initial_call=True
)
def update_graph(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b17,b18,b19,b20,b21,b22,b23,b24,b25,b26,b27,b28):
    triggered_id = ctx.triggered_id
    print(triggered_id)
    if triggered_id == 'gdp':
         return fig1
    elif triggered_id == 'cpi':
         return fig2
    elif triggered_id == 'ppi':
         return fig3
    elif triggered_id == 'pmi':
         return fig4
    elif triggered_id == 'syl':
         return fig5
    elif triggered_id == 'tzwc':
         return tzwc_graph()
    elif triggered_id == 'zzy':
         return zzy_graph()
    elif triggered_id == 'jzy':
         return jzy_graph()
    elif triggered_id == 'fdc':
         return fdc_graph()
    elif triggered_id == 'ck':
         return ck_graph()
    if triggered_id == 'jk':
         return jk_graph()
    elif triggered_id == 'sx':
         return sx_graph()
    elif triggered_id == 'gy':
         return gy_graph()
    elif triggered_id == 'hl':
         return hl_graph()
    elif triggered_id == 'gz10':
         return gz10_graph()
    elif triggered_id == 'gz5':
         return gz5_graph()
    elif triggered_id == 'gz1':
         return gz1_graph()
    elif triggered_id == 'sr':
         return sr_graph()
    elif triggered_id == 'dk':
         return dk_graph()
    elif triggered_id == 'm1':
         return m1_graph()
    elif triggered_id == 'm2':
         return m2_graph()
    elif triggered_id == 'stgg':
         return stgg_graph()
    elif triggered_id == 'zfgg':
         return zfgg_graph()
    elif triggered_id == 'jmgg':
         return jmgg_graph()
    elif triggered_id == 'czsr':
         return czsr_graph()
    elif triggered_id == 'czzc':
         return czzc_graph()
    elif triggered_id == 'zfzqll':
         return zfzqll_graph()
    elif triggered_id == 'zfzqe':
         return zfzqe_graph()

def gdp_graph():
    return fig1
def cpi_graph():
    return fig2
def ppi_graph():
    return fig3
def pmi_graph():
    return fig4
def syl_graph():
    return fig5
def tzwc_graph():
    return fig6
def zzy_graph():
    return fig7
def jzy_graph():
    return fig8
def fdc_graph():
    return fig9
def ck_graph():
    return fig10
def jk_graph():
    return fig11
def sx_graph():
    return fig12
def gy_graph():
    return fig13
def hl_graph():
    return fig14
def gz10_graph():
    return fig15
def gz5_graph():
    return fig16
def gz1_graph():
    return fig17
def sr_graph():
    return fig18
def dk_graph():
    return fig19
def m1_graph():
    return fig20
def m2_graph():
    return fig21
def stgg_graph():
    return fig22
def zfgg_graph():
    return fig23
def jmgg_graph():
    return fig24
def czsr_graph():
    return fig25
def czzc_graph():
    return fig26
def zfzqll_graph():
    return fig27
def zfzqe_graph():
    return fig28

if __name__ == '__main__':
    app.run_server(debug=True,port=3333)