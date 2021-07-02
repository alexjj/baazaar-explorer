import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import data
import pandas as pd
import plotly.express as px
import plotly.io as pio
from dash_core_components.Graph import Graph

pio.templates.default = "plotly_white"

wearables_sales = data.wearable_sales

# Plots:
# Quanitiy of wearables sold per day by slot
# Quantity of wearables sold per day by rarity
# GHST total of wearables sold by rarity
# GHST of total of wearables sold by slot
#

wearables_sales_by_slot = px.histogram(
    wearables_sales,
    x='Date',
    y='Quantity',
    title='Total Wearables Volume by Slot',
    color='Slot',
    histfunc='sum',
)

wearables_sales_by_slot.update_traces(xbins_size="D1")
wearables_sales_by_slot.update_layout(bargap=0.1)
wearables_sales_by_slot.update_layout(yaxis_title_text='Wearables Sold')


wearables_sales_by_rarity = px.histogram(
    wearables_sales,
    x='Date',
    y='Quantity',
    title='Total Wearables Volume by Rarity',
    color='Rarity',
    histfunc='sum',
)

wearables_sales_by_rarity.update_traces(xbins_size="D1")
wearables_sales_by_rarity.update_layout(bargap=0.1)
wearables_sales_by_rarity.update_layout(yaxis_title_text='Wearables Sold')


wearables_ghst_by_slot = px.histogram(
    wearables_sales,
    x='Date',
    y='Total Purchase (GHST)',
    title='Total Wearables Sales by Slot',
    color='Slot',
    histfunc='sum',
)

wearables_ghst_by_slot.update_traces(xbins_size="D1")
wearables_ghst_by_slot.update_layout(bargap=0.1)
wearables_ghst_by_slot.update_layout(yaxis_title_text='GHST')


wearables_ghst_by_rarity = px.histogram(
    wearables_sales,
    x='Date',
    y='Total Purchase (GHST)',
    title='Total Wearables Sales by Rarity',
    color='Rarity',
    histfunc='sum',
)

wearables_ghst_by_rarity.update_traces(xbins_size="D1")
wearables_ghst_by_rarity.update_layout(bargap=0.1)
wearables_ghst_by_rarity.update_layout(yaxis_title_text='GHST')


layout = html.Div(
    [
        dbc.Row(
            dbc.Col(children=[
                html.H2(children="Wearables Sales"),
                html.P(children=['Looking back over ', '{:,.0f}'.format(wearables_sales['Quantity'].sum()), ' wearables sold.' , ' Totalling ', '{:,.0f}'.format(wearables_sales['Total Purchase (GHST)'].sum()), ' GHST.']),
                ]
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='sale-slot-daily',
                    config={'displayModeBar': False},
                    figure=wearables_sales_by_slot
                ),
            )
        ),
        dbc.Row(
            dbc.Col(children=
                [dcc.Graph(
                    id='sales-rarity-daily',
                    config={"displayModeBar": False},
                    figure=wearables_sales_by_rarity
                ),]
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='ghst-slot-daily',
                    config={'displayModeBar': False},
                    figure=wearables_ghst_by_slot
                ),
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='ghst-rarity-daily',
                    config={'displayModeBar': False},
                    figure=wearables_ghst_by_rarity
                ),
            )
        ),
    ],
)