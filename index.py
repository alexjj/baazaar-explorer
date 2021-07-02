import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import server 
from app import app
from apps import gotchi, tickets, wearables

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

# Temporary home page
markdown_text = '''
## Welcome to the Baazaar Explorer

This is very much a 🚧work in progress🚧. Mostly getting the basics setup.

Have a look at [gotchis](/gotchis) and [tickets](/tickets) to get an idea.

I've got a few more figures and tables I want to include with the data you can get 
from [thegraph](https://thegraph.com/explorer/subgraph/aavegotchi/aavegotchi-core-matic). TheGraph does have some limitations which I hadn't realised but will come to those later.

Feel free to drop me an email hi @ aavagotchi.fyi with any suggestions. Code is on [github](https://github.com/alexjj/baazaar-explorer).

![fren](/assets/fren.png)

'''


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
        return dcc.Markdown(children=markdown_text)
    elif pathname.endswith("/gotchis"):
        return gotchi.layout
    elif pathname.endswith("/wearables"):
        return wearables.layout
    elif pathname.endswith("/tickets"):
        return tickets.layout
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
