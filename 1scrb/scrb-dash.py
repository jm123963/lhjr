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

# 调用登录函数（激活后使用，不需要用户名密码）
loginResult = c.start("ForceLogin=1", '')

# 当前时间
date = datetime.today().strftime("%Y-%m-%d")
tradedates=c.tradedates("2021-01-01", ""+date+"")
offday=[-1,-5,-10,-20,-60,-120,-250]
zjday=[-1,-5,-10]
zscode="000985.CSI,000300.SH,000905.SH,399303.SZ"
fgcode="399373.SZ,399377.SZ,399372.SZ,399376.SZ"
hfcode="CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI"
hycode="801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,\
        801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,\
        801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI"
hy2code="801012.SWI,801014.SWI,801015.SWI,801016.SWI,801017.SWI,801018.SWI,801032.SWI,801033.SWI,801034.SWI,801036.SWI,801037.SWI,801038.SWI,801039.SWI,\
        801043.SWI,801044.SWI,801045.SWI,801051.SWI,801053.SWI,801054.SWI,801055.SWI,801056.SWI,801072.SWI,801074.SWI,801076.SWI,801077.SWI,801078.SWI,\
        801081.SWI,801082.SWI,801083.SWI,801084.SWI,801085.SWI,801086.SWI,801092.SWI,801093.SWI,801095.SWI,801096.SWI,801101.SWI,801102.SWI,801103.SWI,\
        801104.SWI,801111.SWI,801112.SWI,801113.SWI,801114.SWI,801115.SWI,801116.SWI,801124.SWI,801125.SWI,801126.SWI,801127.SWI,801128.SWI,801129.SWI,\
        801131.SWI,801132.SWI,801133.SWI,801141.SWI,801142.SWI,801143.SWI,801145.SWI,801151.SWI,801152.SWI,801153.SWI,801154.SWI,801155.SWI,801156.SWI,\
        801161.SWI,801163.SWI,801178.SWI,801179.SWI,801181.SWI,801183.SWI,801191.SWI,801193.SWI,801194.SWI,801202.SWI,801203.SWI,801204.SWI,801206.SWI,\
        801218.SWI,801219.SWI,801223.SWI,801231.SWI,801711.SWI,801712.SWI,801713.SWI,801721.SWI,801722.SWI,801723.SWI,801724.SWI,801726.SWI,801731.SWI,\
        801733.SWI,801735.SWI,801736.SWI,801737.SWI,801738.SWI,801741.SWI,801742.SWI,801743.SWI,801744.SWI,801745.SWI,801764.SWI,801765.SWI,801766.SWI,\
        801767.SWI,801769.SWI,801782.SWI,801783.SWI,801784.SWI,801785.SWI,801881.SWI,801951.SWI,801952.SWI,801962.SWI,801963.SWI,801971.SWI,801972.SWI,\
        801981.SWI,801982.SWI,801991.SWI,801992.SWI,801993.SWI,801994.SWI,801995.SWI"
gncode = "861001.EI,861003.EI,861004.EI,861005.EI,861007.EI,861008.EI,861009.EI,861010.EI,861013.EI,861014.EI,861017.EI,861019.EI,861020.EI,861022.EI,\
        861024.EI,861025.EI,861028.EI,861029.EI,861030.EI,861032.EI,861033.EI,861034.EI,861035.EI,861038.EI,861039.EI,861040.EI,861043.EI,861045.EI,861046.EI,\
        861047.EI,861048.EI,861049.EI,861050.EI,861051.EI,861053.EI,861054.EI,861057.EI,861058.EI,861059.EI,861060.EI,861061.EI,861062.EI,861068.EI,861072.EI,\
        861074.EI,861075.EI,861076.EI,861077.EI,861079.EI,861080.EI,861082.EI,861083.EI,861085.EI,861089.EI,861090.EI,861091.EI,861093.EI,861094.EI,861096.EI,\
        861098.EI,861099.EI,861100.EI,861102.EI,861104.EI,861105.EI,861108.EI,861109.EI,861110.EI,861111.EI,861112.EI,861113.EI,861114.EI,861116.EI,861117.EI,\
        861118.EI,861119.EI,861120.EI,861122.EI,861124.EI,861125.EI,861131.EI,861133.EI,861136.EI,861137.EI,861138.EI,861139.EI,861140.EI,861142.EI,861143.EI,\
        861145.EI,861146.EI,861147.EI,861148.EI,861149.EI,861150.EI,861152.EI,861153.EI,861154.EI,861155.EI,861159.EI,861160.EI,861161.EI,861162.EI,861164.EI,\
        861165.EI,861166.EI,861167.EI,861168.EI,861169.EI,861170.EI,861172.EI,861173.EI,861174.EI,861175.EI,861176.EI,861177.EI,861178.EI,861179.EI,861180.EI,\
        861181.EI,861182.EI,861183.EI,861184.EI,861186.EI,861187.EI,861188.EI,861190.EI,861191.EI,861192.EI,861193.EI,861195.EI,861196.EI,861197.EI,861198.EI,\
        861199.EI,861200.EI,861201.EI,861202.EI,861203.EI,861204.EI,861205.EI,861206.EI,861207.EI,861209.EI,861210.EI,861211.EI,861212.EI,861213.EI,861214.EI,\
        861215.EI,861216.EI,861217.EI,861218.EI,861219.EI,861220.EI,861221.EI,861222.EI,861223.EI,861224.EI,861225.EI,861226.EI,861227.EI,861228.EI,861230.EI,\
        861231.EI,861232.EI,861233.EI,861234.EI,861236.EI,861237.EI,861238.EI,861239.EI,861240.EI,861241.EI,861243.EI,861244.EI,861245.EI,861246.EI,861247.EI,\
        861248.EI,861249.EI,861251.EI,861253.EI,861254.EI,861255.EI,861256.EI,861257.EI,861258.EI,861259.EI,861260.EI,861263.EI,861264.EI,861265.EI,861266.EI,\
        861268.EI,861269.EI,861270.EI,861271.EI,861272.EI,861275.EI,861276.EI,861278.EI,861280.EI,861281.EI,861282.EI,861283.EI,861284.EI,861285.EI,861286.EI,\
        861287.EI,861288.EI,861289.EI,861290.EI,861291.EI,861292.EI,861293.EI,861294.EI,861295.EI,861296.EI,861297.EI,861298.EI,861299.EI,861300.EI,861301.EI,\
        861302.EI,861303.EI,861304.EI,861305.EI,861306.EI,861307.EI,861308.EI,861309.EI,861310.EI,861311.EI,861312.EI,861313.EI,861314.EI,861315.EI,861316.EI,\
        861317.EI,861318.EI,861319.EI,861320.EI,861321.EI,861322.EI,861323.EI,861324.EI,861325.EI,861326.EI,861328.EI,861329.EI,861330.EI,861331.EI,861332.EI,\
        861333.EI,861334.EI,861335.EI,861336.EI,861337.EI,861338.EI,861339.EI,861340.EI,861341.EI,861342.EI,861343.EI,861344.EI,861345.EI,861346.EI,861347.EI,\
        861348.EI,861349.EI,861350.EI,861351.EI,861352.EI,861353.EI,861354.EI,861355.EI,861356.EI,861357.EI,861358.EI,861359.EI,861360.EI,861361.EI,861362.EI,\
        861363.EI,861364.EI,861365.EI,861366.EI,861367.EI,861368.EI,861369.EI,861370.EI,861371.EI,861372.EI,861373.EI,861374.EI,861375.EI,861376.EI,861377.EI,\
        861378.EI,861379.EI,861380.EI,861381.EI,861382.EI,861383.EI,861384.EI,861385.EI,861386.EI,861387.EI,861388.EI,861389.EI,861390.EI,861391.EI,861392.EI,\
        861393.EI,861394.EI,861395.EI,861396.EI,861397.EI,861398.EI,861399.EI,861400.EI,861401.EI,861402.EI,861403.EI,861404.EI,861405.EI,861406.EI,861407.EI,\
        861408.EI,861409.EI,861410.EI,861411.EI,861412.EI,861413.EI,861414.EI,861415.EI,861416.EI,861417.EI,861418.EI,861419.EI,861420.EI,861421.EI,861422.EI,\
        861423.EI,861424.EI,861425.EI,861426.EI,861427.EI,861428.EI,861429.EI,861430.EI,861431.EI,861432.EI,861433.EI,861434.EI,861435.EI,861436.EI,861437.EI,\
        861438.EI,861439.EI,861440.EI,861441.EI,861442.EI,861443.EI,861444.EI,861445.EI,861446.EI,861447.EI,861448.EI,861449.EI,861450.EI,861451.EI,861452.EI,\
        861453.EI,861454.EI,861455.EI,861456.EI,861457.EI,861458.EI,861459.EI,861460.EI,861461.EI,861462.EI,861463.EI,861464.EI,861465.EI,861466.EI,861467.EI,\
        861468.EI,861469.EI,861470.EI,861471.EI,861472.EI,861473.EI"
replace={'000985.CSI':'中证全指','000300.SH':'沪深300','000905.SH':'中证500','399303.SZ':'国证2000','399373.SZ':'大盘价值',
        '399373.SZ':'大盘价值','399377.SZ':'小盘价值','399372.SZ':'大盘成长','399376.SZ':'小盘成长','CI005917.CI':'金融',
        'CI005918.CI':'周期','CI005919.CI':'消费','CI005920.CI':'成长','CI005921.CI':'稳定'}

# 中证全指走势
# 指数 开盘价 收盘价 最高价 最低价 成交量
df=c.csd("000985.CSI","OPEN,CLOSE,HIGH,LOW,VOLUME",'2000-01-01',""+date+"","period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
df.VOLUME=df.VOLUME/100000000
trace1 = {
    "name":"K线图","type": "candlestick", 
    "x": df['DATES'],"yaxis": "y2", 
    "low": df['LOW'],"high": df['HIGH'],
    "open": df['OPEN'],"close": df['CLOSE'],
    "decreasing": {"line": {"color": "red"}}, 
    "increasing": {"line": {"color": "green"}}}
trace2 = {
    "name": "成交量", "type": "bar", 
    "x": df.DATES,"y": df.VOLUME,"yaxis": "y",
    "marker": {"color":"#6495ED"}}
data = [trace1, trace2]
layout1 = {'title': '中证全指20年走势','title_x':0.5,'title_y':0.9,"yaxis": {"domain": [0, 0.2], "showticklabels": False}, "yaxis2": {"domain": [0.2, 0.8]},
            "legend":{"orientation":"h","yanchor":"bottom","y":0.8,"xanchor":"right","x":1}}
layout = dict(font=dict(family="Times New Roman",size=15,color="RebeccaPurple"),coloraxis_colorbar=dict(xanchor="left",x=0.75,ticks="outside"),
            margin=dict(b= 0,l=10, r=10, t= 10))
layout.update(layout1)
fig1 = go.Figure(data=data, layout=layout)
    
# 指数 开盘价 收盘价 最高价 最低价 成交量
df=c.csd("000985.CSI","OPEN,CLOSE,HIGH,LOW,VOLUME",'2022-01-01',""+date+"","period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1").dropna()
df.VOLUME=df.VOLUME/100000000
trace1 = {
    "name":"K线图","type": "candlestick", 
    "x": df['DATES'],"yaxis": "y2", 
    "low": df['LOW'],"high": df['HIGH'],
    "open": df['OPEN'],"close": df['CLOSE'],
    "decreasing": {"line": {"color": "red"}}, 
    "increasing": {"line": {"color": "green"}}}
trace2 = {
    "name": "成交量", "type": "bar", 
    "x": df.DATES,"y": df.VOLUME,"yaxis": "y",
    "marker": {"color":"#6495ED"}}
data = [trace1, trace2]
layout1 = {'title': '中证全指近期走势','title_x':0.5,'title_y':0.9,"yaxis": {"domain": [0, 0.2], "showticklabels": False}, "yaxis2": {"domain": [0.2, 0.8]},
            "legend":{"orientation":"h","yanchor":"bottom","y":0.8,"xanchor":"right","x":1}}
layout = dict(font=dict(family="Times New Roman",size=15,color="RebeccaPurple"),coloraxis_colorbar=dict(xanchor="left",x=0.75,ticks="outside"),
            margin=dict(b= 0,l=10, r=10, t= 10))
layout.update(layout1)
fig2 = go.Figure(data=data, layout=layout)

# 指数走势
# 走势
df=c.csd(zscode,"CLOSE",'2005-01-01',""+date+"",f"period=3,adjustflag=3,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
df.CODES = df.CODES.replace(replace)
fig3 = px.line(df,x='DATES', y='CLOSE',color=df.CODES)
fig3.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 36),width=975,height=500,title={'text': '指数20年走势','y':0.96,'x':0.45,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=20,font_size=12,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1,xanchor="right",x=1))
fig3.update_yaxes(type='log')

df=c.csd(zscode,"CLOSE",'2020-01-01',""+date+"","period=1,adjustflag=3,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
df.CODES = df.CODES.replace(replace)
fig4 = px.line(df,x='DATES', y='CLOSE',color=df.CODES)
fig4.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 121),width=975,height=500,title={'text': '指数 3年走势','y':0.96,'x':0.45,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=20,font_size=12,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1,xanchor="right",x=1))
fig4.update_yaxes(type='log')

# 指数涨幅表
df1=c.css(zscode,"NAME,DIFFERRANGEN","N=-1,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df5=c.css(zscode,"NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df10=c.css(zscode,"NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df20=c.css(zscode,"NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df60=c.css(zscode,"NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df120=c.css(zscode,"NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df250=c.css(zscode,"NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
# 缺失值赋0
df1=df1.fillna(0)
# 数据合并
dfb=pd.concat([df1,df5,df10,df20,df60,df120,df250],names=None,axis=1,ignore_index=True)
# 数据筛选
# 删除无用列
dfb.drop(dfb.columns[[0,1,4,5,6,8,9,10,12,13,14,16,17,18,20,21,22,24,25,26]],axis = 1,inplace = True)
# 变更列名
dfb.columns=['指数', '当日涨幅', '累计5日涨幅', '累计10日涨幅', '累计20日涨幅', '累计60日涨幅', '累计120日涨幅', '累计250日涨幅']
# 删除特定字符
dfb.指数 = dfb.指数.str.replace(' ','')
dfb.指数 = dfb.指数.str.replace('指数','')
# 设置小数位
dfb.当日涨幅=dfb.当日涨幅.map(lambda x:('%.1f')%x)
dfb.累计5日涨幅=dfb.累计5日涨幅.map(lambda x:('%.0f')%x)
dfb.累计10日涨幅=dfb.累计10日涨幅.map(lambda x:('%.0f')%x)
dfb.累计20日涨幅=dfb.累计20日涨幅.map(lambda x:('%.0f')%x)
dfb.累计60日涨幅=dfb.累计60日涨幅.map(lambda x:('%.0f')%x)
dfb.累计120日涨幅=dfb.累计120日涨幅.map(lambda x:('%.0f')%x)
dfb.累计250日涨幅=dfb.累计250日涨幅.map(lambda x:('%.0f')%x)

fig5 = go.Figure(
data=[go.Table(
    header=dict(values=list(dfb.columns),  # 表头取值是data列属性
                fill_color='paleturquoise',align=['center','center'],font_size=17,
    height=60),  # 填充色和文本位置
            
    cells=dict(values=[dfb.指数,dfb.当日涨幅,dfb.累计5日涨幅,dfb.累计10日涨幅,dfb.累计20日涨幅,dfb.累计60日涨幅,dfb.累计120日涨幅,dfb.累计250日涨幅],  # 单元格的取值就是每个列属性的Series取值
                fill_color='lavender',align=['center','right'],font_size=22,
    height=60)
)]
)
fig5.update_layout(width=975,height=500)

# 指数涨幅
df=c.css(zscode,"NAME,DIFFERRANGEN","N=-1,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
# 缺失值赋0
df=df.fillna(0)
df['NAME'] = df['NAME'].str.replace(' ', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig6 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig6.update_traces(texttemplate='%{text:.1f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig6.update_layout(width=975,height=500,title={'text': '指数当日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

df=c.css(zscode,"NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
df['NAME'] = df['NAME'].str.replace(' ', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig7 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig7.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig7.update_layout(width=975,height=500,title={'text': '指数5日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

df=c.css(zscode,"NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
df['NAME'] = df['NAME'].str.replace(' ', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig8 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig8.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig8.update_layout(width=975,height=500,title={'text': '指数10日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

df=c.css(zscode,"NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
df['NAME'] = df['NAME'].str.replace(' ', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig9 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig9.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig9.update_layout(width=975,height=500,title={'text': '指数20日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

df=c.css(zscode,"NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
df['NAME'] = df['NAME'].str.replace(' ', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig10 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig10.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig10.update_layout(width=975,height=500,title={'text': '指数60日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

df=c.css(zscode,"NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
df['NAME'] = df['NAME'].str.replace(' ', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig11 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig11.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig11.update_layout(width=975,height=500,title={'text': '指数120日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

df=c.css(zscode,"NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
df['NAME'] = df['NAME'].str.replace(' ', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig12 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig12.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig12.update_layout(width=975,height=500,title={'text': '指数250日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
    
# 指数主力净流入
df=c.css(zscode,"NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df['NAME'] = df['NAME'].str.replace(' ', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
df['NETINFLOW']=df['NETINFLOW']/100000000
fig13 = px.bar(df,x='NAME',y='NETINFLOW',text='NETINFLOW')
fig13.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['NETINFLOW'])>0,'red','limegreen'))) 
fig13.update_layout(width=975,height=500,title={'text': f'指数当日主力净流入(亿元）','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

# 主力净流入资金
date0 = c.getdate(""+date+"", -0, "Market=CNSESH").Data[0]
date1 = c.getdate(""+date+"", -1, "Market=CNSESH").Data[0]
date2 = c.getdate(""+date+"", -2, "Market=CNSESH").Data[0]
df0=c.css(zscode,"NAME,NETINFLOW","TradeDate="+date0+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df1=c.css(zscode,"NAME,NETINFLOW","TradeDate="+date1+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df2=c.css(zscode,"NAME,NETINFLOW","TradeDate="+date2+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=pd.concat([df0,df1,df2],names=None,axis=1,ignore_index=True)
# 指定列求和
df['n']=df.iloc[:,[3,7,11]].sum(axis=1)
# 删除无用列
df.drop(df.columns[[0,1,3,4,5,6,7,8,9,10,11]],axis = 1,inplace = True)
# 变更列名
df.columns=['NAME', 'NETINFLOW']
df['NAME'] = df['NAME'].str.replace(' ', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
df['NETINFLOW']=df['NETINFLOW']/100000000
fig14 = px.bar(df,x='NAME',y='NETINFLOW',text='NETINFLOW')
fig14.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['NETINFLOW'])>0,'red','limegreen'))) 
fig14.update_layout(width=975,height=500,title={'text':'指数3日主力净流入(亿元）','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

# 风格走势
df=c.csd(fgcode,"CLOSE",'2005-01-01',""+date+"","period=3,adjustflag=3,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
df.CODES = df.CODES.replace(replace)
fig15 = px.line(df,x='DATES', y='CLOSE',color=df.CODES)
fig15.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 36),width=975,height=500,title={'text': '风格20年走势','y':0.96,'x':0.45,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=20,font_size=12,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1,xanchor="right",x=1))
fig15.update_yaxes(type='log')

df=c.csd(fgcode,"CLOSE",'2020-01-01',""+date+"","period=1,adjustflag=3,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
df.CODES = df.CODES.replace(replace)
fig16 = px.line(df,x='DATES', y='CLOSE',color=df.CODES)
fig16.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 121),width=975,height=500,title={'text': '风格 3年走势','y':0.96,'x':0.45,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=20,font_size=12,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1,xanchor="right",x=1))
fig16.update_yaxes(type='log')

# 风格涨幅表
#风格涨幅表格
df1=c.css(fgcode,"NAME,DIFFERRANGEN","N=-1,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df5=c.css(fgcode,"NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df10=c.css(fgcode,"NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df20=c.css(fgcode,"NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df60=c.css(fgcode,"NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df120=c.css(fgcode,"NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df250=c.css(fgcode,"NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
# 缺失值赋0
df1=df1.fillna(0)
# 数据合并
dfb=pd.concat([df1,df5,df10,df20,df60,df120,df250],names=None,axis=1,ignore_index=True)
# 数据筛选
# 删除无用列
dfb.drop(dfb.columns[[0,1,4,5,6,8,9,10,12,13,14,16,17,18,20,21,22,24,25,26]],axis = 1,inplace = True)
# 变更列名
dfb.columns=['风格指数', '当日涨幅', '累计5日涨幅', '累计10日涨幅', '累计20日涨幅', '累计60日涨幅', '累计120日涨幅', '累计250日涨幅']
# 删除特定字符
dfb.风格指数 = dfb.风格指数.str.replace('巨潮','')
dfb.风格指数 = dfb.风格指数.str.replace('指数','')
# 设置小数位
dfb.当日涨幅=dfb.当日涨幅.map(lambda x:('%.1f')%x)
dfb.累计5日涨幅=dfb.累计5日涨幅.map(lambda x:('%.0f')%x)
dfb.累计10日涨幅=dfb.累计10日涨幅.map(lambda x:('%.0f')%x)
dfb.累计20日涨幅=dfb.累计20日涨幅.map(lambda x:('%.0f')%x)
dfb.累计60日涨幅=dfb.累计60日涨幅.map(lambda x:('%.0f')%x)
dfb.累计120日涨幅=dfb.累计120日涨幅.map(lambda x:('%.0f')%x)
dfb.累计250日涨幅=dfb.累计250日涨幅.map(lambda x:('%.0f')%x)

fig17 = go.Figure(
data=[go.Table(
    header=dict(values=list(dfb.columns),  # 表头取值是data列属性
                fill_color='paleturquoise',align=['center','center'],font_size=17,
    height=60),  # 填充色和文本位置
            
    cells=dict(values=[dfb.风格指数,dfb.当日涨幅,dfb.累计5日涨幅,dfb.累计10日涨幅,dfb.累计20日涨幅,dfb.累计60日涨幅,dfb.累计120日涨幅,dfb.累计250日涨幅],  # 单元格的取值就是每个列属性的Series取值
                fill_color='lavender',align=['center','right'],font_size=22,
    height=60)
)]
)
fig17.update_layout(width=975,height=500)

# 风格涨幅
df=c.css(fgcode,"NAME,DIFFERRANGEN",f"N=-1,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
# 缺失值赋0
df=df.fillna(0)
df['NAME'] = df['NAME'].str.replace('巨潮', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig18 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig18.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig18.update_layout(width=975,height=500,title={'text': '风格当日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

df=c.css(fgcode,"NAME,DIFFERRANGEN",f"N=-5,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
# 缺失值赋0
df=df.fillna(0)
df['NAME'] = df['NAME'].str.replace('巨潮', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig19 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig19.update_traces(texttemplate='%{text:.1f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig19.update_layout(width=975,height=500,title={'text': '风格5日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

df=c.css(fgcode,"NAME,DIFFERRANGEN",f"N=-10,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
# 缺失值赋0
df=df.fillna(0)
df['NAME'] = df['NAME'].str.replace('巨潮', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig20 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig20.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig20.update_layout(width=975,height=500,title={'text': '风格10日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

df=c.css(fgcode,"NAME,DIFFERRANGEN",f"N=-20,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
# 缺失值赋0
df=df.fillna(0)
df['NAME'] = df['NAME'].str.replace('巨潮', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig21 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig21.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig21.update_layout(width=975,height=500,title={'text': '风格20日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

df=c.css(fgcode,"NAME,DIFFERRANGEN",f"N=-60,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
# 缺失值赋0
df=df.fillna(0)
df['NAME'] = df['NAME'].str.replace('巨潮', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig22 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig22.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig22.update_layout(width=975,height=500,title={'text': '风格60日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

df=c.css(fgcode,"NAME,DIFFERRANGEN",f"N=-120,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
# 缺失值赋0
df=df.fillna(0)
df['NAME'] = df['NAME'].str.replace('巨潮', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig23 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig23.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig23.update_layout(width=975,height=500,title={'text': '风格120日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

df=c.css(fgcode,"NAME,DIFFERRANGEN",f"N=-250,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
# 缺失值赋0
df=df.fillna(0)
df['NAME'] = df['NAME'].str.replace('巨潮', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig24 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig24.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig24.update_layout(width=975,height=500,title={'text': '风格250日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
    
# 风格主力净流入
df=c.css(fgcode,"NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df['NAME'] = df['NAME'].str.replace('巨潮', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
df['NETINFLOW']=df['NETINFLOW']/100000000
fig25 = px.bar(df,x='NAME',y='NETINFLOW',text='NETINFLOW')
fig25.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['NETINFLOW'])>0,'red','limegreen'))) 
fig25.update_layout(width=975,height=500,title={'text': '风格当日主力净流入(亿元）','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

# 主力净流入资金
date0 = c.getdate(""+date+"", -0, "Market=CNSESH").Data[0]
date1 = c.getdate(""+date+"", -1, "Market=CNSESH").Data[0]
date2 = c.getdate(""+date+"", -2, "Market=CNSESH").Data[0]
df0=c.css(fgcode,"NAME,NETINFLOW","TradeDate="+date0+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df1=c.css(fgcode,"NAME,NETINFLOW","TradeDate="+date1+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df2=c.css(fgcode,"NAME,NETINFLOW","TradeDate="+date2+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=pd.concat([df0,df1,df2],names=None,axis=1,ignore_index=True)
# 指定列求和
df['n']=df.iloc[:,[3,7,11]].sum(axis=1)
# 删除无用列
df.drop(df.columns[[0,1,3,4,5,6,7,8,9,10,11]],axis = 1,inplace = True)
# 变更列名
df.columns=['NAME', 'NETINFLOW']
df['NAME'] = df['NAME'].str.replace('巨潮', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
df['NETINFLOW']=df['NETINFLOW']/100000000
fig26 = px.bar(df,x='NAME',y='NETINFLOW',text='NETINFLOW')
fig26.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['NETINFLOW'])>0,'red','limegreen'))) 
fig26.update_layout(width=975,height=500,title={'text':'风格3日主力净流入(亿元）','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

# 行业风格走势
df=c.csd(hfcode,"CLOSE",'2005-01-01',""+date+"","period=3,adjustflag=3,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
df.CODES = df.CODES.replace(replace)
fig261 = px.line(df,x='DATES', y='CLOSE',color=df.CODES)
fig261.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 36),width=975,height=500,title={'text':'行业风格20年走势','y':0.96,'x':0.45,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=20,font_size=12,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1,xanchor="right",x=1))
fig261.update_yaxes(type='log')

df=c.csd(hfcode,"CLOSE",'2020-01-01',""+date+"","period=1,adjustflag=3,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
df.CODES = df.CODES.replace(replace)
fig27 = px.line(df,x='DATES', y='CLOSE',color=df.CODES)
fig27.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 121),width=975,height=500,title={'text': '行业风格 3年走势','y':0.96,'x':0.45,'xanchor': 'center',
                'yanchor': 'top'},title_font_size=20,font_size=12,title_font_color='red',xaxis_title=None,yaxis_title=None,
                legend=dict(orientation="h",yanchor="bottom",y=1,xanchor="right",x=1))
fig27.update_yaxes(type='log')

# 行业风格涨幅表
df1=c.css(hfcode,"NAME,DIFFERRANGEN","N=-1,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df5=c.css(hfcode,"NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df10=c.css(hfcode,"NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df20=c.css(hfcode,"NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df60=c.css(hfcode,"NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df120=c.css(hfcode,"NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df250=c.css(hfcode,"NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
# 缺失值赋0
df1=df1.fillna(0)
# 数据合并
dfb=pd.concat([df1,df5,df10,df20,df60,df120,df250],names=None,axis=1,ignore_index=True)
# 数据筛选
# 删除无用列
dfb.drop(dfb.columns[[0,1,4,5,6,8,9,10,12,13,14,16,17,18,20,21,22,24,25,26]],axis = 1,inplace = True)
# 变更列名
dfb.columns=['行业风格指数', '当日涨幅', '累计5日涨幅', '累计10日涨幅', '累计20日涨幅', '累计60日涨幅', '累计120日涨幅', '累计250日涨幅']
# 删除特定字符
dfb.行业风格指数 = dfb.行业风格指数.str.replace('\(风格.中信\)','')
dfb.行业风格指数 = dfb.行业风格指数.str.replace(' ','')
# 设置小数位
dfb.当日涨幅=dfb.当日涨幅.map(lambda x:('%.1f')%x)
dfb.累计5日涨幅=dfb.累计5日涨幅.map(lambda x:('%.0f')%x)
dfb.累计10日涨幅=dfb.累计10日涨幅.map(lambda x:('%.0f')%x)
dfb.累计20日涨幅=dfb.累计20日涨幅.map(lambda x:('%.0f')%x)
dfb.累计60日涨幅=dfb.累计60日涨幅.map(lambda x:('%.0f')%x)
dfb.累计120日涨幅=dfb.累计120日涨幅.map(lambda x:('%.0f')%x)
dfb.累计250日涨幅=dfb.累计250日涨幅.map(lambda x:('%.0f')%x)

fig28 = go.Figure(
data=[go.Table(
    header=dict(values=list(dfb.columns),  # 表头取值是data列属性
                fill_color='paleturquoise',align=['center','center'],font_size=17,
    height=60),  # 填充色和文本位置
            
    cells=dict(values=[dfb.行业风格指数,dfb.当日涨幅,dfb.累计5日涨幅,dfb.累计10日涨幅,dfb.累计20日涨幅,dfb.累计60日涨幅,dfb.累计120日涨幅,dfb.累计250日涨幅],  # 单元格的取值就是每个列属性的Series取值
                fill_color='lavender',align=['center','right'],font_size=22,
    height=60)
)]
)
fig28.update_layout(width=975,height=500)

# 行业风格涨幅
df=c.css(hfcode,"NAME,DIFFERRANGEN","N=-1,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
# 缺失值赋0
df=df.fillna(0)
df['NAME'] = df['NAME'].str.replace('\(风格.中信\)', '')
fig29 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig29.update_traces(texttemplate='%{text:.1f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig29.update_layout(width=975,height=500,title={'text': '行业风格当日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

df=c.css(hfcode,"NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
df['NAME'] = df['NAME'].str.replace('\(风格.中信\)', '')
fig30 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig30.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig30.update_layout(width=975,height=500,title={'text': '行业风格5日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

df=c.css(hfcode,"NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
df['NAME'] = df['NAME'].str.replace('\(风格.中信\)', '')
fig31 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig31.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig31.update_layout(width=975,height=500,title={'text': '行业风格10日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

df=c.css(hfcode,"NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
df['NAME'] = df['NAME'].str.replace('\(风格.中信\)', '')
fig32 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig32.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig32.update_layout(width=975,height=500,title={'text': '行业风格20日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

df=c.css(hfcode,"NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
df['NAME'] = df['NAME'].str.replace('\(风格.中信\)', '')
fig33 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig33.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig33.update_layout(width=975,height=500,title={'text': '行业风格60日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

df=c.css(hfcode,"NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
df['NAME'] = df['NAME'].str.replace('\(风格.中信\)', '')
fig34 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig34.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig34.update_layout(width=975,height=500,title={'text': '行业风格120日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

df=c.css(hfcode,"NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
df['NAME'] = df['NAME'].str.replace('\(风格.中信\)', '')
fig35 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig35.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig35.update_layout(width=975,height=500,title={'text': '行业风格250日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
    
# 行业风格主力净流入
df=c.css(hfcode,"NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df['NAME'] = df['NAME'].str.replace('(风格.中信)', '')
df['NETINFLOW']=df['NETINFLOW']/100000000
fig36 = px.bar(df,x='NAME',y='NETINFLOW',text='NETINFLOW')
fig36.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['NETINFLOW'])>0,'red','limegreen'))) 
fig36.update_layout(width=975,height=500,title={'text': '行业风格当日主力净流入(亿元）','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

# 主力净流入资金
date0 = c.getdate(""+date+"", -0, "Market=CNSESH").Data[0]
date1 = c.getdate(""+date+"", -1, "Market=CNSESH").Data[0]
date2 = c.getdate(""+date+"", -2, "Market=CNSESH").Data[0]
df0=c.css(hfcode,"NAME,NETINFLOW","TradeDate="+date0+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df1=c.css(hfcode,"NAME,NETINFLOW","TradeDate="+date1+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df2=c.css(hfcode,"NAME,NETINFLOW","TradeDate="+date2+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=pd.concat([df0,df1,df2],names=None,axis=1,ignore_index=True)
# 指定列求和
df['n']=df.iloc[:,[3,7,11]].sum(axis=1)
# 删除无用列
df.drop(df.columns[[0,1,3,4,5,6,7,8,9,10,11]],axis = 1,inplace = True)
# 变更列名
df.columns=['NAME', 'NETINFLOW']
df['NAME'] = df['NAME'].str.replace('(风格.中信)', '')
df['NETINFLOW']=df['NETINFLOW']/100000000
fig37 = px.bar(df,x='NAME',y='NETINFLOW',text='NETINFLOW')
fig37.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['NETINFLOW'])>0,'red','limegreen'))) 
fig37.update_layout(width=975,height=500,title={'text': '行业风格3日主力净流入(亿元）','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)

# 行业涨幅 申万一级行业指数
df=c.css(hycode,"NAME,DIFFERRANGEN","N=-1,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
# 缺失值赋0
df=df.fillna(0)
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df1=df.head(16)
df2=df.tail(15)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('申万一级', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig38 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig38.update_traces(texttemplate='%{text:.1f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig38.update_layout(width=975,height=500,title={'text':'一级行业当日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

df=c.css(hycode,"NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df1=df.head(16)
df2=df.tail(15)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('申万一级', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig39 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig39.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig39.update_layout(width=975,height=500,title={'text':'一级行业5日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

df=c.css(hycode,"NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df1=df.head(16)
df2=df.tail(15)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('申万一级', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig40 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig40.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig40.update_layout(width=975,height=500,title={'text':'一级行业10日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

df=c.css(hycode,"NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df1=df.head(16)
df2=df.tail(15)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('申万一级', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig41 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig41.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig41.update_layout(width=975,height=500,title={'text':'一级行业20日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

df=c.css(hycode,"NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df1=df.head(16)
df2=df.tail(15)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('申万一级', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig42 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig42.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig42.update_layout(width=975,height=500,title={'text':'一级行业60日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

df=c.css(hycode,"NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df1=df.head(16)
df2=df.tail(15)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('申万一级', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig43 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig43.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig43.update_layout(width=975,height=500,title={'text':'一级行业120日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

df=c.css(hycode,"NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1") 
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df1=df.head(16)
df2=df.tail(15)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('申万一级', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig44 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig44.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig44.update_layout(width=975,height=500,title={'text':'一级行业250日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)
    
# 行业主力净流入
df=c.css(hycode,"NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=df.sort_values(by="NETINFLOW",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字","融资融券","富时罗素","标准普尔","预盈预增","MSCI中国","深成500",
        "华为概念","中证500","预亏预减"])]
df1=df.head(16)
df2=df.tail(15)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('申万一级', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
df['NETINFLOW']=df['NETINFLOW']/100000000
fig45 = px.bar(df,x='NAME',y='NETINFLOW',text='NETINFLOW')
fig45.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['NETINFLOW'])>0,'red','limegreen'))) 
fig45.update_layout(width=975,height=500,title={'text': '一级行业当日主力净流入(亿元）','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

# 主力净流入资金
date0 = c.getdate(""+date+"", -0, "Market=CNSESH").Data[0]
date1 = c.getdate(""+date+"", -1, "Market=CNSESH").Data[0]
date2 = c.getdate(""+date+"", -2, "Market=CNSESH").Data[0]
df0=c.css(hycode,"NAME,NETINFLOW","TradeDate="+date0+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df1=c.css(hycode,"NAME,NETINFLOW","TradeDate="+date1+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df2=c.css(hycode,"NAME,NETINFLOW","TradeDate="+date2+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=pd.concat([df0,df1,df2],names=None,axis=1,ignore_index=True)
# 指定列求和
df['n']=df.iloc[:,[3,7,11]].sum(axis=1)
# 删除无用列
df.drop(df.columns[[0,1,3,4,5,6,7,8,9,10,11]],axis = 1,inplace = True)
# 变更列名
df.columns=['NAME', 'NETINFLOW']
df=df.sort_values(by="NETINFLOW",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字","融资融券","富时罗素","标准普尔","预盈预增","MSCI中国","深成500",
        "华为概念","中证500","预亏预减","HS300","上证180","证金持股","机构重仓","创业板综","深证100R","基金重仓","深股通","转债标的","AH股","上证50","沪股通"])]
df1=df.head(16)
df2=df.tail(15)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('申万一级', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
df['NETINFLOW']=df['NETINFLOW']/100000000
fig46 = px.bar(df,x='NAME',y='NETINFLOW',text='NETINFLOW')
fig46.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['NETINFLOW'])>0,'red','limegreen'))) 
fig46.update_layout(width=975,height=500,title={'text':'一级行业3日主力净流入(亿元）','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

# 行业涨幅 申万二级行业指数
df=c.css(hy2code,"NAME,DIFFERRANGEN","N=-1,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
# 缺失值赋0
df=df.fillna(0) 
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字"])]
df1=df.head(20)
df2=df.tail(20)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('申万二级', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig47 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig47.update_traces(texttemplate='%{text:.1f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig47.update_layout(width=975,height=500,title={'text':'二级行业当日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

df=c.css(hy2code,"NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字"])]
df1=df.head(20)
df2=df.tail(20)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('申万二级', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig48 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig48.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig48.update_layout(width=975,height=500,title={'text':'二级行业5日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

df=c.css(hy2code,"NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字"])]
df1=df.head(20)
df2=df.tail(20)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('申万二级', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig49 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig49.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig49.update_layout(width=975,height=500,title={'text':'二级行业10日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

df=c.css(hy2code,"NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字"])]
df1=df.head(20)
df2=df.tail(20)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('申万二级', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig50 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig50.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig50.update_layout(width=975,height=500,title={'text':'二级行业20日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

df=c.css(hy2code,"NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字"])]
df1=df.head(20)
df2=df.tail(20)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('申万二级', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig51 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig51.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig51.update_layout(width=975,height=500,title={'text':'二级行业60日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

df=c.css(hy2code,"NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字"])]
df1=df.head(20)
df2=df.tail(20)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('申万二级', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig52 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig52.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig52.update_layout(width=975,height=500,title={'text':'二级行业120日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

df=c.css(hy2code,"NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字"])]
df1=df.head(20)
df2=df.tail(20)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('申万二级', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
fig53 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig53.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig53.update_layout(width=975,height=500,title={'text':'二级行业250日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

# 行业主力净流入
# 板块主力净流入资金 
df=c.css(hy2code,"NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=df.sort_values(by="NETINFLOW",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字","融资融券","富时罗素","标准普尔","预盈预增","MSCI中国","深成500",
        "华为概念","中证500","预亏预减"])]
df1=df.head(20)
df2=df.tail(20)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('申万二级', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
df['NETINFLOW']=df['NETINFLOW']/100000000
fig54 = px.bar(df,x='NAME',y='NETINFLOW',text='NETINFLOW')
fig54.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['NETINFLOW'])>0,'red','limegreen'))) 
fig54.update_layout(width=975,height=500,title={'text':'二级行业当日主力净流入(亿元）','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

# 主力净流入资金
date0 = c.getdate(""+date+"", -0, "Market=CNSESH").Data[0]
date1 = c.getdate(""+date+"", -1, "Market=CNSESH").Data[0]
date2 = c.getdate(""+date+"", -2, "Market=CNSESH").Data[0]
df0=c.css(hy2code,"NAME,NETINFLOW","TradeDate="+date0+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df1=c.css(hy2code,"NAME,NETINFLOW","TradeDate="+date1+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df2=c.css(hy2code,"NAME,NETINFLOW","TradeDate="+date2+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=pd.concat([df0,df1,df2],names=None,axis=1,ignore_index=True)
# 指定列求和
df['n']=df.iloc[:,[3,7,11]].sum(axis=1)
# 删除无用列
df.drop(df.columns[[0,1,3,4,5,6,7,8,9,10,11]],axis = 1,inplace = True)
# 变更列名
df.columns=['NAME', 'NETINFLOW']
df=df.sort_values(by="NETINFLOW",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字","融资融券","富时罗素","标准普尔","预盈预增","MSCI中国","深成500",
        "华为概念","中证500","预亏预减","HS300","上证180","证金持股","机构重仓","创业板综","深证100R","基金重仓","深股通","转债标的","AH股","上证50","沪股通"])]
df1=df.head(20)
df2=df.tail(20)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('申万二级', '')
df['NAME'] = df['NAME'].str.replace('指数', '')
df['NETINFLOW']=df['NETINFLOW']/100000000
fig55 = px.bar(df,x='NAME',y='NETINFLOW',text='NETINFLOW')
fig55.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['NETINFLOW'])>0,'red','limegreen'))) 
fig55.update_layout(width=975,height=500,title={'text': '二级行业3日主力净流入(亿元）','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

# 概念涨幅
df=c.css(gncode,"NAME,DIFFERRANGEN","N=-1,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
# 缺失值赋0
df=df.fillna(0) 
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字"])]
df1=df.head(20)
df2=df.tail(20)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('', '')
df['NAME'] = df['NAME'].str.replace('', '')
fig56 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig56.update_traces(texttemplate='%{text:.1f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig56.update_layout(width=975,height=500,title={'text':'概念当日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

df=c.css(gncode,"NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字"])]
df1=df.head(20)
df2=df.tail(20)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('', '')
df['NAME'] = df['NAME'].str.replace('', '')
fig57 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig57.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig57.update_layout(width=975,height=500,title={'text':'概念5日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

df=c.css(gncode,"NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字"])]
df1=df.head(20)
df2=df.tail(20)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('', '')
df['NAME'] = df['NAME'].str.replace('', '')
fig58 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig58.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig58.update_layout(width=975,height=500,title={'text':'概念10日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

df=c.css(gncode,"NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字"])]
df1=df.head(20)
df2=df.tail(20)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('', '')
df['NAME'] = df['NAME'].str.replace('', '')
fig59 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig59.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig59.update_layout(width=975,height=500,title={'text':'概念20日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

df=c.css(gncode,"NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字"])]
df1=df.head(20)
df2=df.tail(20)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('', '')
df['NAME'] = df['NAME'].str.replace('', '')
fig60 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig60.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig60.update_layout(width=975,height=500,title={'text':'概念60日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

df=c.css(gncode,"NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字"])]
df1=df.head(20)
df2=df.tail(20)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('', '')
df['NAME'] = df['NAME'].str.replace('', '')
fig61 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig61.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig61.update_layout(width=975,height=500,title={'text':'概念120日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

df=c.css(gncode,"NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=df.sort_values(by="DIFFERRANGEN",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字"])]
df1=df.head(20)
df2=df.tail(20)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NAME'] = df['NAME'].str.replace('', '')
df['NAME'] = df['NAME'].str.replace('', '')
fig62 = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
fig62.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
fig62.update_layout(width=975,height=500,title={'text':'概念250日涨幅%','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)
    
# 概念主力净流入
df=c.css(gncode,"NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=df.sort_values(by="NETINFLOW",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字","融资融券","富时罗素","标准普尔","预盈预增","MSCI中国","深成500",
        "华为概念","中证500","预亏预减"])]
df1=df.head(20)
df2=df.tail(20)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NETINFLOW']=df['NETINFLOW']/100000000
fig63 = px.bar(df,x='NAME',y='NETINFLOW',text='NETINFLOW')
fig63.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['NETINFLOW'])>0,'red','limegreen'))) 
fig63.update_layout(width=975,height=500,title={'text': '概念当日主力净流入(亿元）','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

# 主力净流入资金
date0 = c.getdate(""+date+"", -0, "Market=CNSESH").Data[0]
date1 = c.getdate(""+date+"", -1, "Market=CNSESH").Data[0]
date2 = c.getdate(""+date+"", -2, "Market=CNSESH").Data[0]
df0=c.css(gncode,"NAME,NETINFLOW","TradeDate="+date0+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df1=c.css(gncode,"NAME,NETINFLOW","TradeDate="+date1+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df2=c.css(gncode,"NAME,NETINFLOW","TradeDate="+date2+",AdjustFlag=1,Rowindex=none,Ispandas=1")
df=pd.concat([df0,df1,df2],names=None,axis=1,ignore_index=True)
# 指定列求和
df['n']=df.iloc[:,[3,7,11]].sum(axis=1)
# 删除无用列
df.drop(df.columns[[0,1,3,4,5,6,7,8,9,10,11]],axis = 1,inplace = True)
# 变更列名
df.columns=['NAME', 'NETINFLOW']
df=df.sort_values(by="NETINFLOW",ascending=False)
df=df[~df['NAME'].isin(["昨日涨停","昨日连板","昨日触板","昨日连板_含一字","昨日涨停_含一字","融资融券","富时罗素","标准普尔","预盈预增","MSCI中国","深成500",
        "华为概念","中证500","预亏预减","HS300","上证180","证金持股","机构重仓","创业板综","深证100R","基金重仓","深股通","转债标的","AH股","上证50","沪股通"])]
df1=df.head(20)
df2=df.tail(20)
df=pd.concat([df1,df2],names=None,axis=0,ignore_index=True)
df['NETINFLOW']=df['NETINFLOW']/100000000
fig64 = px.bar(df,x='NAME',y='NETINFLOW',text='NETINFLOW')
fig64.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['NETINFLOW'])>0,'red','limegreen'))) 
fig64.update_layout(width=975,height=500,title={'text': '概念3日主力净流入(亿元）','y':0.96,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=20,
                font_size=12,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

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
            id='graph261',
            figure=fig261
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
    html.Div([
        dcc.Graph(
            id='graph29',
            figure=fig29
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph30',
            figure=fig30
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph31',
            figure=fig31
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph32',
            figure=fig32
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph33',
            figure=fig33
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph34',
            figure=fig34
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph35',
            figure=fig35
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph36',
            figure=fig36
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph37',
            figure=fig37
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph38',
            figure=fig38
        ),  
    ], className='row'),
        html.Div([
        dcc.Graph(
            id='graph39',
            figure=fig39
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph40',
            figure=fig40
        ),  
    ], className='row'),
        html.Div([
        dcc.Graph(
            id='graph41',
            figure=fig41
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph42',
            figure=fig42
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph43',
            figure=fig43
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph44',
            figure=fig44
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph45',
            figure=fig45
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph46',
            figure=fig46
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph47',
            figure=fig47
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph48',
            figure=fig48
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph49',
            figure=fig49
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph50',
            figure=fig50
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph51',
            figure=fig51
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph52',
            figure=fig52
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph53',
            figure=fig53
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph54',
            figure=fig54
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph55',
            figure=fig55
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph56',
            figure=fig56
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph57',
            figure=fig57
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph58',
            figure=fig58
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph59',
            figure=fig59
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph60',
            figure=fig60
        ),  
    ], className='row'),
        html.Div([
        dcc.Graph(
            id='graph61',
            figure=fig61
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph62',
            figure=fig62
        ),  
    ], className='row'),
        html.Div([
        dcc.Graph(
            id='graph63',
            figure=fig63
        ),  
    ], className='row'),
    html.Div([
        dcc.Graph(
            id='graph64',
            figure=fig64
        ),  
    ], className='row'),
])

if __name__ == '__main__':
    app.run_server(port=1111)