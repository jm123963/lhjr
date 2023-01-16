
from app import app
import dash_bootstrap_components as dbc
from sidebar import SideBar
from table import PersonalTable
from tabarchart import TabCharts
from infocards import InfoCards


app.layout = dbc.Row(
    [
        dbc.Col([SideBar()],className='bg-dark',width=3),
        dbc.Col([InfoCards(),TabCharts(),PersonalTable()],width=9)
    ],className='vh-100'
)
app.run_server(debug=True)













# import dash_bootstrap_components as dbc
# from table import PersonalTable
#
# # from barchart import BarChart
# from tabarchart import TabCharts
# from sidebar import SideBar
# from infocards import InfoCards
#
# app.layout = dbc.Row(
#     [
#         dbc.Col([SideBar()], className="bg-dark", width=3),  # sidebar
#         dbc.Col([InfoCards(),TabCharts(), PersonalTable()], width=9),  # content
#     ],
#     className="vh-100",
# )
# app.run_server(debug=True)
