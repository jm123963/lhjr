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
        ct.leading = 30  # 行间距
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
        ct.textColor = colors.black  # 字体颜色
        ct.alignment = 1    # 居中
        # 创建标题对应的段落，并且返回
        return Paragraph(title, ct)

    # 绘制普通段落内容
    @staticmethod
    def draw_text(text: str):
        # 获取所有样式表
        style = getSampleStyleSheet()
        # 获取普通样式
        ct = style['Normal']
        ct.fontName = 'SimSun'
        ct.fontSize = 13
        ct.wordWrap = 'CJK'     # 设置自动换行
        ct.alignment = 0        # 左对齐
        ct.firstLineIndent = 0     # 第一行开头空格
        ct.leading = 25
        return Paragraph(text, ct)
    
    # 绘制图片
    @staticmethod
    def draw_img(path):
        img = Image(path)       # 读取指定路径下的图片
        img.drawWidth = 20*cm        # 设置图片的宽度
        img.drawHeight = 10*cm       # 设置图片的高度
        return img

date = (date.today() + timedelta(days = -0)).strftime("%Y-%m-%d")

if __name__ == '__main__':
    # 创建内容对应的空列表
    content = list()

    content.append(Graphs.draw_title('宏观月报'))
    content.append(Graphs.draw_little_title2(date))
    
    content.append(Graphs.draw_text('目录'))
    content.append(Graphs.draw_text('1、 A股主要指数走势对比'))
    content.append(Graphs.draw_text('2、 本年行业涨跌幅'))
    content.append(Graphs.draw_text('3、 我国GDP季度增速'))
    content.append(Graphs.draw_text('4、 社会消费品零售总额同比'))
    content.append(Graphs.draw_text('5、 社会消费品零售总额环比'))
    content.append(Graphs.draw_text('6、 社会消费品零售总额累计增速'))
    content.append(Graphs.draw_text('7、 固定资产、房地产投资累计同比'))
    content.append(Graphs.draw_text('8、 本年购置土地面积累计同比'))
    content.append(Graphs.draw_text('9、 我国进出口增速同比'))
    content.append(Graphs.draw_text('10、 我国CPI同比及环比'))
    content.append(Graphs.draw_text('11、 全国猪肉批发月平均价格'))
    content.append(Graphs.draw_text('12、 全国农产品批发月平均价格'))
    content.append(Graphs.draw_text('13、 我国PPI同比及环比'))
    content.append(Graphs.draw_text('14、 M2和社融同比增速'))
    content.append(Graphs.draw_text('15、 社会融资总量余额增速'))
    content.append(Graphs.draw_text('16、 美国CPI与核心CPI同比'))
    
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\agzs.png'))
    content.append(Graphs.draw_text('2022年上半年A股市场总体呈现单边下行态势，5月之后开启反弹。'))

    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\hangyezhangfuzj.png'))
    content.append(Graphs.draw_text('2022年上半年稳增长主线占优。'))
    
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\gdp.png'))
    content.append(Graphs.draw_text('我国经济2022年一季度实现了4.8%，低于两会5.5%的政策目标。由于二季度遭遇到疫情冲击，经济增速将低于一季度，二季度或是全年的经济底。'))
    
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\xfpls.png'))
    content.append(Graphs.draw_text('1—5月份，社会消费品零售总额171,689 亿元，同比下降1.5%。5月消费数据边际改善，同比降幅收窄。5月社会消费品零售总额同比下降6.7%，较4月降幅收窄4.4 个百分点。'))

    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\xfplshb.png'))

    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\xfplslj.png'))

    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\gdzcfdclj.png'))
    content.append(Graphs.draw_text('1—5月份，全国固定资产投资205,964亿元，同比增长6.2%。1—5月份，全国房地产开发投资52,134 亿元，同比下降4.0%；其中，住宅投资39,521亿元，下降3.0%。'))

    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\fdcxs.png'))

    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\fdctd.png'))

    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\jck.png'))
    content.append(Graphs.draw_text('5月中国进出口总值3.45万亿元人民币，同比增长9.6%，增速比上月大幅提高9.5个百分点。'))

    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\cpi.png'))
    content.append(Graphs.draw_text('通胀保持温和，CPI与上月持平。5月份全国CPI同比上涨2.1%，涨幅与上月相同，环比则由上月上涨0.4%转为下降0.2%。'))
    
    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\btz.png'))
    content.append(Graphs.draw_text('中央储备猪肉收储工作继续开展，猪肉价格跌幅开始逐步收窄。5月白条肉月均价格同比降幅收在至-23%，不过进入6 月份白条肉价格基本与去年同期持平。'))

    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\ncpjg.png'))
    content.append(Graphs.draw_text('农产品批发价格在年初稍有跌落，在3月后开始回升上涨。'))

    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\ppi.png'))
    content.append(Graphs.draw_text('上半年PPI 整体从高位往下回落。5 月PPI 同比上涨6.4%，环比上涨0.1%。涨幅均继续回落。'))

    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\m2sr.png'))
    content.append(Graphs.draw_text('M2同比增长11.1%，新增社融规模超预期。'))

    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\rzye.png'))
    content.append(Graphs.draw_text('今年受地缘政治冲突、国内疫情反复影响，在1、3、4 月份融资减少较多。随着市场逐步企稳，进入5月融资余额开始缓慢回升。预计下半年融资余额将保持相对稳定。'))

    content.append(Graphs.draw_img(r'C:\xyzy\1lhjr\3hgyb\mgcpi.png'))
    content.append(Graphs.draw_text('5月美国CPI同比8.6%，前值8.3%。核心CPI同比6.0%，前值6.2%。CPI环比1.0%，前值0.3%，核心CPI环比0.6%，前值0.6%。'))

    content.append(Graphs.draw_title1('数据来源：Choice  报告工具：Python'))
    
# 生成pdf文件
    doc = SimpleDocTemplate(r'C:\xyzy\1lhjr\3hgyb\hgyb.pdf', pagesize=letter)
    doc.build(content)