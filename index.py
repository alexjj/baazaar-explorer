import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from app import server

from layouts import gotchiLayout
import callbacks
from navbar import Navbar

# All pages layout: Navbar plus Title Header and Content put in a container
nav = Navbar()

# not sure if I want this on all pages?
header = dbc.Row(
    dbc.Col(
        html.Div(
            [
                html.H1(children="👻 Aavegotchi Baazaar Explorer 🔭"),
            ]
        )
    ),
    className="banner",
)

content = html.Div([dcc.Location(id="url"), html.Div(id="page-content")])

container = dbc.Container([header, content])

# Menu callback, set and return
# Declair function that connects other pages with content to container
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname in ["/"]:
        return html.Div(
            [
                dcc.Markdown(
                    """
            This is currently acting as the home page when you arrive. Maybe later move it to it's own layout for the 
            high level stats. 🚧 WIP!
            
            ### Gotchi
            Analyse historical sales and compare to current listings. Eventually have a price prediction for your gotchi.

            ### Wearables
            Past and current wearables, look up specific ones

            ### Tickets
            Prices of tickets over time

            ### Stats
            More stats about the Aavegotchi universe - total value of gotchi and items etc.

        """
                )
            ],
            className="home",
        )
    elif pathname.endswith("/gotchis"):
        return gotchiLayout
    elif pathname.endswith("/wearables"):
        return "🚧 WIP!"
    elif pathname.endswith("/tickets"):
        return "🚧 WIP!"
    elif pathname.endswith("/stas"):
        return "🚧 WIP!"
    else:
        return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

# Main index function that will call and return all layout variables
def index():
    layout = html.Div([nav, container])
    return layout


# Set layout to index function
app.layout = index()

# Call app server
if __name__ == "__main__":
    # set debug to false when deploying app
    app.run_server(debug=False)