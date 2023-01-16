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
    return dcc.Graph(figure=fig, id="chart1",style = style)


@app.callback(Output("chart", "figure"), [Input("table", "data")])
def update(data):
    df = pd.DataFrame(data)
    data = df.sum().to_list()
    return px.bar(x=df.end_date, y=data)


def YearChart(hidden=False):
    style = {"display": "none"} if hidden else {}
    fig = px.bar()
    return dcc.Graph(figure=fig, id="chart2",style = style)


@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return html.Div([MonthChart(), YearChart(hidden=True)])
    elif at == "tab-2":
        return html.Div([YearChart(), MonthChart(hidden=True)])
    return html.P("This shouldn't ever be displayed...")
