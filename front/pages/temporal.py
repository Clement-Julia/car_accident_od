import dash
from dash import html, dcc
from back.temporal_graphs import *
import pandas as pd
import os

dash.register_page(__name__, path="/temporal")

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
df = pd.read_csv(os.path.join(base_path, "data", "dataset_simplify.csv"), dtype=str)

df = load_temporal_data(df)

layout = html.Div([
    html.H3("Analyse temporelle des accidents"),

    html.Div(dcc.Graph(figure=plot_tendance_annuelle(df)), className="card-dark"),
    html.Div(dcc.Graph(figure=plot_accidents_mois(df)), className="card-dark"),
    html.Div(dcc.Graph(figure=plot_accidents_jour(df)), className="card-dark"),
    html.Div(dcc.Graph(figure=plot_accidents_heure(df)), className="card-dark"),
    html.Div(dcc.Graph(figure=plot_age_annee(df)), className="card-dark"),
    html.Div(dcc.Graph(figure=plot_heatmap_jour_heure(df)), className="card-dark"),
    html.Div(dcc.Graph(figure=plot_gravite_annee(df)), className="card-dark"),
    html.Div(dcc.Graph(figure=plot_accidents_heure_gravite(df)), className="card-dark"),
    html.Div(dcc.Graph(figure=plot_accidents_jour_catr(df)), className="card-dark"),
])
