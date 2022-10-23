from __future__ import print_function, absolute_import, unicode_literals
from gm.api import *
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.tsa.stattools as sttools
from statsmodels.tsa.stattools import adfuller
import pandas as pd
import numpy as np
import datetime
# 用来正常显示中文标签        
plt.rcParams['font.sans-serif']=['SimHei'] 
#用来正常显示负号        
plt.rcParams['axes.unicode_minus']=False 
pd.set_option('display.max_rows',None)      #显示所有列 
pd.set_option('display.max_columns',None)   #显示所有行
pd.set_option('colheader_justify', 'center')    #  显示居中还是左边 

class myquant():
    def __init__(self,date= None):
        # 获取当前日期(不是交易日的话，返回最近一个交易日)
        self.current_date = datetime.datetime.now() if date is None else date
        if len(get_trading_dates(exchange='SZSE', start_date=self.current_date, end_date=self.current_date))==0:
            self.current_date = get_previous_trading_date(exchange='SZSE', date=self.current_date)
        self.current_date_str = self.current_date.strftime('%Y-%m-%d')
        # 获取上一个交易日
        self.last_date = get_previous_trading_date(exchange='SZSE', date=self.current_date)
        # 获取所有股票
        self.all_stocks,self.all_stocks_str = self.get_normal_stocks(self.current_date,new_days=0)
        # 计算当日收益
        self.stocks_rate = self.get_return()
        # 其他信息数据
        # 收盘价（除权）
        self.close  = history(symbol=self.all_stocks_str, frequency='1d', start_time=self.current_date,  end_time=self.current_date, fields='symbol, close', adjust=ADJUST_NONE, df= True)
        self.base_data = get_history_instruments(symbols=self.all_stocks, start_date=self.current_date, end_date=self.current_date, df=True)
        self.base_data = self.base_data.merge(self.close,on='symbol',how='left')
        self.close.set_index('symbol',inplace=True)
        # 单季度归母净利润
        self.quarter_net_profit = None
        # 单季度ROE及其报告日期
        self.quarter_ROE = None
        self.quarter_ROE_end_date = None
        # 单季度ROA及其报告日期
        self.quarter_ROA = None
        self.quarter_ROA_end_date = None
        # 一个月反转
        self.inversion_1month = None

def plot_distribution(self):
    """绘制涨幅分布图"""
    # 计算各区间的股票数量
    rate_neg10 = len(self.base_data[(self.base_data['close']==self.base_data['lower_limit'])&(self.base_data['sec_level']==1)])# 跌停(不包含ST)
    rate_10 = len(self.base_data[(self.base_data['close']==self.base_data['upper_limit'])&(self.base_data['sec_level']==1)])# 涨停(不包含ST)
    is_suspended = len(self.base_data[(self.base_data['is_suspended']==1)])# 停牌
    rate_neg8t10 = len(self.stocks_rate[self.stocks_rate<=-0.08])# <=-8%
    rate_neg6t8 = len(self.stocks_rate[(self.stocks_rate<=-0.06)&(self.stocks_rate>-0.08)])# -8%至-6%
    rate_neg4t6 = len(self.stocks_rate[(self.stocks_rate<=-0.04)&(self.stocks_rate>-0.06)])# -6%至-4%
    rate_neg2t4 = len(self.stocks_rate[(self.stocks_rate<=-0.02)&(self.stocks_rate>-0.04)])# -4%至-2%
    rate_neg0t2 = len(self.stocks_rate[(self.stocks_rate<-0.00)&(self.stocks_rate>-0.02)])# -2%至-0%
    rate_0 = len(self.stocks_rate[(self.stocks_rate==0.00)])# 0%
    rate_0t2 = len(self.stocks_rate[(self.stocks_rate<=0.02)&(self.stocks_rate>0.00)])# 0%至2%
    rate_2t4 = len(self.stocks_rate[(self.stocks_rate<=0.04)&(self.stocks_rate>0.02)])# 2%至4%
    rate_4t6 = len(self.stocks_rate[(self.stocks_rate<=0.06)&(self.stocks_rate>0.04)])# 4%至6%
    rate_6t8 = len(self.stocks_rate[(self.stocks_rate<=0.08)&(self.stocks_rate>0.06)])# 6%至8%
    rate_8t10 = len(self.stocks_rate[self.stocks_rate>0.08])# >8%
    # 汇总统计
    down_num = rate_neg0t2+rate_neg2t4+rate_neg4t6+rate_neg6t8+rate_neg8t10+rate_neg10# 下跌
    none_num = rate_0# 平盘
    up_num = rate_0t2+rate_2t4+rate_4t6+rate_6t8+rate_8t10+rate_10# 上涨
    # 输出
    print('当前日期：{}'.format(self.current_date_str),end = '    ')
    print('赚钱效应：{:0.2f}%'.format(100*up_num/(up_num+down_num)))
    
    print('下跌：{:4}家'.format(down_num),end = '    ')
    print('平盘：{:4}家'.format(none_num),end = '    ')
    print('上涨：{:4}家'.format(up_num))
    
    print('跌停：{:4}家'.format(rate_neg10),end = '    ')
    print('停牌：{:4}家'.format(is_suspended),end = '    ')
    print('涨停：{:4}家'.format(rate_10))
    
    print('注：1、股票不包含北交所股票；\n    2、涨幅为0的股票包含在(-2%,0%]中；\n    3、部分涨跌停股票可能存在未彻底封板情况。')
    
    # 绘图
    plt.figure(figsize=(10,5))
    data_zf = [rate_neg10,rate_neg8t10,rate_neg6t8,rate_neg4t6,rate_neg2t4,rate_neg0t2,rate_0t2,rate_2t4,rate_4t6,rate_6t8,rate_8t10,rate_10]
    idx = np.arange(len(data_zf))
    colors = ['g']*6+['r']*6
    plt.bar(idx,data_zf,color=colors,zorder=10)
    for a,b in zip(idx, data_zf):            
        plt.text(a, b+max(data_zf)/100, '%.0f' % b, ha='center', va= 'bottom',fontsize=10)
    label = ['跌停  ','<=-8%','(-8%,-6%] ','(-6%,-4%] ','(-4%,2%] ','(-2%,0%) ','(0%,2%]','(2%,4%] ','(4%,6%] ','(6%,8%] ','>8%','涨停  ']
    plt.xticks(idx,label, rotation=45)
    plt.title('全市场涨跌分布({})'.format(self.current_date_str))
    plt.grid(axis='y',zorder=0)
    plt.show()

    # 请替换您的掘金终端token
set_token('b3b25e805bd20c4156e558bbf97683f98c89f620')
# set_token('90270ec166064d4a4e8376d1af68cc145ecc99c7')
mq = myquant(date=datetime.datetime(2022,10,12))

# 个股统计
mq.plot_distribution()

