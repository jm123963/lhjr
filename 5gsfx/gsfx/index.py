from app import app
import dash_bootstrap_components as dbc
from table import PersonalTable
from tabarchart import TabCharts

app.layout = dbc.Row(
    [
        dbc.Col([TabCharts(),PersonalTable()],width=12)
    ],className='vh-100'
)
app.run_server(debug=True)

