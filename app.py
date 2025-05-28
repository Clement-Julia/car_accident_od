import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, pages_folder="front/pages", external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

header = dbc.Navbar(
    dbc.Container([
        html.Div("Accidents de la route en France (2019–2023)", className="navbar-title"),
        dbc.Nav(
            [
                dbc.NavItem(
                    dcc.Link(
                        page["name"],
                        href=page["relative_path"],
                        className="navbar-link"
                    )
                )
                for page in dash.page_registry.values()
            ],
            className="navbar-nav"
        ),
    ]),
    className="navbar-container"
)

app.layout = dbc.Container([
    header,
    html.Br(),
    dash.page_container
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)