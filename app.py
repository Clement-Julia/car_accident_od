import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    html.H1("Accidents de la route en France (2019–2023)"),
    dash.page_container
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)