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
jddates='2022-09-30','2022-06-30','2022-03-31','2021-12-31','2021-09-30','2021-06-30','2021-03-31','2020-12-31','2020-09-30','2020-06-30','2020-03-31',\
        '2019-12-31','2019-09-30','2019-06-30','2019-03-31','2018-12-31','2018-09-30','2018-06-30','2018-03-31'

for code in codes:
    # 沪深股票 市净率(PB,扣除商誉) 市盈率TTM（扣除非经常性损益）市销率PS 收盘价 成交金额 
    df=c.csd(code,"PBDEDUCTBS,PETTMDEDUCTED,PSTTM,CLOSE,AMOUNT","1990-12-24",""+today+"","period=3,adjustflag=3, curtype=1,order=1,market=CNSESH,filldata=1,\
            Rowindex=none,Ispandas=1")
    df=df.dropna()
    df['DATES']=df['DATES'].str[:7]
    # 净资产收益率ROETTM(扣除非经常性损益) 投入资本回报率ROIC 销售毛利率 销售净利率 营业总收入同比增长率 归属母公司股东的净利润同比增长率(扣除非经常性损益)
    # 总资产周转率 应收账款周转率(含应收票据) 应付账款周转率(含应付票据) 资产负债率 有息负债率 经营活动产生的现金流量净额/营业总收入 经营活动产生的现金流量净额/净利润 
    df1=pd.DataFrame()
    for date in nddates:
        data=c.css(code,"NAME,ROEEXWA,ROIC,GPMARGIN,NPMARGIN,YOYGR,YOYPNIDEDUCTED,ASSETTURNRATIO,ARTURNRATIO,APTURNRATIO,LIBILITYTOASSET,INTERESLIBILITYTOLIBILITY,\
                    CFOTOGR,CFOTONP",f"ReportDate={date},Ispandas=1")
        df1=pd.concat([df1,data],ignore_index=True)
    # 变更年份
    df1.DATES=['2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021']
    df1=df1.dropna(thresh=3)
    df=pd.concat([df.reset_index(drop=True),df1.reset_index(drop=True)],axis=1,ignore_index=False)
    # 变更列名
    df.columns=['股票名称', '日期', '市净率', '市盈率', '市销率', '股价', '成交金额','年份', '股票', '净资产收益率', '投入资本回报率', '销售毛利率', '销售净利率',\
              '收入增长率', '净利润增长率', '总资产周转率', '应收账款周转率', '应付账款周转率','资产负债率', '有息负债率', '收现率', '净现率']
    df.股票名称 = df.股票名称.str.replace('code', 'df.股票[0]')
    df = df.drop('股票',axis=1)
    df.to_excel(Fr'C:\xyzy\1lhjr\5gsfx\ndsj\{code[0:6]}.xlsx')



