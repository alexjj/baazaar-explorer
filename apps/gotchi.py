import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import data
import pandas as pd
import plotly.express as px
import plotly.io as pio
from dash_core_components.Graph import Graph

gotchi_sales = data.gotchi_sales

pio.templates.default = "plotly_white"

# Figures

brs_vs_log_price_scatter = px.scatter(
    gotchi_sales,
    x='BRS',
    y='Price (GHST)',
    color='Has Wearables',
    hover_name='Name',
    log_y=True,
    title='Cost by Rarity',
    labels={'Price (GHST)': 'GHST (log scale)'})

#04B7BC

value_over_time_line = px.line(
    gotchi_sales, 
    x='Date', 
    y='Value', 
    title='Cost efficiency of Gotchis',
    hover_name='Name',
    labels={'Value': 'Value (BRS/GHST)'},
    range_y=[0, 2])

value_over_time_histogram = px.histogram(
    gotchi_sales,
    x='Date',
    y='Value',
    title='Daily Average BRS/GHST',
    histfunc="avg",
    range_y=[0, 2],
    color_discrete_sequence=['#FA34F3']
)
value_over_time_histogram.update_traces(xbins_size="D1")
value_over_time_histogram.update_layout(bargap=0.1)
value_over_time_histogram.update_layout(yaxis_title_text='Value (BRS/GHST)')

sales_per_day = px.histogram(
    gotchi_sales,
    x='Date',
    title='Daily Gotchi Sales',
)
sales_per_day.update_traces(xbins_size="D1")
sales_per_day.update_layout(bargap=0.1)
sales_per_day.update_layout(yaxis_title_text='Number of Sales')



layout = html.Div(
    [
        dbc.Row(
            dbc.Col(children=[
                html.H2(children="Aavegotchi Sales"),
                html.P(children=['Looking back over ', '{:,.0f}'.format(gotchi_sales.shape[0]), ' gotchis sold.' , ' Totalling ', '{:,.0f}'.format(gotchi_sales['Price (GHST)'].sum()), ' GHST.']),
                ]
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='daily-sales',
                    config={'displayModeBar': False},
                    figure=sales_per_day
                ),
            )
        ),
        dbc.Row(
            dbc.Col(children=
                [dcc.Graph(
                    id='price-chart',
                    config={"displayModeBar": False},
                    figure=brs_vs_log_price_scatter
                ),]
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='value-chart-daily',
                    config={'displayModeBar': False},
                    figure=value_over_time_histogram
                ),
            )
        ),
    ],
)
