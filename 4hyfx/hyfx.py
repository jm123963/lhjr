from EmQuantAPI import *
from datetime import timedelta, datetime
#调用登录函数（激活后使用，不需要用户名密码）
loginResult = c.start("ForceLogin=1", '')

date = datetime.today().strftime("%Y-%m-%d")
hycode="801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,\
        801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,\
        801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI"
# 指数 指数简称 
data=c.css("801010.SWI,801030.SWI,801040.SWI,801050.SWI,801080.SWI,801110.SWI,801120.SWI,801130.SWI,801140.SWI,801150.SWI,801160.SWI,801170.SWI,801180.SWI,801200.SWI,801210.SWI,801230.SWI,801710.SWI,801720.SWI,801730.SWI,801740.SWI,801750.SWI,801760.SWI,801770.SWI,801780.SWI,801790.SWI,801880.SWI,801890.SWI,801950.SWI,801960.SWI,801970.SWI,801980.SWI","SHORTNAME","Ispandas=1")
print(data)
# 指数 净资产收益率 市净率PB(MRQ) 市盈率PE(TTM) 收盘价 成交量 
#df=c.csd(hycode,"ROE,PBMRQ,PETTM,CLOSE","2000-01-01","2023-01-15","DelType=1,period=3,adjustflag=1,curtype=1,order=1,market=CNSESH,Rowindex=none,Ispandas=1")
#df.to_excel(Fr'C:\xyzy\1lhjr\4hyfx\hysj.xlsx')