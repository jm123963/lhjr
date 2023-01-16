import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
from app import app
import plotly.express as px
from dash import dcc
import pandas as pd
import os

def TabCharts():
    return html.Div(
            [
                dbc.Tabs(
                    [
                        dbc.Tab(label="月消费", tab_id="tab-1"),
                        dbc.Tab(label="年消费", tab_id="tab-2"),
                    ],
                    id="tabs",
                    active_tab="tab-1",
                ),
                html.Div([YearChart(), MonthChart(hidden=True)],id="content"),
            ]
        )



def  MonthChart(hidden=False):
    style = {"display": "none"} if hidden else {}
    fig = px.bar()
    return dcc.Graph(figure=fig, id="chart",style = style)


@app.callback(Output("chart", "figure"), [Input("table", "data")])
def update(data):
    df = pd.DataFrame(data)
    data = df.sum().to_list()
    return px.bar(x=df.columns, y=data, range_y=[0, 4000])


def YearChart(hidden=False):
    style = {"display": "none"} if hidden else {}
    total = []
    for f in os.listdir("D:\Download\dash-vs-personal-app-today\data/"):
        df = pd.read_excel(f"D:\Download\dash-vs-personal-app-today\data/{f}")
        month_total = sum(df.sum().to_list())
        total.append(month_total)
    fig = px.bar(x=[f"{i}月" for i in range(1, 13)], y=total, range_y=[0, 9000])
    return dcc.Graph(figure=fig, id="year-chart",style = style)


@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return html.Div([MonthChart(), YearChart(hidden=True)])
    elif at == "tab-2":
        return html.Div([YearChart(), MonthChart(hidden=True)])
    return html.P("This shouldn't ever be displayed...")

# def TabCharts():
#     return html.Div(
#         [
#             dbc.Tabs(
#                 [
#                     dbc.Tab(label="月消费", tab_id="tab-1"),
#                     dbc.Tab(label="年消费", tab_id="tab-2"),
#                 ],
#                 id="tabs",
#                 active_tab="tab-1",
#             ),
#             html.Div([YearChart(), MonthChart(hidden=True)], id="content"),
#         ]
#     )


# def MonthChart(hidden=False):
#     style = {"display": "none"} if hidden else {}
#     fig = px.bar()
#     return dcc.Graph(figure=fig, id="chart", style=style)
#
#
# def YearChart(hidden=False):
#     style = {"display": "none"} if hidden else {}
#     total = []
#     for f in os.listdir("data/"):
#         df = pd.read_excel(f"data/{f}")
#         month_total = sum(df.sum().to_list())
#         total.append(month_total)
#     fig = px.bar(x=[f"{i}月" for i in range(1, 13)], y=total, range_y=[0, 9000])
#     return dcc.Graph(figure=fig, id="year-chart", style=style)
#
#
# @app.callback(Output("chart", "figure"), [Input("table", "data")])
# def update(data):
#     df = pd.DataFrame(data)
#     data = df.sum().to_list()
#     return px.bar(x=df.columns, y=data, range_y=[0, 4000])
#
#
# @app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
# def switch_tab(at):
#     if at == "tab-1":
#         # return MonthChart()
#         return html.Div([MonthChart(), YearChart(hidden=True)])
#     elif at == "tab-2":
#         # return YearChart()
#         return html.Div([YearChart(), MonthChart(hidden=True)])
#     return html.P("This shouldn't ever be displayed...")
