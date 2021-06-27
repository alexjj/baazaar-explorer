import dash_core_components as dcc
from dash_core_components.Graph import Graph
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc

# Import custom data.py
import data

gotchi_sales = data.gotchi_sales

# Layout for Gotchi page

gotchiLayout = html.Div(
    [
        dbc.Row(dbc.Col(html.H2(children="What does base rarity (BRS) cost?"))),
        # Scatter of BRS vs price
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='price-chart',
                    config={"displayModeBar": False},
                    figure={
                        'data': [
                            {
                                "x": gotchi_sales['BRS'],
                                "y": gotchi_sales['Price (GHST)'],
                                'text': gotchi_sales['Name'],
                                "type": "scatter",
                                'mode': 'markers',
                                'hoverinfo': 'x+y+text',
                                'hovertemplate': 'BRS: %{x}<br>GHST: %{y}'
                                                    "<extra>%{text}</extra>",
                            }
                        ],
                        'layout': {
                            'title': 'Cost by Rarity',
                            "hovermode": "closest",
                            'yaxis': {
                                'title': 'GHST (log scale)',
                                'type': 'log',
                            }
                            },
                    },
                )
            )
        ),
        dbc.Row(
            dbc.Col(children=[
                html.H2(children="Value over time"),
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
                    figure={
                        'data': [
                            {
                                "x": gotchi_sales['Date'],
                                "y": gotchi_sales['Value'],
                                "type": "lines",
                            }
                        ],
                        'layout': {
                            "title": "Cost efficiency of Gotchis",

                        'yaxis': {
                            'title': 'BRS/GHST',
                            'range': [0, 2],
                            },
                        "colorway": ["#17B897"],
                        },
                    },
                )
            )
        ),
    ],
)