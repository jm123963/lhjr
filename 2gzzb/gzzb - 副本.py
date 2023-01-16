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
zscode="000985.CSI,000300.SH,000905.SH,000852.SH"
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

def zs(code,field,days,period,text,image):
    df=c.csd(code,field,days,""+date+"",f"DelType=1,period={period},adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
    df['DATES']=df['DATES'].str[:7]
    df.index = df.index.str.replace('000985.CSI','中证全指')
    df.index = df.index.str.replace('000300.SH','沪深300')
    df.index = df.index.str.replace('000905.SH','中证500')
    df.index = df.index.str.replace('399303.SZ','国证2000')
    df.index = df.index.str.replace('399373.SZ','大盘价值')
    df.index = df.index.str.replace('399373.SZ','大盘价值')
    df.index = df.index.str.replace('399377.SZ','小盘价值')
    df.index = df.index.str.replace('399372.SZ','大盘成长')
    df.index = df.index.str.replace('399376.SZ','小盘成长')
    df.index = df.index.str.replace('CI005917.CI','金融')
    df.index = df.index.str.replace('CI005918.CI','周期')
    df.index = df.index.str.replace('CI005919.CI','消费')
    df.index = df.index.str.replace('CI005920.CI','成长')
    df.index = df.index.str.replace('CI005921.CI','稳定')
    fig = px.line(df,x='DATES',y=field,color=df.index)
    fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=1200,height=600,title={'text':text,'y':0.98,'x':0.4,'xanchor': 'center',
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

        content.append(Graphs.draw_title('估值周报'))
        content.append(Graphs.draw_title1(date))
        
        content.append(Graphs.draw_little_title('目录'))
        content.append(Graphs.draw_little_title('1.1 指数PB'))
        content.append(Graphs.draw_little_title('1.2 指数PE'))
        content.append(Graphs.draw_little_title('2.1 风格PB'))
        content.append(Graphs.draw_little_title('2.2 风格PE'))
        content.append(Graphs.draw_little_title('3.1 行业风格PB'))
        content.append(Graphs.draw_little_title('3.2 行业风格PE'))
        content.append(Graphs.draw_little_title('4.1 行业PB'))
        content.append(Graphs.draw_little_title('4.2 行业PE'))
        
        # content.append(Graphs.draw_little_title('★1.1 指数PB'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zspbzs20.png'))
        #content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zspbfw20.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zspbzs10.png'))
        #content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zspbfw10.png'))
        # content.append(Graphs.draw_little_title('★1.2 指数PE'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zspezs20.png'))
        #content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zspefw20.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zspezs10.png'))
        #content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zspefw10.png'))

        content.append(Graphs.draw_title2('数据来源：Choice  报告工具：Python'))

        # 生成pdf文件
        doc = SimpleDocTemplate(r'C:\xyzy\1lhjr\1scrb\ribao.pdf', pagesize=letter)
        doc.build(content)

# 指数PB走势
zs('000985.CSI','PBMRQ','2005-01-01',3,'中证全指PB20年走势','zspb20')
zs('000985.CSI','PBMRQ','2013-01-01',3,'中证全指PB10年走势','zspb10')
# 指数PE走势
zs('000985.CSI','PETTM','2005-01-01',3,'中证全指PE20年走势','zspe20')
zs('000985.CSI','PETTM','2013-01-01',3,'中证全指PE10年走势','zspe10')

# 风格PB走势
zs(fgcode,'PBMRQ','2010-01-01',3,'风格PB13年走势','fgpb10')
# 风格PE走势
zs(fgcode,'PETTM','2010-01-01',3,'风格PE13年走势','fgpe10')

# 行业风格PB走势
zs(hfcode,'PBMRQ','2010-01-01',3,'行业风格PB13年走势','fgpb10')
# 风格PE走势
zs(hfcode,'PETTM','2010-01-01',3,'行业风格PE13年走势','fgpe10')

# 行业市净率PBMRQ
hypb("PBMRQ","2005-01-01",3,"行业20年PB分位",'hypb20')
hypb("PBMRQ","2013-01-01",3,"行业10年PB分位",'hypb10')

# 行业市盈率PETTM
hype("PETTM","2005-01-01",3,"行业10年PE分位",'hype10')
hype("PETTM","2013-01-01",3,"行业 3年PE分位",'hype3')

to_pdf