# -*- coding: utf-8 -*-

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
        ct.textColor = colors.black     # 字体颜色
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
        ct.fontSize = 15            # 字体大小
        ct.leading = 30             # 行间距
        ct.textColor = colors.black     # 字体颜色
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
    
    @staticmethod
    def draw_little_title1(title: str):
        # 获取所有样式表
        style = getSampleStyleSheet()
        # 拿到标题样式
        ct = style['Normal']
        # 单独设置样式相关属性
        ct.fontName = 'SimSun'  # 字体名
        ct.fontSize = 15  # 字体大小
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
        ct.fontSize = 15  # 字体大小
        ct.leading = 40  # 行间距
        ct.textColor = colors.red  # 字体颜色
        ct.alignment = 1    # 居中
        # 创建标题对应的段落，并且返回
        return Paragraph(title, ct)

    # 绘制图片
    @staticmethod
    def draw_img(path):
        img = Image(path)       # 读取指定路径下的图片
        img.drawWidth = 20*cm        # 设置图片的宽度
        img.drawHeight = 10*cm       # 设置图片的高度
        return img

    @staticmethod
    def draw_img1(path):
        img1 = Image(path)       # 读取指定路径下的图片
        img1.drawWidth = 20*cm        # 设置图片的宽度
        img1.drawHeight = 11*cm       # 设置图片的高度
        return img1

    @staticmethod
    def draw_img2(path):
        img2 = Image(path)       # 读取指定路径下的图片
        img2.drawWidth = 20*cm        # 设置图片的宽度
        img2.drawHeight = 5*cm       # 设置图片的高度
        return img2

date = (datetime.today() + timedelta(days = -0)).strftime("%Y-%m-%d")

if __name__ == '__main__':
    # 创建内容对应的空列表
    content = list()

    content.append(Graphs.draw_title('金融市场日报'))
    content.append(Graphs.draw_little_title2(date))
    
    content.append(Graphs.draw_little_title('目录'))
    content.append(Graphs.draw_little_title('1、指数涨幅'))
    content.append(Graphs.draw_little_title('2、指数资金'))
    content.append(Graphs.draw_little_title('3、风格涨幅'))
    content.append(Graphs.draw_little_title('4、风格资金'))
    content.append(Graphs.draw_little_title('5、行业涨幅'))
    content.append(Graphs.draw_little_title1('6、行业资金'))
    
    content.append(Graphs.draw_little_title('★1、指数涨幅'))
    content.append(Graphs.draw_img2(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfubiaoge.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu5.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu10.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu20.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu60.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu120.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zhishuzhangfu250.png'))
    
    content.append(Graphs.draw_little_title('★2、指数资金'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zhishuzijin0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\zhishuzijin2.png'))

    content.append(Graphs.draw_little_title('★3、风格涨幅'))
    content.append(Graphs.draw_img2(r'C:\xyzy\1lhjr\1scrb\fenggezhangfubiaoge.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu5.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu10.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu20.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu60.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu120.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fenggezhangfu250.png'))

    content.append(Graphs.draw_little_title('★4、风格资金'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fenggezijin0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\fenggezijin2.png'))

    content.append(Graphs.draw_little_title('★5、行业涨幅'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu5.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu10.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu20.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu60.png'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu120.png'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\1scrb\hangyezhangfu250.png'))

    content.append(Graphs.draw_little_title('★6、行业资金'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hangyezijin0.png'))
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\1scrb\hangyezijin2.png'))

    content.append(Graphs.draw_title1('数据来源：Choice  报告工具：Python'))

    # 生成pdf文件
    doc = SimpleDocTemplate(r'C:\xyzy\1lhjr\1scrb\ribao.pdf', pagesize=letter)
    doc.build(content)