import dash_bootstrap_components as dbc

# Navigation Bar function
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/

def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Gotchis", href="/gotchis", active="exact")),
            dbc.NavItem(dbc.NavLink("Wearables", href="/wearables", active="exact")),
            dbc.NavItem(dbc.NavLink("Tickets", href="/tickets", active="exact")),
            dbc.NavItem(dbc.NavLink("More Stats", href="/stats", active="exact")),
        ],
        brand="Home",
        brand_href="/",
        sticky="top",
        color="primary",
        dark=True,
        expand='lg',
    )
    return navbar