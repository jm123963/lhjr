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
offday=[-2,-5,-10,-20,-60,-120,-250]
fgzfcode="399373.SZ,399372.SZ,399377.SZ,399376.SZ"
fgcode="399373.SZ,399372.SZ,399377.SZ,399376.SZ"
hycode="801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,\
        801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,\
        801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI"

def pb(code,field,days,period,text,image):
    # PB
    df=c.csd(code,field,days,""+date+"",f"DelType=1,period={period},adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    fig = px.line(df,x='DATES',y=field,color=df.index)
    fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=1200,height=600,title={'text':text,'y':0.98,'x':0.5,'xanchor': 'center',
                    'yanchor': 'top'},title_font_size=35,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45,
                    legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
    fig.update_yaxes(type='log')
    fig.write_image(Fr'C:\xyzy\2gzzb\1scrb\{image}.png',scale=3)

def db(code,field,days,period,text,image):
    # 对比走势
    df=c.csd(code,field,days,""+date+"",f"DelType=1,period={period},adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    fig = px.line(df,x='DATES',y='PBMRQ',color=df.index)
    fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=1200,height=600,title={'text': text,'y':0.98,'x':0.5,'xanchor': 'center',
                    'yanchor': 'top'},title_font_size=35,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45,
                    legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
    fig.update_yaxes(type='log')
    fig.write_image(Fr'C:\xyzy\2gzzb\1scrb\{image}.png',scale=3)

def hypb(field,days,period,text,image):
    # 行业field 
    hygz=c.csd(hycode,field,days,""+date+"",f"DelType=1,period={period},adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    hygzclose=c.css(hycode,f"SHORTNAME,{field}","TradeDate="+date+",DelType=1,Ispandas=1")
    # 变更特定字符
    hygz.index = hygz.index.str.replace('801010.SWI', '农林牧渔')
    hygz.index = hygz.index.str.replace('801030.SWI', '基础化工')
    hygz.index = hygz.index.str.replace('801040.SWI', '钢铁')
    hygz.index = hygz.index.str.replace('801050.SWI', '有色金属')
    hygz.index = hygz.index.str.replace('801080.SWI', '电子')
    hygz.index = hygz.index.str.replace('801110.SWI', '家用电器')
    hygz.index = hygz.index.str.replace('801120.SWI', '食品饮料')
    hygz.index = hygz.index.str.replace('801130.SWI', '纺织服饰')
    hygz.index = hygz.index.str.replace('801140.SWI', '轻工制造')
    hygz.index = hygz.index.str.replace('801150.SWI', '医药生物')
    hygz.index = hygz.index.str.replace('801160.SWI', '公用事业')
    hygz.index = hygz.index.str.replace('801170.SWI', '交通运输')
    hygz.index = hygz.index.str.replace('801180.SWI', '房地产')
    hygz.index = hygz.index.str.replace('801200.SWI', '商贸零售')
    hygz.index = hygz.index.str.replace('801210.SWI', '社会服务')
    hygz.index = hygz.index.str.replace('801230.SWI', '综合')
    hygz.index = hygz.index.str.replace('801710.SWI', '建筑材料')
    hygz.index = hygz.index.str.replace('801720.SWI', '建筑装饰')
    hygz.index = hygz.index.str.replace('801730.SWI', '电力设备')
    hygz.index = hygz.index.str.replace('801740.SWI', '国防军工')
    hygz.index = hygz.index.str.replace('801750.SWI', '计算机')
    hygz.index = hygz.index.str.replace('801760.SWI', '传媒')
    hygz.index = hygz.index.str.replace('801770.SWI', '通信')
    hygz.index = hygz.index.str.replace('801780.SWI', '银行')
    hygz.index = hygz.index.str.replace('801790.SWI', '非银金融')
    hygz.index = hygz.index.str.replace('801880.SWI', '汽车')
    hygz.index = hygz.index.str.replace('801890.SWI', '机械设备')
    hygz.index = hygz.index.str.replace('801950.SWI', '煤炭')
    hygz.index = hygz.index.str.replace('801960.SWI', '石油石化')
    hygz.index = hygz.index.str.replace('801970.SWI', '环保')
    hygz.index = hygz.index.str.replace('801980.SWI', '美容护理')
    # 保留1位小数
    hygzclose[field] = hygzclose[field].apply(lambda x:format(x,'.1f'))
    y0 = hygzclose.PBMRQ[0]
    y1 = hygzclose.PBMRQ[1]
    y2 = hygzclose.PBMRQ[2]
    y3 = hygzclose.PBMRQ[3]
    y4 = hygzclose.PBMRQ[4]
    y5 = hygzclose.PBMRQ[5]
    y6 = hygzclose.PBMRQ[6]
    y7 = hygzclose.PBMRQ[7]
    y8 = hygzclose.PBMRQ[8]
    y9 = hygzclose.PBMRQ[9]
    y10 = hygzclose.PBMRQ[10]
    y11 = hygzclose.PBMRQ[11]
    y12 = hygzclose.PBMRQ[12]
    y13 = hygzclose.PBMRQ[13]
    y14 = hygzclose.PBMRQ[14]
    y15 = hygzclose.PBMRQ[15]
    y16 = hygzclose.PBMRQ[16]
    y17 = hygzclose.PBMRQ[17]
    y18 = hygzclose.PBMRQ[18]
    y19 = hygzclose.PBMRQ[19]
    y20 = hygzclose.PBMRQ[20]
    y21 = hygzclose.PBMRQ[21]
    y22 = hygzclose.PBMRQ[22]
    y23 = hygzclose.PBMRQ[23]
    y24 = hygzclose.PBMRQ[24]
    y25 = hygzclose.PBMRQ[25]
    y26 = hygzclose.PBMRQ[26]
    y27 = hygzclose.PBMRQ[27]
    y28 = hygzclose.PBMRQ[28]
    y29 = hygzclose.PBMRQ[29]
    y30 = hygzclose.PBMRQ[30]

    fig = px.violin(hygz,x=hygz.index,y="PBMRQ",color=hygz.index,box=True)
    fig.update_layout(width=1200,height=600,title={'text': text,'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                        title_font_size=35,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

    fig.add_annotation(x=0,y=y0,text="×{}".format(y0),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=1,y=y1,text="×{}".format(y1),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=2,y=y2,text="×{}".format(y2),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=3,y=y3,text="×{}".format(y3),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=4,y=y4,text="×{}".format(y4),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=5,y=y5,text="×{}".format(y5),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=6,y=y6,text="×{}".format(y6),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=7,y=y7,text="×{}".format(y7),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=8,y=y8,text="×{}".format(y8),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=9,y=y9,text="×{}".format(y9),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=10,y=y10,text="×{}".format(y10),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=11,y=y11,text="×{}".format(y11),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=12,y=y12,text="×{}".format(y12),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=13,y=y13,text="×{}".format(y13),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=14,y=y14,text="×{}".format(y14),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=15,y=y15,text="×{}".format(y15),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=16,y=y16,text="×{}".format(y16),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=17,y=y17,text="×{}".format(y17),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=18,y=y18,text="×{}".format(y18),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=19,y=y19,text="×{}".format(y19),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=20,y=y20,text="×{}".format(y20),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=21,y=y21,text="×{}".format(y21),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=22,y=y22,text="×{}".format(y22),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=23,y=y23,text="×{}".format(y23),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=24,y=y24,text="×{}".format(y24),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=25,y=y25,text="×{}".format(y25),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=26,y=y26,text="×{}".format(y26),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=27,y=y27,text="×{}".format(y27),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=28,y=y28,text="×{}".format(y28),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=29,y=y29,text="×{}".format(y29),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=30,y=y30,text="×{}".format(y30),ax=10,ay=0,font={'size': 12})
    fig.write_image(Fr'C:\xyzy\2gzzb\1scrb\{image}.png',scale=3)

def hype(field,days,period,text,image):
    # 行业field 
    hygz=c.csd(hycode,field,days,""+date+"",f"DelType=1,period={period},adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    hygzclose=c.css(hycode,f"SHORTNAME,{field}","TradeDate="+date+",DelType=1,Ispandas=1")
    # 变更特定字符
    hygz.index = hygz.index.str.replace('801010.SWI', '农林牧渔')
    hygz.index = hygz.index.str.replace('801030.SWI', '基础化工')
    hygz.index = hygz.index.str.replace('801040.SWI', '钢铁')
    hygz.index = hygz.index.str.replace('801050.SWI', '有色金属')
    hygz.index = hygz.index.str.replace('801080.SWI', '电子')
    hygz.index = hygz.index.str.replace('801110.SWI', '家用电器')
    hygz.index = hygz.index.str.replace('801120.SWI', '食品饮料')
    hygz.index = hygz.index.str.replace('801130.SWI', '纺织服饰')
    hygz.index = hygz.index.str.replace('801140.SWI', '轻工制造')
    hygz.index = hygz.index.str.replace('801150.SWI', '医药生物')
    hygz.index = hygz.index.str.replace('801160.SWI', '公用事业')
    hygz.index = hygz.index.str.replace('801170.SWI', '交通运输')
    hygz.index = hygz.index.str.replace('801180.SWI', '房地产')
    hygz.index = hygz.index.str.replace('801200.SWI', '商贸零售')
    hygz.index = hygz.index.str.replace('801210.SWI', '社会服务')
    hygz.index = hygz.index.str.replace('801230.SWI', '综合')
    hygz.index = hygz.index.str.replace('801710.SWI', '建筑材料')
    hygz.index = hygz.index.str.replace('801720.SWI', '建筑装饰')
    hygz.index = hygz.index.str.replace('801730.SWI', '电力设备')
    hygz.index = hygz.index.str.replace('801740.SWI', '国防军工')
    hygz.index = hygz.index.str.replace('801750.SWI', '计算机')
    hygz.index = hygz.index.str.replace('801760.SWI', '传媒')
    hygz.index = hygz.index.str.replace('801770.SWI', '通信')
    hygz.index = hygz.index.str.replace('801780.SWI', '银行')
    hygz.index = hygz.index.str.replace('801790.SWI', '非银金融')
    hygz.index = hygz.index.str.replace('801880.SWI', '汽车')
    hygz.index = hygz.index.str.replace('801890.SWI', '机械设备')
    hygz.index = hygz.index.str.replace('801950.SWI', '煤炭')
    hygz.index = hygz.index.str.replace('801960.SWI', '石油石化')
    hygz.index = hygz.index.str.replace('801970.SWI', '环保')
    hygz.index = hygz.index.str.replace('801980.SWI', '美容护理')
    # 保留1位小数
    hygzclose[field] = hygzclose[field].apply(lambda x:format(x,'.0f'))
    y0 =hygzclose.PETTM[0]
    y1 =hygzclose.PETTM[1]
    y2 =hygzclose.PETTM[2]
    y3 =hygzclose.PETTM[3]
    y4 =hygzclose.PETTM[4]
    y5 =hygzclose.PETTM[5]
    y6 =hygzclose.PETTM[6]
    y7 =hygzclose.PETTM[7]
    y8 =hygzclose.PETTM[8]
    y9 =hygzclose.PETTM[9]
    y10 =hygzclose.PETTM[10]
    y11 =hygzclose.PETTM[11]
    y12 =hygzclose.PETTM[12]
    y13 =hygzclose.PETTM[13]
    y14 =hygzclose.PETTM[14]
    y15 =hygzclose.PETTM[15]
    y16 =hygzclose.PETTM[16]
    y17 =hygzclose.PETTM[17]
    y18 =hygzclose.PETTM[18]
    y19 =hygzclose.PETTM[19]
    y20 =hygzclose.PETTM[20]
    y21 =hygzclose.PETTM[21]
    y22 =hygzclose.PETTM[22]
    y23 =hygzclose.PETTM[23]
    y24 =hygzclose.PETTM[24]
    y25 =hygzclose.PETTM[25]
    y26 =hygzclose.PETTM[26]
    y27 =hygzclose.PETTM[27]
    y28 =hygzclose.PETTM[28]
    y29 =hygzclose.PETTM[29]
    y30 =hygzclose.PETTM[30]

    fig = px.violin(hygz,x=hygz.index,y="PETTM",color=hygz.index,box=True)
    fig.update_layout(width=1200,height=600,title={'text': text,'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=35,font_size=18,
                    title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)

    fig.add_annotation(x=0,y=y0,text="×{}".format(y0),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=1,y=y1,text="×{}".format(y1),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=2,y=y2,text="×{}".format(y2),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=3,y=y3,text="×{}".format(y3),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=4,y=y4,text="×{}".format(y4),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=5,y=y5,text="×{}".format(y5),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=6,y=y6,text="×{}".format(y6),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=7,y=y7,text="×{}".format(y7),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=8,y=y8,text="×{}".format(y8),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=9,y=y9,text="×{}".format(y9),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=10,y=y10,text="×{}".format(y10),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=11,y=y11,text="×{}".format(y11),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=12,y=y12,text="×{}".format(y12),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=13,y=y13,text="×{}".format(y13),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=14,y=y14,text="×{}".format(y14),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=15,y=y15,text="×{}".format(y15),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=16,y=y16,text="×{}".format(y16),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=17,y=y17,text="×{}".format(y17),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=18,y=y18,text="×{}".format(y18),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=19,y=y19,text="×{}".format(y19),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=20,y=y20,text="×{}".format(y20),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=21,y=y21,text="×{}".format(y21),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=22,y=y22,text="×{}".format(y22),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=23,y=y23,text="×{}".format(y23),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=24,y=y24,text="×{}".format(y24),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=25,y=y25,text="×{}".format(y25),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=26,y=y26,text="×{}".format(y26),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=27,y=y27,text="×{}".format(y27),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=28,y=y28,text="×{}".format(y28),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=29,y=y29,text="×{}".format(y29),ax=10,ay=0,font={'size': 12})
    fig.add_annotation(x=30,y=y30,text="×{}".format(y30),ax=10,ay=0,font={'size': 12})
    fig.write_image(Fr'C:\xyzy\2gzzb\1scrb\{image}.png',scale=3)

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
            ct = style['Heading1']
            # 单独设置样式相关属性
            ct.fontName = 'SimSun'      # 字体名
            ct.fontSize = 20            # 字体大小
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
            ct.fontSize = 20  # 字体大小
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

        content.append(Graphs.draw_title('金融市场日报'))
        content.append(Graphs.draw_title1(date))
        
        content.append(Graphs.draw_little_title('目录'))
        content.append(Graphs.draw_little_title('1.1 指数走势'))
        content.append(Graphs.draw_little_title('1.2 指数资金'))
        content.append(Graphs.draw_little_title('1.3 指数估值'))
        content.append(Graphs.draw_little_title('2.1 风格走势'))
        content.append(Graphs.draw_little_title('2.2 风格涨幅'))
        content.append(Graphs.draw_little_title('2.3 风格资金'))
        content.append(Graphs.draw_little_title('2.4 风格估值'))
        content.append(Graphs.draw_little_title('3.1 行业涨幅'))
        content.append(Graphs.draw_little_title('3.2 行业资金'))
        content.append(Graphs.draw_little_title('3.3 行业估值'))
        
        content.append(Graphs.draw_little_title('★1.1 指数走势'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\zszs20.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\zszs.png'))

        content.append(Graphs.draw_little_title('★1.2 指数资金'))
        #content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\zszj.png'))

        content.append(Graphs.draw_little_title('★1.3 指数估值'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\zspb10.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\zspb3.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\zspe10.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\zspe3.png'))

        content.append(Graphs.draw_little_title('★2.1 风格走势'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\fgzs20.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\fgzs3.png'))
        
        content.append(Graphs.draw_little_title('★2.2 风格涨幅'))
        #content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\fgzfb.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\fgzf1.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\fgzf1.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\fgzf5.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\fgzf10.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\fgzf20.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\fgzf60.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\fgzf120.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\fgzf250.png'))
        
        content.append(Graphs.draw_little_title('★2.3 风格资金'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\fgzj1.png'))

        content.append(Graphs.draw_little_title('★2.4 风格估值'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\fgpb10.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\fgpb3.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\fgpe10.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\fgpe3.png'))

        content.append(Graphs.draw_little_title('★3.1 行业涨幅'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\hyzf1.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\hyzf5.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\hyzf10.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\hyzf20.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\hyzf60.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\hyzf120.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\hyzf250.png'))

        content.append(Graphs.draw_little_title('★3.2 行业资金'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\hyzj1.png'))

        content.append(Graphs.draw_little_title('★3.3 行业估值'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\hypb10.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\hypb3.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\hype10.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\2gzzb\1scrb\hype3.png'))

        content.append(Graphs.draw_title('数据来源：Choice  报告工具：Python'))

        # 生成pdf文件
        doc = SimpleDocTemplate(r'C:\xyzy\2gzzb\1scrb\ribao.pdf', pagesize=letter)
        doc.build(content)

    # 指数PB走势
pb('000985.CSI','PBMRQ','2013-01-01',3,'指数PB10年走势','zspb10')
pb('000985.CSI','PBMRQ','2020-01-01',2,'指数PB 3年走势','zspb3')

# 指数PE走势
pb('000985.CSI','PETTM','2013-01-01',3,'指数PE10年走势','zspe10')
pb('000985.CSI','PETTM','2020-01-01',2,'指数PE 3年走势','zspe3')

# 风格PB走势
pb(fgcode,'PBMRQ','2013-01-01',3,'风格PB10年走势','fgpb10')
pb(fgcode,'PBMRQ','2020-01-01',2,'风格PB 3年走势','fgpb3')

# 风格PE走势
pb(fgcode,'PETTM','2013-01-01',3,'风格PE10年走势','fgpe10')
pb(fgcode,'PETTM','2020-01-01',2,'风格PE 3年走势','fgpe3')

# 行业市净率PBMRQ
hypb("PBMRQ","2013-01-01",3,"行业10年PB分位",'hypb10')
hypb("PBMRQ","2020-01-01",2,"行业 3年PB分位",'hypb3')

# 行业市盈率PETTM
hype("PETTM","2013-01-01",3,"行业10年PE分位",'hype10')
hype("PETTM","2020-01-01",2,"行业 3年PE分位",'hype3')

to_pdf