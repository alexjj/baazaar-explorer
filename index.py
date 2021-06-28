import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import server 
from app import app
from apps import gotchi

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Gotchis", href="/gotchis", active="exact")),
        dbc.NavItem(dbc.NavLink("Wearables", href="/wearables", active="exact")),
        dbc.NavItem(dbc.NavLink("Tickets", href="/tickets", active="exact")),
        dbc.NavItem(dbc.NavLink("More Stats", href="/stats", active="exact")),
    ],
    brand="👻 Baazaar Explorer",
    brand_href="/",
    sticky="top",
    color="#FA34F3",
    dark=True,
    style={'margin-bottom': '1em'},
)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    dbc.Container(html.Div(id='page-content'))
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname in ["/"]:
        return "🚧 WIP!"
    elif pathname.endswith("/gotchis"):
        return gotchi.layout
    elif pathname.endswith("/wearables"):
        return "🚧 WIP!"
    elif pathname.endswith("/tickets"):
        return "🚧 WIP!"
    elif pathname.endswith("/stats"):
        return "🚧 WIP!"
    else:
        return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

# Call app server
if __name__ == "__main__":
    # set debug to false when deploying app
    app.run_server(debug=True)
