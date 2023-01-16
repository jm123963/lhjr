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

from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import plotly

from reportlab.pdfbase import pdfmetrics   # 注册字体
from reportlab.pdfbase.ttfonts import TTFont # 字体类
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph, Image  # 报告内容相关类
from reportlab.lib.pagesizes import letter  # 页面的标志尺寸(8.5*inch, 11*inch)
from reportlab.lib.styles import getSampleStyleSheet  # 文本样式
from reportlab.lib import colors  # 颜色模块
from reportlab.graphics.charts.barcharts import VerticalBarChart  # 图表类
from reportlab.graphics.charts.legends import Legend  # 图例类
from reportlab.graphics.shapes import Drawing  # 绘图工具
from reportlab.lib.units import cm  # 单位：cm

# 注册字体(提前准备好字体文件, 如果同一个文件需要多种字体可以注册多个)
pdfmetrics.registerFont(TTFont('SimSun', 'simsun.ttf'))

#调用登录函数（激活后使用，不需要用户名密码）
loginResult = c.start("ForceLogin=1", '')

# 当前时间
date = datetime.today().strftime("%Y-%m-%d")
tradedates=c.tradedates("2021-01-01", ""+date+"")
offday=[-1,-5,-10,-20,-60,-120,-250]
zjday=[-1,-5,-10]

def zs(code,field,days,period,text,image):
    # 走势
    df=c.csd(code,field,days,""+date+"",f"period={period},adjustflag=3,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    fig = px.line(df,x='DATES', y=field, color=df.CODES)
    fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24),width=1200,height=600,title={'text': text,'y':1,'x':0.5,'xanchor': 'center',
                    'yanchor': 'top'},title_font_size=35,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45,
                    legend=dict(orientation="h",yanchor="bottom",y=1,xanchor="right",x=1))
    fig.update_yaxes(type='log')
    fig.write_image(Fr'C:\xyzy\1lhjr\1scrb\{image}.png',scale=3)


def zxzfb():
    #涨幅表格
    df1=c.css(zxcode,"NAME,DIFFERRANGEN","N=-2,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    df5=c.css(zxcode,"NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    df10=c.css(zxcode,"NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    df20=c.css(zxcode,"NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    df60=c.css(zxcode,"NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    df120=c.css(zxcode,"NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    df250=c.css(zxcode,"NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1,Ispandas=1")
    # 数据合并
    dfb=pd.concat([df1,df5,df10,df20,df60,df120,df250],names=None,axis=1,ignore_index=True)
    # 数据筛选
    # 删除无用列
    dfb.drop(dfb.columns[[0,3,4,6,7,9,10,12,13,15,16,18,19]],axis = 1,inplace = True)
    # 变更列名
    dfb.columns=['股票名称', '当日涨幅', '累计5日涨幅', '累计10日涨幅', '累计20日涨幅', '累计60日涨幅', '累计120日涨幅', '累计250日涨幅']
    # 设置小数位
    dfb.当日涨幅=dfb.当日涨幅.map(lambda x:('%.1f')%x)
    dfb.累计5日涨幅=dfb.累计5日涨幅.map(lambda x:('%.0f')%x)
    dfb.累计10日涨幅=dfb.累计10日涨幅.map(lambda x:('%.0f')%x)
    dfb.累计20日涨幅=dfb.累计20日涨幅.map(lambda x:('%.0f')%x)
    dfb.累计60日涨幅=dfb.累计60日涨幅.map(lambda x:('%.0f')%x)
    dfb.累计120日涨幅=dfb.累计120日涨幅.map(lambda x:('%.0f')%x)
    dfb.累计250日涨幅=dfb.累计250日涨幅.map(lambda x:('%.0f')%x)

    fig = go.Figure(
    data=[go.Table(
        header=dict(values=list(dfb.columns),  # 表头取值是data列属性
                    fill_color='paleturquoise',align=['center','center'],font_size=17,
        height=60),  # 填充色和文本位置
                
        cells=dict(values=[dfb.股票名称,dfb.当日涨幅,dfb.累计5日涨幅,dfb.累计10日涨幅,dfb.累计20日涨幅,dfb.累计60日涨幅,dfb.累计120日涨幅,dfb.累计250日涨幅],  # 单元格的取值就是每个列属性的Series取值
                    fill_color='lavender',align=['center','right'],font_size=22,
        height=60)
    )]
    )
    fig.update_layout(width=1200,height=600)
    fig.write_image(r'C:\xyzy\1lhjr\1scrb\zxzfb.png',scale=3)

def zxzf(code,field,n,replace1,replace2,text,image):
    df=c.css(code,field,f"N={n},TradeDate="+date+",AdjustFlag=1,Ispandas=1") 
    df['NAME'] = df['NAME'].str.replace(replace1, '')
    df['NAME'] = df['NAME'].str.replace(replace2, '')
    fig = px.bar(df,x='NAME',y='DIFFERRANGEN',text='DIFFERRANGEN')
    fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['DIFFERRANGEN'])>0,'red','limegreen'))) 
    fig.update_layout(width=1200,height=600,title={'text': text,'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=35,
                    font_size=20,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
    fig.write_image(Fr'C:\xyzy\1lhjr\1scrb\{image}.png',scale=3)

def zj(code,replace1,replace2,text,image):
    # 主力净流入资金 
    df=c.css(code,"NAME,NETINFLOW","TradeDate="+date+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    df['NAME'] = df['NAME'].str.replace(replace1, '')
    df['NAME'] = df['NAME'].str.replace(replace2, '')
    df['NETINFLOW']=df['NETINFLOW']/100000000
    fig = px.bar(df,x='NAME',y='NETINFLOW',text='NETINFLOW')
    fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['NETINFLOW'])>0,'red','limegreen'))) 
    fig.update_layout(width=1200,height=600,title={'text': text,'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=35,
                    font_size=20,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
    fig.write_image(Fr'C:\xyzy\1lhjr\1scrb\{image}.png',scale=3)

def zj3(code,replace1,replace2,text,image):
    # 主力净流入资金
    date0 = c.getdate(""+date+"", -0, "Market=CNSESH").Data[0]
    date1 = c.getdate(""+date+"", -1, "Market=CNSESH").Data[0]
    date2 = c.getdate(""+date+"", -2, "Market=CNSESH").Data[0]
    df0=c.css(code,"NAME,NETINFLOW","TradeDate="+date0+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    df1=c.css(code,"NAME,NETINFLOW","TradeDate="+date1+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    df2=c.css(code,"NAME,NETINFLOW","TradeDate="+date2+",AdjustFlag=1,Rowindex=none,Ispandas=1")
    df=pd.concat([df0,df1,df2],names=None,axis=1,ignore_index=True)
    # 指定列求和
    df['n']=df.iloc[:,[3,7,11]].sum(axis=1)
    # 删除无用列
    df.drop(df.columns[[0,1,3,4,5,6,7,8,9,10,11]],axis = 1,inplace = True)
    # 变更列名
    df.columns=['NAME', 'NETINFLOW']
    df['NAME'] = df['NAME'].str.replace(replace1, '')
    df['NAME'] = df['NAME'].str.replace(replace2, '')
    df['NETINFLOW']=df['NETINFLOW']/100000000
    fig = px.bar(df,x='NAME',y='NETINFLOW',text='NETINFLOW')
    fig.update_traces(texttemplate='%{text:.0f}',textposition='inside',marker=dict(color=np.where(np.array(df['NETINFLOW'])>0,'red','limegreen'))) 
    fig.update_layout(width=1200,height=600,title={'text': text,'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=35,
                    font_size=20,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
    fig.write_image(Fr'C:\xyzy\1lhjr\1scrb\{image}.png',scale=3)

def extreme_percentile(series,min = 0.01,max = 0.99):
  # 百分位法去极值
  series = series.sort_values()
  q = series.quantile([min,max])
  return np.clip(series,q.iloc[0],q.iloc[1])

def gzzs(code,field,days,period,text,image):
    df=c.csd(code,field,days,""+date+"",f"DelType=1,period={period},adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    df['PBMRQ'] = extreme_percentile(df['PBMRQ'])
    df['DATES']=df['DATES'].str[:7]
    df.CODES = df.CODES.str.replace('000776.SZ','广发证券')
    df.CODES = df.CODES.str.replace('002415.SZ','海康威视')
    df.CODES = df.CODES.str.replace('002236.SZ','大华股份')
    df.CODES = df.CODES.str.replace('002815.SZ','崇达技术')
    df.CODES = df.CODES.str.replace('688230.SH','芯导科技')
    df.CODES = df.CODES.str.replace('300418.SZ','昆仑万维')
    df.CODES = df.CODES.str.replace('002191.SZ','劲嘉股份')
    df.CODES = df.CODES.str.replace('002757.SZ','南兴股份')
    fig = px.line(df,x='DATES',y=field,color=df.CODES)
    fig.update_layout(xaxis = dict(tickmode='linear',tick0 =1,dtick = 24,),width=1200,height=600,title={'text':text,'y':0.98,'x':0.15,'xanchor': 'center',
                    'yanchor': 'top'},title_font_size=35,font_size=12,title_font_color='red',xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45,
                    legend=dict(orientation="h",yanchor="bottom",y=1,xanchor="right",x=1))
    fig.update_yaxes(type='log')
    fig.write_image(Fr'C:\xyzy\1lhjr\1scrb\{image}.png',scale=3)

def fwpb(code,days,period,text,image,r):
    df=c.csd(code,"PBMRQ",days,""+date+"",f"DelType=1,period={period},adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    df['PBMRQ'] = extreme_percentile(df['PBMRQ'])
    dc=c.css(code,"NAME,PBMRQN","TradeDate="+date+",Ispandas=1")
    # 变更特定字符
    df.CODES = df.CODES.str.replace('000776.SZ','广发证券')
    df.CODES = df.CODES.str.replace('002415.SZ','海康威视')
    df.CODES = df.CODES.str.replace('002236.SZ','大华股份')
    df.CODES = df.CODES.str.replace('002815.SZ','崇达技术')
    df.CODES = df.CODES.str.replace('688230.SH','芯导科技')
    df.CODES = df.CODES.str.replace('300418.SZ','昆仑万维')
    df.CODES = df.CODES.str.replace('002191.SZ','劲嘉股份')
    df.CODES = df.CODES.str.replace('002757.SZ','南兴股份')
    data=c.css(code,"NAME","Ispandas=1")
    # 保留1位小数
    dc["PBMRQN"] = dc["PBMRQN"].apply(lambda x:format(x,'.1f'))
        
    fig = px.violin(df,x=df.CODES,y=df.PBMRQ,color=df.CODES,box=True,points='all')
    fig.update_layout(width=1200,height=600,title={'text': text,'y':0.98,'x':0.4,'xanchor': 'center','yanchor': 'top'},
                        title_font_size=35,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)
    for i in range(0,r):
        y = dc.PBMRQN[i]
        fig.add_annotation(x=i,y=y,text=f"×{y}",ax=10,ay=0,font={'size': 12})
    fig.write_image(Fr'C:\xyzy\1lhjr\1scrb\{image}.png',scale=3)


def fwpe(code,days,period,text,image,r):
    df=c.csd(code,'PETTM',days,""+date+"",f"DelType=1,period={period},adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    df['PETTM'] = extreme_percentile(df['PETTM'])
    dc=c.css(code,"NAME,PETTM","TradeDate="+date+",Ispandas=1")
    # 变更特定字符
    df.CODES = df.CODES.str.replace('000776.SZ','广发证券')
    df.CODES = df.CODES.str.replace('002415.SZ','海康威视')
    df.CODES = df.CODES.str.replace('002236.SZ','大华股份')
    df.CODES = df.CODES.str.replace('002815.SZ','崇达技术')
    df.CODES = df.CODES.str.replace('688230.SH','芯导科技')
    df.CODES = df.CODES.str.replace('300418.SZ','昆仑万维')
    df.CODES = df.CODES.str.replace('002191.SZ','劲嘉股份')
    df.CODES = df.CODES.str.replace('002757.SZ','南兴股份')
    data=c.css(code,"NAME","Ispandas=1")
    # 保留1位小数
    dc["PETTM"] = dc["PETTM"].apply(lambda x:format(x,'.1f'))
        
    fig = px.violin(df,x=df.CODES,y=df.PETTM,color=df.CODES,box=True,points='all')
    fig.update_layout(width=1200,height=600,title={'text': text,'y':0.98,'x':0.4,'xanchor': 'center','yanchor': 'top'},
                        title_font_size=35,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)
    for i in range(0,r):
        y = dc.PETTM[i]
        fig.add_annotation(x=i,y=y,text=f"×{y}",ax=10,ay=0,font={'size': 12})
    fig.write_image(Fr'C:\xyzy\1lhjr\1scrb\{image}.png',scale=3)

    

def to_pdf():
    class Graphs:
        # 绘制标题
        @staticmethod
        def draw_title(title: str):
            # 获取所有样式表
            style = getSampleStyleSheet()
            # 拿到标题样式
            ct = style['Heading1']
            # 单独设置样式相关属性
            ct.fontName = 'SimSun'      # 字体名
            ct.fontSize = 25            # 字体大小
            ct.leading = 30             # 行间距
            ct.textColor = colors.red     # 字体颜色
            ct.alignment = 1    # 居中
            ct.bold = True
            # 创建标题对应的段落，并且返回
            return Paragraph(title,ct)    

        @staticmethod
        def draw_title1(title: str):
            # 获取所有样式表
            style = getSampleStyleSheet()
            # 拿到标题样式
            ct = style['Normal']
            # 单独设置样式相关属性
            ct.fontName = 'SimSun'  # 字体名
            ct.fontSize = 20  # 字体大小
            ct.leading = 40  # 行间距
            ct.textColor = colors.red  # 字体颜色
            ct.alignment = 1    # 居中
            # 创建标题对应的段落，并且返回
            return Paragraph(title, ct)

        @staticmethod
        def draw_title2(title: str):
            # 获取所有样式表
            style = getSampleStyleSheet()
            # 拿到标题样式
            ct = style['Heading1']
            # 单独设置样式相关属性
            ct.fontName = 'SimSun'      # 字体名
            ct.fontSize = 10            # 字体大小
            ct.leading = 30             # 行间距
            ct.textColor = colors.red     # 字体颜色
            ct.alignment = 2    # 居中
            ct.bold = True
            # 创建标题对应的段落，并且返回
            return Paragraph(title,ct)  

        # 绘制小标题
        @staticmethod
        def draw_little_title(title: str):
            # 获取所有样式表
            style = getSampleStyleSheet()
            # 拿到标题样式
            ct = style['Normal']
            # 单独设置样式相关属性
            ct.fontName = 'SimSun'  # 字体名
            ct.fontSize = 15  # 字体大小
            ct.leading = 20  # 行间距
            ct.textColor = colors.red  # 字体颜色
            # 创建标题对应的段落，并且返回
            return Paragraph(title, ct)       
       
        # 绘制图片
        @staticmethod
        def draw_img(path):
            img = Image(path)       # 读取指定路径下的图片
            img.drawWidth = 22*cm        # 设置图片的宽度
            img.drawHeight = 10*cm       # 设置图片的高度
            return img

    date = (datetime.today() + timedelta(days = -0)).strftime("%Y-%m-%d")

    if __name__ == '__main__':
        # 创建内容对应的空列表
        content = list()

        content.append(Graphs.draw_title('套 利 模 板'))
        content.append(Graphs.draw_title1(date))
        
        content.append(Graphs.draw_little_title('目录'))
        content.append(Graphs.draw_little_title('1.1 股票走势'))
        content.append(Graphs.draw_little_title('1.2 股票涨幅'))
        content.append(Graphs.draw_little_title('1.3 股票资金'))
        
        # content.append(Graphs.draw_little_title('★1.1 股票走势'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxzs20.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxzs3.png'))
        # content.append(Graphs.draw_little_title('★1.2 股票涨幅'))
        # content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxzfb.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxzf1.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxzf5.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxzf10.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxzf20.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxzf60.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxzf120.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxzf250.png'))
        # content.append(Graphs.draw_little_title('★1.3 股票资金'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxzj0.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxzj3.png'))

        # content.append(Graphs.draw_little_title('★2.1 PB'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxpb20.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxpbfw20.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxpb10.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxpbfw10.png'))
        # content.append(Graphs.draw_little_title('★2.2 PE'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxpe20.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxpefw20.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxpe10.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zxpefw10.png'))

        content.append(Graphs.draw_title2('数据来源：Choice  报告工具：Python'))

        # 生成pdf文件
        doc = SimpleDocTemplate(r'C:\xyzy\1lhjr\1scrb\套利模板.pdf', pagesize=letter)
        doc.build(content)

# 自选股
zxcode="002415.SZ,002236.SZ"
# 走势
zs(zxcode,'CLOSE','2005-01-01',3,'自选20年走势','zxzs20')
zs(zxcode,'CLOSE','2020-01-01',1,'自选 3年走势','zxzs3')
# 涨幅表
zxzfb()
# 涨幅
for i in offday:
    zxzf(zxcode,"NAME,DIFFERRANGEN",i,' ',' ',f'自选{-i}日涨幅%',f'zxzf{-i}')
# 主力净流入
zj(zxcode,' ',' ',f'自选当日主力净流入(亿元）',f'zxzj0')
zj3(zxcode,' ',' ',f'自选3日主力净流入(亿元）',f'zxzj3')

# PB
zs(zxcode,'PBMRQ','2000-01-01',3,'PB20年走势','zxpb20')
fwpb(zxcode,"2000-01-01",3,"PB20年分位",'zxpbfw20',8)
zs(zxcode,'PBMRQ','2013-01-01',3,'PB10年走势','zxpb10')
fwpb(zxcode,"2013-01-01",3,"PB10年分位",'zxpbfw10',8)
# PE
zs(zxcode,'PETTM','2000-01-01',3,'PE20年走势','zxpe20')
fwpe(zxcode,"2000-01-01",3,"PE20年分位",'zxpefw20',8)
zs(zxcode,'PETTM','2013-01-01',3,'PE10年走势','zxpe10')
fwpe(zxcode,"2000-01-01",3,"PE10年分位",'zxpefw10',8)

to_pdf()