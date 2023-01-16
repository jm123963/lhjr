

from dash import dash_table
from dash import html
import pandas as pd
from dash import dcc
from app import app
from dash.dependencies import Output,Input
import os

def PersonalTable():
    df = pd.read_excel("C:\xyzy\1lhjr\5gsfx\gsfx\data/002415.xlsx")
    return html.Div(
        [
            dcc.Dropdown(
                id="dpd",
                options=[{"label": f[:-5], "value": f} for f in os.listdir("C:\xyzy\1lhjr\5gsfx\gsfx\data")],
                value="002415.xlsx",
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
    return pd.read_excel(f"C:\xyzy\1lhjr\5gsfx\gsfx\data/{v}").to_dict("records")






# import dash_table
# import dash_html_components as html
# import dash_core_components as dcc
# from dash.dependencies import Output, Input
# import pandas as pd
# from app import app
# import os
#
# def PersonalTable():
#     df = pd.read_excel("data/1月账单.xlsx")
#     return html.Div(
#         [
#             dcc.Dropdown(
#                 id="dpd",
#                 options=[{"label": f[:-5], "value": f} for f in os.listdir("data")],
#                 value="1月账单.xlsx",
#             ),
#             # 1月账单.xlsx
#             # 12月账单.xlsx
#             dash_table.DataTable(
#                 id="table",
#                 data=df.to_dict("records"),
#                 page_size=12,
#                 columns=[{"id": i, "name": i} for i in df.columns],
#             ),
#         ],
#         className="shadow",
#     )
#
#
# @app.callback(Output("table", "data"), [Input("dpd", "value")])
# def update(v):
#     return pd.read_excel(f"data/{v}").to_dict("records")
