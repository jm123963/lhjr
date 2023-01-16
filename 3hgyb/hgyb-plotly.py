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
def zs(code,sdate,dtick,text,image):
    df=c.edb(code, f"IsLatest=0,StartDate={sdate},EndDate="+date+",Ispandas=1")
    df['DATES']=df['DATES'].str[:7]
    fig = px.line(df,x='DATES',y='RESULT')
    fig.update_layout(xaxis = dict(tickmode='linear',tick0=1,dtick =dtick,),width=1200,height=600,title={'text':text,'y':0.98,'x':0.5,'xanchor': 'center',
                    'yanchor': 'top'},title_font_size=30,font_size=15,title_font_color='red',xaxis_title=None,yaxis_title=None,
                    legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
    fig.write_image(Fr'C:\xyzy\1lhjr\3hgyb\{image}.png',scale=3)

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
            ct.leading = 30  # 行间距
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
            ct.leading = 18  # 行间距
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

        content.append(Graphs.draw_title('宏 观 数 据 月 报'))
        content.append(Graphs.draw_title1(date))
        
        content.append(Graphs.draw_little_title('目录'))
        content.append(Graphs.draw_little_title('1. GDP同比增速'))
        content.append(Graphs.draw_little_title('2. 通货膨胀-CPI月同比'))
        content.append(Graphs.draw_little_title('3. 通货膨胀-PPI月同比'))
        content.append(Graphs.draw_little_title('4. 景气度-PMI采购经理指数 '))
        content.append(Graphs.draw_little_title('5. 景气度-失业率'))
        content.append(Graphs.draw_little_title('6. 需求-固定资产投资完成额累计同比'))
        content.append(Graphs.draw_little_title('7. 需求-固定资产投资完成额:制造业:累计同比'))
        content.append(Graphs.draw_little_title('8. 需求-固定资产投资完成额:建筑业:累计同比'))
        content.append(Graphs.draw_little_title('9. 需求-房地产开发投资完成额：累计同比'))
        content.append(Graphs.draw_little_title('10. 需求-出口金额:累计同比'))
        content.append(Graphs.draw_little_title('11. 需求-出口金额:累计同比'))
        content.append(Graphs.draw_little_title('12. 需求-社会消费品零售总额累计同比'))
        content.append(Graphs.draw_little_title('13. 供给-工业增加值:累计同比'))
        content.append(Graphs.draw_little_title('14. 信贷-离岸人民币汇率'))
        content.append(Graphs.draw_little_title('15. 信贷-国债到期收益率:10年'))
        content.append(Graphs.draw_little_title('16. 信贷-国债到期收益率:5年'))
        content.append(Graphs.draw_little_title('17. 信贷-国债到期收益率:1年'))
        content.append(Graphs.draw_little_title('18. 信贷-社会融资增量:累计值(亿)'))
        content.append(Graphs.draw_little_title('19. 信贷-社会融资增量:新增人民币贷款:累计值(亿)'))
        content.append(Graphs.draw_little_title('20. 信贷-M1:同比'))
        content.append(Graphs.draw_little_title('21. 信贷-M2:同比'))
        content.append(Graphs.draw_little_title('22. 信贷-实体经济部门杠杆率'))
        content.append(Graphs.draw_little_title('23. 信贷-政府部门杠杆率'))
        content.append(Graphs.draw_little_title('24. 信贷-居民部门杠杆率'))
        content.append(Graphs.draw_little_title('25. 财政-公共财政收入:累计同比'))
        content.append(Graphs.draw_little_title('26. 财政-公共财政支出:累计同比'))
        content.append(Graphs.draw_little_title('27. 财政-地方政府债券平均发行利率'))
        content.append(Graphs.draw_little_title('28. 财政-地方政府债券发行额:累计值（亿）'))
        
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\gdp.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\cpi.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\ppi.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\pmi.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\syl.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\gdzc.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\gdzczzy.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\gdzcjzy.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\fdckf.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\ckje.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\jkje.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\lsze.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\gyzjz.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\rmbhl.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\gzsyl10.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\gzsyl5.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\gzsyl1.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\rzgm.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\rzgmdk.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\m1.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\m2.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\jjgg.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\jjggzf.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\jjggjm.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\czsr.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\czzc.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\zfzqll.png'))
        content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\zfzqje.png'))
        content.append(Graphs.draw_title2('数据来源：Choice  报告工具：Python'))

        # 生成pdf文件
        doc = SimpleDocTemplate(r'C:\xyzy\1lhjr\3hgyb\hgyb.pdf', pagesize=letter)
        doc.build(content)

# GDP同比增速 
zs('EMM00000012','1990-01-01',12,'GDP同比增速','gdp')
# CPI月同比 
zs('EMM00072301','1990-01-01',36,'通货膨胀-CPI月同比','cpi')
# PPI月同比 
zs('EMM00073348','1990-01-01',24,'通货膨胀-PPI月同比','ppi')
# PMI指数 
zs('EMM00121996','1990-01-01',24,'景气度-采购经理指数','pmi')
# 失业率 
zs('EMM00631597','1990-01-01',12,'景气度-失业率','syl')
# 固定资产投资完成额累计同比（%）
zs('EMM00027210','1990-01-01',33,'需求-固定资产投资完成额累计同比（%）','gdzc')
# 固定资产投资完成额:制造业:累计同比
zs('EMM00027220','1990-01-01',33,'需求-固定资产投资完成额:制造业:累计同比（%）','gdzczzy')
# 固定资产投资完成额:建筑业:累计同比
zs('EMM00027257','1990-01-01',33,'需求-固定资产投资完成额:建筑业:累计同比（%）','gdzcjzy')
# 房地产开发投资完成额：累计同比
zs('EMM00039176','1990-01-01',33,'需求-房地产开发投资完成额：累计同比（%）','fdckf')
# 出口金额:累计同比
zs('EMM00053070','1990-01-01',33,'需求-出口金额:累计同比（%）','ckje')
# 进口金额:累计同比
zs('EMM00053094','1990-01-01',33,'需求-进口金额:累计同比（%）','jkje')
# 社会消费品零售总额累计同比（%）
zs('EMM00063225','1990-01-01',33,'需求-社会消费品零售总额累计同比（%）','lsze')
# 工业增加值:累计同比（%）
zs('EMM00008464','1990-01-01',33,'供给-工业增加值:累计同比（%）','gyzjz')
# 离岸人民币汇率
zs('EMM00618963','1990-01-01',12,'信贷-离岸人民币汇率','rmbhl')
# 国债到期收益率:10年
zs('E1001827','1990-01-01',12,'信贷-国债到期收益率:10年','gzsyl10')
# 国债到期收益率:5年
zs('E1001823','1990-01-01',12,'信贷-国债到期收益率:5年','gzsyl5')
# 国债到期收益率:1年
zs('E1001819','1990-01-01',12,'信贷-国债到期收益率:1年','gzsyl1')
# 社会融资增量:累计值(亿)
zs('EMM00088692','1990-01-01',12,'信贷-社会融资增量:累计值(亿)','rzgm')
# 社会融资增量:新增人民币贷款:累计值(亿)
zs('EMM00088693','1990-01-01',12,'信贷-社会融资增量:新增人民币贷款:累计值(亿)','rzgmdk')
# M1:同比
zs('EMM00087084','1990-01-01',12,'信贷-M1:同比','m1')
# M2:同比
zs('EMM00087086','1990-01-01',12,'信贷-M2:同比','m2')
# 实体经济部门杠杆率
zs('EMM01244359','1990-01-01',12,'信贷-实体经济部门杠杆率','jjgg')
# 政府部门杠杆率
zs('EMM01244356','1990-01-01',12,'信贷-政府部门杠杆率','jjggzf')
# 居民部门杠杆率
zs('EMM01244354','1990-01-01',12,'信贷-居民部门杠杆率','jjggjm')
# 公共财政收入:累计同比(%)
zs('EMM00058449','1990-01-01',36,'财政-公共财政收入:累计同比(%)','czsr')
# 公共财政支出:累计同比(%)-
zs('EMM00058496','1990-01-01',36,'财政-公共财政支出:累计同比(%)','czzc')
# 地方政府债券平均发行利率（%）
zs('EMM01259592','1990-01-01',12,'财政-地方政府债券平均发行利率（%）','zfzqll')
# 地方政府债券发行额:累计值（亿）
zs('EMM01259582','1990-01-01',12,'财政-地方政府债券发行额:累计值（亿）','zfzqje')

to_pdf()