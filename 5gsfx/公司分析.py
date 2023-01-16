#盈利：（ROE、ROIC）、（净利率、毛利率）
#成长：（利润增长率、收入增长率）
#营运：（总资产周转率、应收账款周转率）
#偿债：（资产负债率、有息负债率）
#现金：（收现率、净现率）

# coding=utf-8
import numpy as np
import pandas as pd
import plotly_express as px
import plotly.graph_objs as go
import plotly.offline as pyoff
from dash import Dash, Input, Output, ctx, html, dcc

code='002236'
df=pd.read_excel(Fr'C:\xyzy\1lhjr\5gsfx\tzsj\{code}.xlsx')

trace1 = go.Scatter(x=df.年份,y=df.净资产收益率,xaxis='x1',yaxis='y1',name='净资产收益率')
trace2 = go.Scatter(x=df.年份,y=df.销售净利率,xaxis='x2',yaxis='y2',name='销售净利率')
trace3 = go.Scatter(x=df.年份,y=df.净利润增长率,xaxis='x3',yaxis='y3',name='净利润增长率')
trace4 = go.Scatter(x=df.年份,y=df.总资产周转率,xaxis='x4',yaxis='y4',name='总资产周转率')
trace5 = go.Scatter(x=df.年份,y=df.资产负债率,xaxis='x5',yaxis='y5',name='资产负债率')
trace6 = go.Scatter(x=df.年份,y=df.收现率,xaxis='x6',yaxis='y6',name='收现率')
trace7 = go.Scatter(x=df.日期,y=df.市净率,xaxis='x7',yaxis='y7',name='市净率')
trace8 = go.Scatter(x=df.日期,y=df.股价,xaxis='x8',yaxis='y8',name='股价')
#trace9 = go.Scatter(x=df.iloc[:,1][-750:],y=df.iloc[:,3][-750:],xaxis='x9',yaxis='y9',name='近三年价格')

data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8]
layout = go.Layout(
    xaxis=dict(
        domain=[0, 0.32]
    ),
    yaxis=dict(
        domain=[0.67, 1]
    ),
    xaxis2=dict(
        domain=[0, 0.32],
        anchor='y2',
    ),
    yaxis2=dict(
        domain=[0.34, 0.65],
        anchor='x2'
    ),
    xaxis3=dict(
        domain=[0, 0.32],
        anchor='y3',    
    ),
    yaxis3=dict(
        domain=[0, 0.32],
        anchor='x3'
    ),
    xaxis4=dict(
        domain=[0.34, 0.65]
    ),
    yaxis4=dict(
        domain=[0.67, 1],
        anchor='x4'
    ),
    xaxis5=dict(
        domain=[0.34, 0.65],
        anchor='y5',
    ),
    yaxis5=dict(
        domain=[0.34, 0.65],
        anchor='x5'
    ),
    xaxis6=dict(
        domain=[0.34, 0.65],
        anchor='y6',    
    ),
    yaxis6=dict(
        domain=[0, 0.32],
        anchor='x6'
    ),
    xaxis7=dict(
        domain=[0.67, 1],
        anchor='y7',
        tickmode='linear',tick0=1,dtick =36,
    ),
    yaxis7=dict(
        domain=[0.67, 1],
        anchor='x7'
    ),
    xaxis8=dict(
        domain=[0.67, 1],
        anchor='y8',
        tickmode='linear',tick0=1,dtick =36,
    ),
    yaxis8=dict(
        domain=[0.34, 0.65],
        anchor='x8'
    ),    
    #xaxis9=dict(
        #domain=[0.67, 1],
        #anchor='y9',
        #tickmode='linear',tick0=1,dtick =24,
    #),
    #yaxis9=dict(
        #domain=[0, 0.32],
        #anchor='x9'
    #),    
    legend=dict(orientation="h",yanchor="bottom",y=1,xanchor="right",x=1),title_font_size=10,font_size=8
)
fig1 = go.Figure(data=data, layout=layout)
fig1.update_layout=layout

fig2 = go.Figure(data=data, layout=layout)
fig2.update_layout=layout

app = Dash(__name__)

app.layout = html.Div([
    html.Button('年度', id='nd'),
    html.Button('季度', id='jd'),
    dcc.Graph(id='graph')
])

@app.callback(
    Output('graph', 'figure'),
    Input('nd', 'n_clicks'),
    Input('jd', 'n_clicks'),
    prevent_initial_call=True
)
def update_graph(b1,b2):
    triggered_id = ctx.triggered_id
    print(triggered_id)
    if triggered_id == 'nd':
         return nd_graph()
    elif triggered_id == 'jd':
         return jd_graph()

def nd_graph():
    return fig1
def jd_graph():
    return fig2

if __name__ == '__main__':
    app.run_server(port=5555)