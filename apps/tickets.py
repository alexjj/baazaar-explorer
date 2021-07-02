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

ticket_sales = data.ticket_sales
frens_per_ticket = data.frens_per_ticket

ticket_sales['FRENS'] = ticket_sales['Type'].replace(frens_per_ticket, regex=True).astype(float)
ticket_sales['GHST/FREN'] = ticket_sales['Price per Ticket (GHST)'] / ticket_sales['FRENS']

# Figures

# Price over time by type and daily total sold and daily GHST spent
# best FRENS/GHST rewards - box to enter your FRENS total?

price_vs_time_by_type = px.line(
    ticket_sales,
    x='Date',
    y='Price per Ticket (GHST)',
    color='Type',
    title='Price per Ticket'
)

frens_vs_time_by_type = px.line(
    ticket_sales,
    x='Date',
    y='GHST/FREN',
    color='Type',
    title='Amount of GHST per FREN you can make by ticket type',
    range_y=[0, 0.0025]
)

frens_vs_time_by_type.update_xaxes(rangeslider_visible=True)

tickets_per_day = px.histogram(
    ticket_sales,
    x='Date',
    y='Quantity',
    title='Total Ticket Volume',
    histfunc='sum',
    color='Type',
    #color_discrete_sequence=['#FA34F3']
)
tickets_per_day.update_traces(xbins_size="D1")
tickets_per_day.update_layout(bargap=0.1)
tickets_per_day.update_layout(yaxis_title_text='Tickets Sold')

ghst_per_day = px.histogram(
    ticket_sales,
    x='Date',
    y='Total Purchase (GHST)',
    title='Total Ticket Sales',
    histfunc='sum',
    color='Type',
    #color_discrete_sequence=['#04B7BC']
)
ghst_per_day.update_traces(xbins_size="D1")
ghst_per_day.update_layout(bargap=0.1)
ghst_per_day.update_layout(yaxis_title_text='Sales (GHST)')


layout = html.Div(
    [
        dbc.Row(
            dbc.Col(children=[
                html.H2(children="Raffle Ticket Sales"),
                html.P(children=['Looking back over ', '{:,.0f}'.format(ticket_sales.shape[0]), ' ticket transaction.' , ' Totalling ', '{:,.0f}'.format(ticket_sales['Total Purchase (GHST)'].sum()), ' GHST.']),
                ]
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='price-chart',
                    config={'displayModeBar': False},
                    figure=price_vs_time_by_type
                ),
            )
        ),
        dbc.Row(
            dbc.Col(children=
                [dcc.Graph(
                    id='frens-chart',
                    config={"displayModeBar": False},
                    figure=frens_vs_time_by_type
                ),]
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='volume-daily',
                    config={'displayModeBar': False},
                    figure=tickets_per_day
                ),
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='sales-daily',
                    config={'displayModeBar': False},
                    figure=ghst_per_day
                ),
            )
        ),
    ],
)