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

# 绘制FB股票走势
data = xlrd.open_workbook(r'C:\xyzy\1lhjr\1scrb\zhishu10y.xls')
print(data)
#fig = px.line(data, x="DATES", y="CLOSE")
#fig.update_layout(title={'text':'中证全指走势','x':0.52,'y':0.96,'xanchor':'center','yanchor':'top'})
#fig.show()

#fig.write_image(r'C:\xyzy\1lhjr\1scrb\zhishu10y.png')

