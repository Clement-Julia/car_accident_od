import dash
from dash import html, dcc, callback, Output, Input
from back.temporal_graphs import *
import pandas as pd
import os
from utils.helpers import accordion_stats
from utils.data_loader import get_data

dash.register_page(__name__, name="Stats temporelles", path="/temporal")
df = get_data()

layout = html.Div([
    html.H3("Analyse temporelle des accidents", className="title-main"),

    html.Div([
        html.Label("Sélectionnez une vue :", className="radio-title"),
        dcc.RadioItems(
            id="mode-temporal",
            options=[
                {"label": "Data temporelles", "value": "vue1"},
                {"label": "Data temporelles croisées", "value": "vue2"},
            ],
            value="vue1",
            className="radio-switch",
            labelStyle={"marginRight": "30px"},
        )
    ], className="radio-container"),

    html.Div(id="contenu-graphiques-temporaux")
])


@callback(
    Output("contenu-graphiques-temporaux", "children"),
    Input("mode-temporal", "value")
)
def update_graphs(mode):
    if mode == "vue1":
        return [
            html.Div(dcc.Graph(figure=plot_tendance_annuelle(df)), className="card-dark"),
            html.Div(dcc.Graph(figure=plot_accidents_mois(df)), className="card-dark"),
            html.Div(dcc.Graph(figure=plot_accidents_jour(df)), className="card-dark"),
            html.Div(dcc.Graph(figure=plot_accidents_heure(df)), className="card-dark"),
        ]
    else:
        return [
            html.Div([
                dcc.Graph(figure=plot_age_annee(df)),
                accordion_stats("Répartition des tranches d’âge par année", age_annee_stats(df))
            ], className="card-dark"),

            html.Div([
                dcc.Graph(figure=plot_heatmap_jour_heure(df)),
                accordion_stats("Top 10 des plages horaires d'accidents", stats_top_zones_temporelles(df), is_percent=False)
            ], className="card-dark"),

            html.Div([
                dcc.Graph(figure=plot_gravite_annee(df)),
                accordion_stats("Répartition des blessures selon les années en pourcentage", stats_gravite_annee(df), is_percent=True),
            ], className="card-dark"),  

            html.Div(dcc.Graph(figure=plot_accidents_heure_gravite(df)), className="card-dark"),
            html.Div(dcc.Graph(figure=plot_accidents_jour_catr(df)), className="card-dark"),
        ]
