from EmQuantAPI import *
from datetime import timedelta, datetime
import time as _time
import traceback
from datetime import *
import numpy as np
import pandas as pd
from pandas import DataFrame
from pylab import mpl
from pandas.plotting import table
#调用登录函数（激活后使用，不需要用户名密码）
loginResult = c.start("ForceLogin=1", '')

codes = '605336.SH','002757.SZ','002191.SZ','300418.SZ','002815.SZ','688230.SH','002236.SZ','000776.SZ'
# 当前时间
today = datetime.today().strftime("%Y-%m-%d")
nddates='2001-12-31','2002-12-31','2003-12-31','2004-12-31','2005-12-31','2006-12-31','2007-12-31','2008-12-31','2009-12-31','2010-12-31','2011-12-31','2012-12-31',\
        '2013-12-31','2014-12-31','2015-12-31','2016-12-31','2017-12-31','2018-12-31','2019-12-31','2020-12-31','2021-12-31'
jddates='2017-03-31','2017-06-30','2017-09-30','2017-12-31','2018-03-31','2018-06-30','2018-09-30','2018-12-31','2019-03-31','2019-06-30','2019-09-30','2019-12-31',\
        '2020-03-31','2020-06-30','2020-09-30','2020-12-31','2021-03-31','2021-06-30','2021-09-30','2021-12-31','2022-03-31','2022-06-30','2022-09-30'

for code in codes:
    # 沪深股票 市净率(PB,扣除商誉) 市盈率TTM（扣除非经常性损益）市销率PS 收盘价 成交量 
    df=c.csd(code,"PBDEDUCTBS,PETTMDEDUCTED,PSTTM,CLOSE,VOLUME","1990-12-24",""+today+"","period=3,adjustflag=3, curtype=1,order=1,market=CNSESH,filldata=1,\
            Rowindex=none,Ispandas=1")
    df=df.dropna()
    df['DATES']=df['DATES'].str[:7]
    # 变更列名
    df.columns=['股票名称', '日期', '市净率', '市盈率', '市销率', '股价', '成交量']

    # 净资产收益率ROETTM(扣除非经常性损益) 投入资本回报率ROIC 销售毛利率 销售净利率 营业总收入同比增长率 归属母公司股东的净利润同比增长率(扣除非经常性损益)
    # 总资产周转率 应收账款周转率(含应收票据) 应付账款周转率(含应付票据) 资产负债率 有息负债率 经营活动产生的现金流量净额/营业总收入 经营活动产生的现金流量净额/净利润 
    # 报告期数据
    df1=pd.DataFrame()
    for date in jddates:
        data=c.css(code,"ROEWA,ROIC,GPMARGIN,NPMARGIN,YOYGR,YOYPNIDEDUCTED,ASSETTURNRATIO,ARTURNRATIO,APTURNRATIO,LIBILITYTOASSET,INTERESLIBILITYTOLIBILITY,\
                    CFOTOGR,CFOTONP",f"ReportDate={date},Ispandas=1")
        df1=pd.concat([df1,data],ignore_index=True)
    # 变更年份
    df1.DATES=['2017ZQ1','2017ZQ2','2017ZQ3','2017ZQ4','2018ZQ1','2018ZQ2','2018ZQ3','2018ZQ4','2019ZQ1','2019ZQ2','2019ZQ3','2019ZQ4','2020ZQ1','2020ZQ2',\
                '2020ZQ3','2020ZQ4','2021ZQ1','2021ZQ2','2021ZQ3','2021ZQ4','2022ZQ1','2022ZQ2','2022ZQ3']
    # 变更列名
    df1.columns=['报告期', '报告期净资产收益率', '报告期投入资本回报率', '报告期销售毛利率','报告期销售净利率','报告期收入增长率','报告期净利润增长率','报告期总资产周转率',\
                '报告期应收账款周转率','报告期应付账款周转率','报告期资产负债率', '报告期有息负债率', '报告期收现率', '报告期净现率']
    df1=df1.dropna(thresh=3)
    
    # 年度数据
    df2=pd.DataFrame()
    for date in nddates:
        data=c.css(code,"NAME,ROEEXWA,ROIC,GPMARGIN,NPMARGIN,YOYGR,YOYPNIDEDUCTED,ASSETTURNRATIO,ARTURNRATIO,APTURNRATIO,LIBILITYTOASSET,INTERESLIBILITYTOLIBILITY,\
                    CFOTOGR,CFOTONP",f"ReportDate={date},Ispandas=1")
        df2=pd.concat([df2,data],ignore_index=True)
    # 变更年份
    df2.DATES=['2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021']
    # 变更列名
    df2.columns=['年份', '股票', '净资产收益率', '投入资本回报率', '销售毛利率', '销售净利率','收入增长率', '净利润增长率', '总资产周转率', '应收账款周转率',\
                '应付账款周转率','资产负债率', '有息负债率', '收现率', '净现率']
    df2=df2.dropna(thresh=3)

    # 单季度数据
    df3=pd.DataFrame()
    for date in jddates:
        data=c.css(code,"QROEDEDUCTED,QROA,QGPMARGIN,QNPMARGIN,QYOYGR,QYOYNIDEDUCTED,QCFOTOOR,QCFOTOOPERATEINCOME",f"ReportDate={date},Ispandas=1")
        df3=pd.concat([df3,data],ignore_index=True)
    # 变更年份
    df3.DATES=['2017Q1','2017Q2','2017Q3','2017Q4','2018Q1','2018Q2','2018Q3','2018Q4','2019Q1','2019Q2','2019Q3','2019Q4','2020Q1','2020Q2','2020Q3','2020Q4',\
                '2021Q1','2021Q2','2021Q3','2021Q4','2022Q1','2022Q2','2022Q3']
    # 变更列名
    df3.columns=['单季度', '季度净资产收益率','季度总资产净利率', '季度销售毛利率', '季度销售净利率','季度收入增长率', '季度净利润增长率', '季度收现率', '季度净现率']
    df3=df3.dropna(thresh=3)
    
    df=pd.concat([df.reset_index(drop=True),df1.reset_index(drop=True),df2.reset_index(drop=True),df3.reset_index(drop=True)],axis=1,ignore_index=False)
    df = df.replace(f'{code}', f'{df.股票[0]}')
    df = df.drop('股票',axis=1)
    df.to_excel(Fr'C:\xyzy\1lhjr\5gsfx\tzsj\{code[0:6]}.xlsx')





