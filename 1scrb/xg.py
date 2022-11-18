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

def mainCallback(quantdata):
    """
    mainCallback 是主回调函数，可捕捉如下错误
    在start函数第三个参数位传入，该函数只有一个为c.EmQuantData类型的参数quantdata
    :param quantdata:c.EmQuantData
    :return:
    """
    print ("mainCallback",str(quantdata))
    #登录掉线或者 登陆数达到上线（即登录被踢下线） 这时所有的服务都会停止
    if str(quantdata.ErrorCode) == "10001011" or str(quantdata.ErrorCode) == "10001009":
        print ("Your account is disconnect. You can force login automatically here if you need.")
    #行情登录验证失败（每次连接行情服务器时需要登录验证）或者行情流量验证失败时，会取消所有订阅，用户需根据具体情况处理
    elif str(quantdata.ErrorCode) == "10001021" or str(quantdata.ErrorCode) == "10001022":
        print ("Your all csq subscribe have stopped.")
    #行情服务器断线自动重连连续6次失败（1分钟左右）不过重连尝试还会继续进行直到成功为止，遇到这种情况需要确认两边的网络状况
    elif str(quantdata.ErrorCode) == "10002009":
        print ("Your all csq subscribe have stopped, reconnect 6 times fail.")
    # 行情订阅遇到一些错误(这些错误会导致重连，错误原因通过日志输出，统一转换成EQERR_QUOTE_RECONNECT在这里通知)，正自动重连并重新订阅,可以做个监控
    elif str(quantdata.ErrorCode) == "10002012":
        print ("csq subscribe break on some error, reconnect and request automatically.")
    # 资讯服务器断线自动重连连续6次失败（1分钟左右）不过重连尝试还会继续进行直到成功为止，遇到这种情况需要确认两边的网络状况
    elif str(quantdata.ErrorCode) == "10002014":
        print ("Your all cnq subscribe have stopped, reconnect 6 times fail.")
    # 资讯订阅遇到一些错误(这些错误会导致重连，错误原因通过日志输出，统一转换成EQERR_INFO_RECONNECT在这里通知)，正自动重连并重新订阅,可以做个监控
    elif str(quantdata.ErrorCode) == "10002013":
        print ("cnq subscribe break on some error, reconnect and request automatically.")
    # 资讯登录验证失败（每次连接资讯服务器时需要登录验证）或者资讯流量验证失败时，会取消所有订阅，用户需根据具体情况处理
    elif str(quantdata.ErrorCode) == "10001024" or str(quantdata.ErrorCode) == "10001025":
        print("Your all cnq subscribe have stopped.")
    else:
        pass

def startCallback(message):
    print("[EmQuantAPI Python]", message)
    return 1
def csqCallback(quantdata):
    """
    csqCallback 是csq订阅时提供的回调函数模板。该函数只有一个为c.EmQuantData类型的参数quantdata
    :param quantdata:c.EmQuantData
    :return:
    """
    print ("csqCallback,", str(quantdata))

def cstCallBack(quantdata):
    '''
    cstCallBack 是日内跳价服务提供的回调函数模板
    '''
    for i in range(0, len(quantdata.Codes)):
        length = len(quantdata.Dates)
        for it in quantdata.Data.keys():
            print(it)
            for k in range(0, length):
                for j in range(0, len(quantdata.Indicators)):
                    print(quantdata.Data[it][j * length + k], " ",end = "")
                print()
def cnqCallback(quantdata):
    """
    cnqCallback 是cnq订阅时提供的回调函数模板。该函数只有一个为c.EmQuantData类型的参数quantdata
    :param quantdata:c.EmQuantData
    :return:
    """
    # print ("cnqCallback,", str(quantdata))
    print("cnqCallback,")
    for code in quantdata.Data:
        total = len(quantdata.Data[code])
        for k in range(0, len(quantdata.Data[code])):
            print(quantdata.Data[code][k])

try:
    #调用登录函数（激活后使用，不需要用户名密码）
    loginResult = c.start("ForceLogin=1", '', mainCallback)
    if(loginResult.ErrorCode != 0):
        print("login in fail")
        exit()

    # 市场特征
    date = datetime.today().strftime("%Y-%m-%d")
    # 指数涨幅
    xg5=c.css("300418.SZ,002191.SZ,002815.SZ,000776.SZ","NAME,DIFFERRANGEN","N=-5,TradeDate="+date+",AdjustFlag=1, Ispandas=1")
    xg10=c.css("300418.SZ,002191.SZ,002815.SZ,000776.SZ","NAME,DIFFERRANGEN","N=-10,TradeDate="+date+",AdjustFlag=1, Ispandas=1")
    xg20=c.css("300418.SZ,002191.SZ,002815.SZ,000776.SZ","NAME,DIFFERRANGEN","N=-20,TradeDate="+date+",AdjustFlag=1, Ispandas=1")
    xg60=c.css("300418.SZ,002191.SZ,002815.SZ,000776.SZ","NAME,DIFFERRANGEN","N=-60,TradeDate="+date+",AdjustFlag=1, Ispandas=1")
    xg120=c.css("300418.SZ,002191.SZ,002815.SZ,000776.SZ","NAME,DIFFERRANGEN","N=-120,TradeDate="+date+",AdjustFlag=1, Ispandas=1")
    xg250=c.css("300418.SZ,002191.SZ,002815.SZ,000776.SZ","NAME,DIFFERRANGEN","N=-250,TradeDate="+date+",AdjustFlag=1, Ispandas=1")
    # 指数走势
    date = datetime.today().strftime("%Y-%m-%d")
    xgxg=c.csd(" 300418.SZ,002191.SZ,002815.SZ,000776.SZ","CLOSE","2005-01-01",""+date+"","period=3,adjustflag=3,curtype=1,order=1,market=CNSESH, Ispandas=1")
    xgxg3=c.csd(" 300418.SZ,002191.SZ,002815.SZ,000776.SZ","CLOSE","2020-01-01",""+date+"","period=1,adjustflag=3,curtype=1,order=1,market=CNSESH, Ispandas=1")
    # 指数估值
    xgpb=c.csd(" 300418.SZ,002191.SZ,002815.SZ,000776.SZ","PBMRQ","2013-01-01",""+date+"","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH, Ispandas=1")
    xgpb3=c.csd(" 300418.SZ,002191.SZ,002815.SZ,000776.SZ","PBMRQ","2020-01-01",""+date+"","DelType=1,period=1,adjustflag=1,curtype=1,order=1,market=CNSESH, Ispandas=1")
    xgpbclose=c.css(" 300418.SZ,002191.SZ,002815.SZ,000776.SZ","SHORTNAME,PBMRQ","TradeDate="+date+",DelType=1, Ispandas=1")



#退出
    data = logoutResult = c.stop()
except Exception as ee:
    print("error >>>",ee)
    traceback.print_exc()
else:
    print("demo end")

# 指数走势
# 变更列名
xgxg.columns=['指数','日期','收盘价']
xgxg['指数'] = xgxg['指数'].str.replace('002815.SZ','昆仑万维')
xgxg['指数'] = xgxg['指数'].str.replace('002191.SZ','劲嘉股份 ')
xgxg['指数'] = xgxg['指数'].str.replace('002815.SZ','崇达技术 ')
xgxg['指数'] = xgxg['指数'].str.replace('000776.SZ','广发证券 ')
fig = px.line(xgxg,x='日期', y='收盘价',color='指数')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=1200,height=600,title={'text': "指数走势",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\xgxg.png',scale=3)

# 3年指数走势
# 变更列名
xgxg3.columns=['指数','日期','收盘价']
xgxg3['指数'] = xgxg3['指数'].str.replace('002815.SZ','昆仑万维')
xgxg3['指数'] = xgxg3['指数'].str.replace('002191.SZ','劲嘉股份 ')
xgxg3['指数'] = xgxg3['指数'].str.replace('002815.SZ','崇达技术 ')
xgxg3['指数'] = xgxg3['指数'].str.replace('000776.SZ','广发证券 ')
fig = px.line(xgxg3,x='日期', y='收盘价',color='指数')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 120,),width=1200,height=600,title={'text': "3年指数走势",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\xgxg3.png',scale=3)

# 指数估值
# 分位图10年
# 变更特定字符
xgpb['CODES'] = xgpb['CODES'].str.replace('002815.SZ', '昆仑万维')
xgpb['CODES'] = xgpb['CODES'].str.replace('002191.SZ', '劲嘉股份 ')
xgpb['CODES'] = xgpb['CODES'].str.replace('002815.SZ', '崇达技术 ')
xgpb['CODES'] = xgpb['CODES'].str.replace('000776.SZ', '广发证券 ')
# 保留1位小数
xgpbclose['PBMRQ'] = xgpbclose['PBMRQ'].apply(lambda x:format(x,'.1f'))
y0 = xgpbclose.PBMRQ[0]
y1 = xgpbclose.PBMRQ[1]
y2 = xgpbclose.PBMRQ[2]
y3 = xgpbclose.PBMRQ[3]
fig = px.violin(xgpb,x="CODES",y="PBMRQ",color="CODES",box=True,points='all')
fig.update_layout(width=1200,height=600,title={'text': "指数PB分位-10年",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                    title_font_size=35,font_size=15,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
#fig.update_yaxes(type='log')
fig.add_annotation(x=0,y=y0,text="现值{}".format(y0),ax=-55,ay=0)
fig.add_annotation(x=1,y=y1,text="现值{}".format(y1),ax=-55,ay=0)
fig.add_annotation(x=2,y=y2,text="现值{}".format(y2),ax=-55,ay=0)
fig.add_annotation(x=3,y=y3,text="现值{}".format(y3),ax=-55,ay=0)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\xgPB1.png',scale=3)
# 走势图10年
fig = px.line(xgpb,x='DATES', y='PBMRQ', color='CODES')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 24,),width=1200,height=600,title={'text': "指数PB走势-10年",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\xgPB2.png',scale=3)

# 分位图3年
# 变更特定字符
xgpb3['CODES'] = xgpb3['CODES'].str.replace('002815.SZ', '昆仑万维')
xgpb3['CODES'] = xgpb3['CODES'].str.replace('002191.SZ', '劲嘉股份 ')
xgpb3['CODES'] = xgpb3['CODES'].str.replace('002815.SZ', '崇达技术 ')
xgpb3['CODES'] = xgpb3['CODES'].str.replace('000776.SZ', '广发证券 ')

fig = px.violin(xgpb3,x="CODES",y="PBMRQ",color="CODES",box=True,points='all')
fig.update_layout(width=1200,height=600,title={'text': "指数PB分位-3年",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                    title_font_size=35,font_size=15,title_font_color='red',showlegend=False,xaxis_title=None,yaxis_title=None)
#fig.update_yaxes(type='log')
fig.add_annotation(x=0,y=y0,text="现值{}".format(y0),ax=-55,ay=0)
fig.add_annotation(x=1,y=y1,text="现值{}".format(y1),ax=-55,ay=0)
fig.add_annotation(x=2,y=y2,text="现值{}".format(y2),ax=-55,ay=0)
fig.add_annotation(x=3,y=y3,text="现值{}".format(y3),ax=-55,ay=0)
fig.write_image(r'C:\xyzy\1lhjr\1scrb\xgPB31.png',scale=3)
# 走势图3年
fig = px.line(xgpb3,x='DATES', y='PBMRQ', color='CODES')
fig.update_layout(xaxis = dict(tickmode='linear',tick0 = 1,dtick = 120,),width=1200,height=600,title={'text': "指数PB走势-3年",'y':0.98,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_size=35,font_size=15,title_font_color='red',xaxis_tickangle=-45,xaxis_title=None,yaxis_title=None)
fig.update_yaxes(type='log')
fig.write_image(r'C:\xyzy\1lhjr\1scrb\xgPB32.png',scale=3)

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
from datetime import timedelta, datetime
import time as _time
import traceback
from datetime import *

# 注册字体(提前准备好字体文件, 如果同一个文件需要多种字体可以注册多个)
pdfmetrics.registerFont(TTFont('SimSun', 'simsun.ttf'))

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
    
    @staticmethod
    def draw_little_title1(title: str):
        # 获取所有样式表
        style = getSampleStyleSheet()
        # 拿到标题样式
        ct = style['Normal']
        # 单独设置样式相关属性
        ct.fontName = 'SimSun'  # 字体名
        ct.fontSize = 20  # 字体大小
        ct.leading = 40  # 行间距
        ct.textColor = colors.red  # 字体颜色
        # 创建标题对应的段落，并且返回
        return Paragraph(title, ct)

    @staticmethod
    def draw_little_title2(title: str):
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

    # 绘制图片
    @staticmethod
    def draw_img(path):
        img = Image(path)       # 读取指定路径下的图片
        img.drawWidth = 22*cm        # 设置图片的宽度
        img.drawHeight = 10*cm       # 设置图片的高度
        return img

    @staticmethod
    def draw_img1(path):
        img1 = Image(path)       # 读取指定路径下的图片
        img1.drawWidth = 22*cm        # 设置图片的宽度
        img1.drawHeight = 11*cm       # 设置图片的高度
        return img1

    @staticmethod
    def draw_img2(path):
        img2 = Image(path)       # 读取指定路径下的图片
        img2.drawWidth = 22*cm        # 设置图片的宽度
        img2.drawHeight = 11*cm       # 设置图片的高度
        return img2

date = (datetime.today() + timedelta(days = -0)).strftime("%Y-%m-%d")

if __name__ == '__main__':
    # 创建内容对应的空列表
    content = list()

    content.append(Graphs.draw_title('选股'))
    content.append(Graphs.draw_little_title2(date))
    

    content.append(Graphs.draw_little_title('1、涨幅'))
    content.append(Graphs.draw_little_title('2、资金'))
    content.append(Graphs.draw_little_title('3、走势'))
    content.append(Graphs.draw_little_title('3、PB'))

    
    content.append(Graphs.draw_img2(r'C:\xyzy\1lhjr\1scrb\xghb.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\xg0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\xg5.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\xg10.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\xg20.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\xg60.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\xg120.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\xg250.png'))
    
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\xgzj0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\xgzj3.png'))

    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\xgxg.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\xgxg3.png'))

    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\xgPB1.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\xgPB2.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\xgPB31.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\xgPB32.png'))

    # 生成pdf文件
    doc = SimpleDocTemplate(r'C:\xyzy\1lhjr\1scrb\xg.pdf', pagesize=letter)
    doc.build(content)