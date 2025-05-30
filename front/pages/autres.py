import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import os
from back.autres_graphs import *
from back.vehicule_analysis import *
from utils.helpers import accordion_stats
from utils.data_loader import get_data

dash.register_page(__name__, name="Autres stats", path="/autres")

df = get_data()
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['heure'] = df['date'].dt.hour

layout = html.Div([
    html.H3("Diverses représentations et statistiques pertinentes", className="title-main"),

    html.Div([
        dcc.Graph(figure=age_moyen_gravite(df)),
        accordion_stats("Âge moyen et écart-type par gravité", age_moyen_gravite_stats(df), is_percent=False)
    ], className="card-dark"),  

    html.Div([
        dcc.Graph(figure=gravite_sexe(df)),
        accordion_stats("Pourcentage de gravité par sexe", gravite_sexe_stats(df), is_percent=True)
    ], className="card-dark"),

    html.Div([
        dcc.Graph(figure=gravite_catv(df)),
        accordion_stats("Pourcentage de type de véhicules par gravité", gravite_catv_stats(df), is_percent=True)
    ], className="card-dark"),  

    html.Div([
        dcc.Graph(figure=plot_top_vehicules_graves(df))
    ], className="card-dark"),

    html.Div([
        dcc.Graph(figure=plot_gravite_moyenne_manv(df)),
    ], className="card-dark"),

    html.Div([
        dcc.Graph(figure=plot_nombre_accidents_manv(df)),
        accordion_stats("Nombre d'accidents par manœuvre", stats_nb_accidents_manv(df), is_percent=False)
    ], className="card-dark"),
])