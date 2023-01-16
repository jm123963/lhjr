from dash import dcc
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd
from app import app


def BarChart():
    fig = px.bar()
    return dcc.Graph(figure=fig, id="chart")


@app.callback(Output("chart", "figure"), [Input("table", "data")])
def update(data):
    df = pd.DataFrame(data)
    data = df.sum().to_list()
    return px.bar(x=df.end_date, y=data)

