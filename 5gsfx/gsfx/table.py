import pandas as pd
from dash import Dash, Input, Output, ctx, html, dcc, dash_table
import os
from app import app

def PersonalTable():
    df = pd.read_excel(r"C:\xyzy\1lhjr\5gsfx\gsfx\data/002415.xlsx")
    return html.Div(
        [
            dcc.Dropdown(
                id="dpd",
                options=[{"label": f[:-5], "value": f} for f in os.listdir(r"C:\xyzy\1lhjr\5gsfx\gsfx\data")],
                value="002415.xlsx"
            ),
            dash_table.DataTable(id='table',
                              data=df.to_dict("records"),
                              page_size=12,
                              columns=[{"id": i, "name": i} for i in df.columns]
            )
        ]
        , className='shadow'
    )
#
@app.callback(Output('table','data'),[Input('dpd','value')])
def update(v):
    return pd.read_excel(Fr"C:\xyzy\1lhjr\5gsfx\gsfx\data/{v}").to_dict("records")
