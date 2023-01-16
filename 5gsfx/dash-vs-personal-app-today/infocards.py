import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
from app import app

def Card(name,cost,color='bg-warning'):
    return html.Div([
                        html.H6(name),
                        html.Hr(),
                        html.H1(cost,id=name)
                    ],className=f'{color} shadow text-white p-3 rounded'
    )

def InfoCards():
    return dbc.Row(
            [
                dbc.Col(Card('月度消费','---')),
                dbc.Col(Card('季度消费','---',color='bg-primary')),
                dbc.Col(Card('年度消费','---',color='bg-info'))
            ]
        ,className='py-4'
        )

@app.callback(
    output=[
        Output("月度消费", "children"),
        Output("季度消费", "children"),
        Output("年度消费", "children"),
    ],
    inputs=[Input("year-chart", "figure"), Input("dpd", "value")])
def update(fig,cur_table):
    data = fig["data"][0]["y"]
    print(data)
    cur_month = int(cur_table[:-8])
    cur_month_index = cur_month - 1
    cur_month_cost = data[cur_month_index]
    cur_season_cost = None
    cur_year_cost = sum(data)

    season_table = {
        "第一季度": [1, 2, 3],
        "第二季度": [4, 5, 6],
        "第三季度": [7, 8, 9],
        "第四季度": [10, 11, 12],
    }
    for s in season_table.values():
        if cur_month in s:
            a, b, c = s
            cur_season_cost = data[a - 1] + data[b - 1] + data[c - 1]

    return cur_month_cost, cur_season_cost, cur_year_cost



# def Card(name, cost, color="bg-primary"):
#     return html.Div(
#         [html.H6(name), html.Hr(), html.H1(cost, id=name)],
#         className=f"{color} shadow text-white p-3 rounded",
#     )
#
#
# def InfoCards():
#     return dbc.Row(
#         [
#             dbc.Col(Card("本月花销", "---", color="bg-info")),
#             dbc.Col(Card("季度花销", "---", color="bg-warning")),
#             dbc.Col(Card("年度花销", "---")),
#         ],
#         className="py-4",
#     )
#
#
# @app.callback(
#     output=[
#         Output("本月花销", "children"),
#         Output("季度花销", "children"),
#         Output("年度花销", "children"),
#     ],
#     inputs=[Input("year-chart", "figure"), Input("dpd", "value")],
# )
# def fill_cost(fig, cur_table):
#     data = fig["data"][0]["y"]
#     print(cur_table)
#     print(data)
#     cur_month = int(cur_table[:-8])
#     cur_month_index = cur_month - 1
#     cur_month_cost = data[cur_month_index]
#     cur_season_cost = None
#     cur_year_cost = sum(data)
#
#     season_table = {
#         "第一季度": [1, 2, 3],
#         "第二季度": [4, 5, 6],
#         "第三季度": [7, 8, 9],
#         "第四季度": [10, 11, 12],
#     }
#     for s in season_table.values():
#         if cur_month in s:
#             a, b, c = s
#             cur_season_cost = data[a - 1] + data[b - 1] + data[c - 1]
#
#     return cur_month_cost, cur_season_cost, cur_year_cost
