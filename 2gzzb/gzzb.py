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
zscode="000985.CSI,000300.SH,000905.SH,399303.SZ"
fgcode="399373.SZ,399377.SZ,399372.SZ,399376.SZ"
hfcode="CI005917.CI,CI005918.CI,CI005919.CI,CI005920.CI,CI005921.CI"
hycode="801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,\
        801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,\
        801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI"

def zs(code,field,days,period,text,image):
    df=c.csd(code,field,days,""+date+"",f"DelType=1,period={period},adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    df['DATES']=df['DATES'].str[:7]
    df.CODES = df.CODES.str.replace('000985.CSI','中证全指')
    df.CODES = df.CODES.str.replace('000300.SH','沪深300')
    df.CODES = df.CODES.str.replace('000905.SH','中证500')
    df.CODES = df.CODES.str.replace('399303.SZ','国证2000')
    df.CODES = df.CODES.str.replace('399373.SZ','大盘价值')
    df.CODES = df.CODES.str.replace('399373.SZ','大盘价值')
    df.CODES = df.CODES.str.replace('399377.SZ','小盘价值')
    df.CODES = df.CODES.str.replace('399372.SZ','大盘成长')
    df.CODES = df.CODES.str.replace('399376.SZ','小盘成长')
    df.CODES = df.CODES.str.replace('CI005917.CI','金融')
    df.CODES = df.CODES.str.replace('CI005918.CI','周期')
    df.CODES = df.CODES.str.replace('CI005919.CI','消费')
    df.CODES = df.CODES.str.replace('CI005920.CI','成长')
    df.CODES = df.CODES.str.replace('CI005921.CI','稳定')
    fig = px.line(df,x='DATES',y=field,color=df.CODES)
    fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=1200,height=600,title={'text':text,'y':0.98,'x':0.4,'xanchor': 'center',
                    'yanchor': 'top'},title_font_size=35,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45,
                    legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
    fig.update_yaxes(type='log')
    fig.write_image(Fr'C:\xyzy\1lhjr\2gzzb\{image}.png',scale=3)

def fwpb(code,field,days,period,text,image,r):
    df=c.csd(code,field,days,""+date+"",f"DelType=1,period={period},adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    dc=c.css(code,f"SHORTNAME,{field}","TradeDate="+date+",DelType=1,Rowindex=none,Ispandas=1")
    data=c.css(code,"SHORTNAME","Ispandas=1")
    # 变更特定字符
    for a,b in zip(data.index,data.SHORTNAME):
        df.CODES = df.CODES.str.replace(a,b)
    df.CODES = df.CODES.str.replace("\(申万\)","")
    df.CODES = df.CODES.str.replace("\(风格.中信\)","")
    # 保留1位小数
    dc[field] = dc[field].apply(lambda x:format(x,'.1f'))
    
    fig = px.violin(df,x=df.CODES,y=field,color=df.CODES,box=True,points='all')
    fig.update_layout(width=1200,height=600,title={'text': text,'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                        title_font_size=35,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)
    for i in range(0,r):
        y = dc.PBMRQ[i]
        fig.add_annotation(x=i,y=y,text=f"×{y}",ax=10,ay=0,font={'size': 12})
    fig.write_image(Fr'C:\xyzy\1lhjr\2gzzb\{image}.png',scale=3)


def fwpe(code,field,days,period,text,image,r):
    df=c.csd(code,field,days,""+date+"",f"DelType=1,period={period},adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    df['PETTM'] = extreme_percentile(df['PETTM'])
    dc=c.css(code,f"SHORTNAME,{field}","TradeDate="+date+",DelType=1,Rowindex=none,Ispandas=1")
    data=c.css(code,"SHORTNAME","Ispandas=1")
    # 变更特定字符
    for a,b in zip(data.index,data.SHORTNAME):
        df.CODES = df.CODES.str.replace(a,b) 
    df.CODES = df.CODES.str.replace("\(申万\)","")
    df.CODES = df.CODES.str.replace("\(风格.中信\)","")
    # 保留1位小数
    dc[field] = dc[field].apply(lambda x:format(x,'.1f'))
    
    fig = px.violin(df,x=df.CODES,y=field,color=df.CODES,box=True,points='all')
    fig.update_layout(width=1200,height=600,title={'text': text,'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                        title_font_size=35,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)
    for i in range(0,r):
        y = dc.PETTM[i]
        fig.add_annotation(x=i,y=y,text=f"×{y}",ax=10,ay=0,font={'size': 12})
    fig.write_image(Fr'C:\xyzy\1lhjr\2gzzb\{image}.png',scale=3)

def hyfwpb(code,field,days,period,text,image,r):
    dc=c.css(code,f"SHORTNAME,{field}","TradeDate="+date+",DelType=1,Rowindex=none,Ispandas=1")
    dc=dc.sort_values(by="PBMRQ",ascending=True)
    dc=dc.reset_index(drop=True)
    newcode=dc.iloc[:,0].to_list()
    df=c.csd(newcode,field,days,""+date+"",f"DelType=1,period={period},adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    data=c.css(newcode,"SHORTNAME","Ispandas=1")
    # 变更特定字符
    for a,b in zip(data.index,data.SHORTNAME):
        df.CODES = df.CODES.str.replace(a,b)
    df.CODES = df.CODES.str.replace("\(申万\)","")
    df.CODES = df.CODES.str.replace("\(风格.中信\)","")
    # 保留1位小数
    dc[field] = dc[field].apply(lambda x:format(x,'.1f'))
    
    fig = px.violin(df,x=df.CODES,y=field,color=df.CODES,box=True)
    fig.update_layout(width=1200,height=600,title={'text': text,'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                        title_font_size=35,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)
    for i in range(0,r):
        y = dc.PBMRQ[i]
        fig.add_annotation(x=i,y=y,text=f"×{y}",ax=10,ay=0,font={'size': 12})
    fig.write_image(Fr'C:\xyzy\1lhjr\2gzzb\{image}.png',scale=3)

def extreme_percentile(series,min = 0.01,max = 0.99):
  # 百分位法去极值
  series = series.sort_values()
  q = series.quantile([min,max])
  return np.clip(series,q.iloc[0],q.iloc[1])

def hyfwpe(code,field,days,period,text,image,r):
    dc=c.css(code,f"SHORTNAME,{field}","TradeDate="+date+",DelType=1,Rowindex=none,Ispandas=1")
    dc=dc.sort_values(by="PETTM",ascending=True)
    dc=dc.reset_index(drop=True)
    # 负值置尾
    dc=dc.reindex([5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,4,3,2,1,0])
    dc=dc.reset_index(drop=True)
    newcode=dc.iloc[:,0].to_list()
    df=c.csd(newcode,field,days,""+date+"",f"DelType=1,period={period},adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
    df['PETTM'] = extreme_percentile(df['PETTM'])
    data=c.css(newcode,"SHORTNAME","Ispandas=1")
    # 变更特定字符
    for a,b in zip(data.index,data.SHORTNAME):
        df.CODES = df.CODES.str.replace(a,b)
    df.CODES = df.CODES.str.replace("\(申万\)","")
    df.CODES = df.CODES.str.replace("\(风格.中信\)","")
    # 保留1位小数
    dc[field] = dc[field].apply(lambda x:format(x,'.1f'))
    
    fig = px.violin(df,x=df.CODES,y=field,color=df.CODES,box=True)
    fig.update_layout(width=1200,height=600,title={'text': text,'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                        title_font_size=35,font_size=18,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None,xaxis_tickangle=-45)
    for i in range(0,r):
        y = dc.PETTM[i]
        fig.add_annotation(x=i,y=y,text=f"×{y}",ax=10,ay=0,font={'size': 12})
    fig.write_image(Fr'C:\xyzy\1lhjr\2gzzb\{image}.png',scale=3)

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
            ct.fontSize = 15  # 字体大小
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

        content.append(Graphs.draw_title('估  值  周  报'))
        content.append(Graphs.draw_title1(date))
        
        content.append(Graphs.draw_little_title('目录'))
        content.append(Graphs.draw_little_title('1.1 中证全指PB'))
        content.append(Graphs.draw_little_title('1.2 中证全指PE'))
        content.append(Graphs.draw_little_title('2.1 指数PB'))
        content.append(Graphs.draw_little_title('2.2 指数PE'))
        content.append(Graphs.draw_little_title('3.1 风格PB'))
        content.append(Graphs.draw_little_title('3.2 风格PE'))
        content.append(Graphs.draw_little_title('4.1 行业风格PB'))
        content.append(Graphs.draw_little_title('4.2 行业风格PE'))
        content.append(Graphs.draw_little_title('5.1 行业PB'))
        content.append(Graphs.draw_little_title('5.2 行业PE'))
        
        # content.append(Graphs.draw_little_title('★1.1 中证全指PB'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\zzqzpb20.png'))
        #content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\zzqzpbfw20.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\zzqzpb10.png'))
        #content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\zzqzpbfw10.png'))
        # content.append(Graphs.draw_little_title('★1.2 中证全指PE'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\zzqzpe20.png'))
        #content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\zzqzpefw20.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\zzqzpe10.png'))
        #content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\zzqzpefw10.png'))

        # content.append(Graphs.draw_little_title('★2.1 指数PB'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\zspb13.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\zspbfw13.png'))
        # content.append(Graphs.draw_little_title('★2.2 指数PE'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\zspe13.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\zspefw13.png'))

        # content.append(Graphs.draw_little_title('★3.1 风格PB'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\fgpb13.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\fgpbfw13.png'))
        # content.append(Graphs.draw_little_title('★3.2 风格PE'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\fgpe13.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\fgpefw13.png'))

        # content.append(Graphs.draw_little_title('★4.1 行业风格PB'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\hfpb13.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\hfpbfw13.png'))
        # content.append(Graphs.draw_little_title('★4.2 行业风格PE'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\hfpe13.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\hfpefw13.png'))
      
        # content.append(Graphs.draw_little_title('★5.1 行业PB'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\hypbfw20.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\hypbfw10.png'))
        # content.append(Graphs.draw_little_title('★5.2 行业PE'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\hypefw20.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\2gzzb\hypefw10.png'))
        content.append(Graphs.draw_title2('数据来源：Choice  报告工具：Python'))

        # 生成pdf文件
        doc = SimpleDocTemplate(r'C:\xyzy\1lhjr\2gzzb\gzzb.pdf', pagesize=letter)
        doc.build(content)

# 中证全指PB
zs('000985.CSI','PBMRQ','2005-01-01',3,'中证全指PB20年走势','zzqzpb20')
#fwpb('000985.CSI',"PBMRQ","2005-01-01",3,"中证全指PB 20年分位",'zzqzpbfw20')
zs('000985.CSI','PBMRQ','2013-01-01',3,'中证全指PB10年走势','zzqzpb10')
#fwpb('000985.CSI',"PBMRQ","2005-01-01",3,"中证全指PB 10年分位",'zzqzpbfw10')
# 中证全指PE
zs('000985.CSI','PETTM','2005-01-01',3,'中证全指PE20年走势','zzqzpe20')
#fwpb('000985.CSI',"PBMRQ","2005-01-01",3,"中证全指PE 20年分位",'zzqzpefw20')
zs('000985.CSI','PETTM','2013-01-01',3,'中证全指PE10年走势','zzqzpe10')
#fwpb('000985.CSI',"PBMRQ","2005-01-01",3,"中证全指PE 10年分位",'zzqzpefw10')
        
# 指数PB
zs(zscode,'PBMRQ','2010-01-01',3,'指数PB13年走势','zspb13')
fwpb(zscode,"PBMRQ","2010-01-01",3,"指数PB13年分位",'zspbfw13',4)
# 指数PE
zs(zscode,'PETTM','2010-01-01',3,'指数PE13年走势','zspe13')
fwpe(zscode,'PETTM','2010-01-01',3,'指数PE13年分位','zspefw13',4)

# 风格PB
zs(fgcode,'PBMRQ','2010-01-01',3,'风格PB13年走势','fgpb13')
fwpb(fgcode,"PBMRQ","2005-01-01",3,"风格PB13年分位",'fgpbfw13',4)
# 风格PE
zs(fgcode,'PETTM','2010-01-01',3,'风格PE13年走势','fgpe13')
fwpe(fgcode,"PETTM","2005-01-01",3,"风格PE13年分位",'fgpefw13',4)

# 行业风格PB
zs(hfcode,'PBMRQ','2010-01-01',3,'行业风格PB13年走势','hfpb13')
fwpb(hfcode,"PBMRQ","2005-01-01",3,"行业风格PB13年分位",'hfpbfw13',5)
# 风格PE
zs(hfcode,'PETTM','2010-01-01',3,'行业风格PE13年走势','hfpe13')
fwpe(hfcode,"PETTM","2005-01-01",3,"行业风格PE13年分位",'hfpefw13',5)

# 行业市净率PBMRQ
hyfwpb(hycode,"PBMRQ","2005-01-01",3,"行业PB20年分位",'hypbfw20',31)
hyfwpb(hycode,"PBMRQ","2013-01-01",3,"行业PB10年分位",'hypbfw10',31)

# 行业市盈率PETTM
hyfwpe(hycode,"PETTM","2005-01-01",3,"行业PE20年分位",'hypefw20',31)
hyfwpe(hycode,"PETTM","2013-01-01",3,"行业PE10年分位",'hypefw10',31)

to_pdf()