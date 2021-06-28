import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
# Import custom data.py
import data
import pandas as pd
import plotly.express as px
import plotly.io as pio
from dash_core_components.Graph import Graph

gotchi_sales = data.gotchi_sales

# Layout for Gotchi page
pio.templates.default = "plotly_white"


layout = html.Div(
    [
        dbc.Row(
            dbc.Col(children=[
                html.H2(children="Aavegotchi Sales"),
                html.P(children=['Looking back over ', '{:,.0f}'.format(gotchi_sales.shape[0]), ' gotchis sold.' , ' Totalling ', '{:,.0f}'.format(gotchi_sales['Price (GHST)'].sum()), ' GHST.']),
                ]
            )
        ),
        # Scatter of BRS vs price
        dbc.Row(
            dbc.Col(children=
                [dcc.Graph(
                    id='price-chart',
                    config={"displayModeBar": False},
                    figure=px.scatter(
                        gotchi_sales,
                        x='BRS',
                        y='Price (GHST)',
                        color='Has Wearables',
                        hover_name='Name',
                        log_y=True,
                        title='Cost by Rarity',
                        labels={'Price (GHST)': 'GHST (log scale)'},
                    )
                ),
                html.P(children=['Naked means without wearables currently.'])]
            )
        ),
        dbc.Row(
            dbc.Col(children=[
                html.H3(children="Value over time"),
                html.P(children='The bigger the value the better the deal.'
                ' Lower values suggests more demand and/or less supply')
            ]
            )
        ),
        # Line of BRS vs price
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='value-chart',
                    config={'displayModeBar': False},
                    figure=px.line(
                        gotchi_sales, 
                        x='Date', 
                        y='Value', 
                        title='Cost efficiency of Gotchis',
                        hover_name='Name',
                        labels={'Value': 'Value (BRS/GHST)'},
                        range_y=[0, 2])
                ),
            )
        )
    ],
)
