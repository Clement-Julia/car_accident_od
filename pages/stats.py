import dash
from dash import html

dash.register_page(__name__, path="/stats")

layout = html.Div([
    html.H3("Statistiques générales"),
    html.P("Cette section affichera des chiffres clés : nombre d'accidents, blessés, mortalité, etc.")
])
