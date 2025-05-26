import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

layout = dbc.Container([
    html.H2("Bienvenue sur l'observatoire des accidents de la route en France"),
    html.P("""
        Cette application permet d'explorer les données d'accidents de la route entre 2019 et 2023. 
        Vous y trouverez des statistiques, des visualisations interactives et un outil de prédiction.
    """),
    html.Hr(),
    html.H4("Navigation rapide :"),
    dbc.ListGroup([
        dbc.ListGroupItem("Statistiques générales", href="/stats", action=True)
    ]),
])
