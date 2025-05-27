import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, pages_folder="front/pages", external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    html.H1("Accidents de la route en France (2019–2023)"),
    html.Hr(),
    dbc.Nav([
        dbc.NavLink("Accueil", href="/", active="exact"),
        dbc.NavLink("Statistiques", href="/stats", active="exact"),
        dbc.NavLink("Analyse temporelle", href="/temporal", active="exact"),
    ], pills=True),
    dash.page_container
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)
