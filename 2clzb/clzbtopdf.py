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
        ct.fontSize = 18           # 字体大小
        ct.leading = 20           # 行间距
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
        ct.fontSize = 10            # 字体大小
        ct.leading = 15             # 行间距
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
        ct.fontSize = 10  # 字体大小
        ct.leading = 10  # 行间距
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
        ct.fontSize = 10  # 字体大小
        ct.leading = 15  # 行间距
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
        ct.fontSize = 10  # 字体大小
        ct.leading = 15  # 行间距
        ct.textColor = colors.black  # 字体颜色
        ct.alignment = 1    # 居中
        # 创建标题对应的段落，并且返回
        return Paragraph(title, ct)
    
    @staticmethod
    def draw_little_title3(title: str):
        # 获取所有样式表
        style = getSampleStyleSheet()
        # 拿到标题样式
        ct = style['Normal']
        # 单独设置样式相关属性
        ct.fontName = 'SimSun'  # 字体名
        ct.fontSize = 18  # 字体大小
        ct.leading = 15 # 行间距
        ct.textColor = colors.black  # 字体颜色
        ct.alignment = 1    # 居中
        # 创建标题对应的段落，并且返回
        return Paragraph(title, ct)

    # 绘制图片
    @staticmethod
    def draw_img(path):
        img = Image(path)       # 读取指定路径下的图片
        img.drawWidth = 18*cm        # 设置图片的宽度
        img.drawHeight = 9*cm       # 设置图片的高度
        return img

    @staticmethod
    def draw_img1(path):
        img1 = Image(path)       # 读取指定路径下的图片
        img1.drawWidth = 25*cm        # 设置图片的宽度
        img1.drawHeight = 10*cm       # 设置图片的高度
        return img1
    
    @staticmethod
    def draw_img2(path):
        img2 = Image(path)       # 读取指定路径下的图片
        img2.drawWidth = 25*cm        # 设置图片的宽度
        img2.drawHeight = 18*cm       # 设置图片的高度
        return img2

date = (date.today() + timedelta(days = -0)).strftime("%Y-%m-%d")

if __name__ == '__main__':
    # 创建内容对应的空列表
    content = list()

    content.append(Graphs.draw_little_title3('策略周报'))
    content.append(Graphs.draw_little_title2(date))
    
    content.append(Graphs.draw_little_title('目录'))
    content.append(Graphs.draw_little_title('一、市场特征'))
    content.append(Graphs.draw_little_title('1.1 全球主要指数'))
    content.append(Graphs.draw_little_title('1.2 全球主要商品'))
    content.append(Graphs.draw_little_title('1.3 A股主要指数'))
    content.append(Graphs.draw_little_title('1.4 风格指数'))
    content.append(Graphs.draw_little_title('1.5 行业风格'))
    content.append(Graphs.draw_little_title('1.6 行业指数'))
    content.append(Graphs.draw_little_title('1.7 大小盘对比'))
    content.append(Graphs.draw_little_title('1.8 成长价值对比'))
    
    content.append(Graphs.draw_little_title('二、估值跟踪'))
    content.append(Graphs.draw_little_title('2.1 市场PE趋势'))
    content.append(Graphs.draw_little_title('2.2 市场PB趋势'))
    content.append(Graphs.draw_little_title('2.3 行业当前PE'))
    content.append(Graphs.draw_little_title('2.4 行业当前PB'))
    content.append(Graphs.draw_little_title('2.5 行业资金'))
    content.append(Graphs.draw_little_title1('2.6 标普500PE趋势'))
    
    content.append(Graphs.draw_little_title('一、市场特征'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\2clzb\qqzs.png'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\2clzb\qqsp.png'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\2clzb\agsczdf.png'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\2clzb\fgzf.png'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\2clzb\agfgzdf.png'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\2clzb\zxhy.png'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\2clzb\dpxp.png'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\2clzb\czjz.png'))


    content.append(Graphs.draw_little_title('二、估值跟踪'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\2clzb\agpe.png'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\2clzb\agpb.png'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\2clzb\hype.png'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\2clzb\hypb.png'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\2clzb\hyzj.png'))
    content.append(Graphs.draw_img1(r'C:\xyzy\1lhjr\2clzb\bppe.png'))
    
    content.append(Graphs.draw_title1('数据来源：Choice  报告工具：Python'))


    # 生成pdf文件
    doc = SimpleDocTemplate(r'C:\xyzy\1lhjr\2clzb\clzb.pdf', pagesize=letter)
    doc.build(content)