# import dash
# from dash import html

# dash.register_page(__name__, path="/stats")

# layout = html.Div([
#     html.H3("Statistiques générales"),
#     html.P("Cette section affichera des chiffres clés : nombre d'accidents, blessés, mortalité, etc.")
# ])
import dash
import sqlite3
from dash import html, dcc, Output, Input
import dash_leaflet as dl
import pandas as pd
import os
from back.meteo_analysis import plot_gravite_meteo, plot_nombre_accidents_meteo, plot_nombre_accidents_meteo_sans_normale, plot_catr_atm
from utils.helpers import accordion_stats

dash.register_page(__name__, name="Statistiques", path="/statistique")
def load_df():
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(current_dir, "..","..", "data", "dataset_simplify.csv")
    df = pd.read_csv(data_path)
    df_unique = df.drop_duplicates("Num_Acc")

    grav_mapping = {
        'Indemne': 1,
        'Blessé léger': 2,
        'Blessé hospitalisé': 3,
        'Tué': 4
    }
    df['grav_num'] = df['grav'].map(grav_mapping)
    return df, df_unique
def get_vehicule_types():
    db_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "ma_base.db")
    conn = sqlite3.connect(db_path)
    query = "SELECT DISTINCT * FROM donnees_simplifiees"
    df = pd.read_sql_query(query, conn)
    print(df)
    conn.close()
    return df["vehicule_type_majoritaire"].dropna().unique()
df, df_unique = load_df()
layout = html.Div([
    html.H2("Exploration des statistiques"),

    html.Label("Sélectionner une section :"),
    dcc.Dropdown(
        id="section_selector",
        options=[
            {"label": "Statistiques météo", "value": "meteo"},
            {"label": "Cartographie", "value": "carto"},
            {"label": "Autres statistiques", "value": "autres"}
        ],
        value="meteo",
        clearable=False,
        style={"width": "300px", "marginBottom": "20px"}
    ),

    html.Div(id="section_content")
])

@dash.callback(
    Output("section_content", "children"),
    Input("section_selector", "value")
)
def update_section(selected_section):
    if selected_section == "meteo":
        return html.Div([
            html.H4("Section : Statistiques météo"),
            dcc.Graph(figure=plot_gravite_meteo(df.copy())),
            html.Hr(),
            dcc.Graph(figure=plot_nombre_accidents_meteo(df_unique.copy())),
            # accordion_stats("Âge moyen et écart-type par gravité", dcc.Graph(figure=plot_nombre_accidents_meteo_sans_normale(df.copy())), is_percent=False),
            html.Hr(),
            dcc.Graph(figure=plot_nombre_accidents_meteo_sans_normale(df_unique.copy())),
            # accordion_stats("Âge moyen et écart-type par gravité", dcc.Graph(figure=plot_nombre_accidents_meteo_sans_normale(df.copy())), is_percent=False),
            html.Hr(),
            dcc.Graph(figure=plot_catr_atm(df_unique.copy())),
        ])
    elif selected_section == "carto":
        vehicule_types = get_vehicule_types()

        vehicule_dropdown = dcc.Dropdown(
            id="vehicule_selector",
            options=[{"label": v, "value": v} for v in vehicule_types],
            placeholder="Sélectionner un type de véhicule",
            style={"width": "300px", "marginBottom": "20px"}
        )
        return html.Div([
            html.H4("Section : Cartographie"),
            html.Label("Filtrer par type de véhicule :"),
            vehicule_dropdown,
            dl.Map(center=[46.5, 2.5], zoom=6, children=[
                dl.TileLayer()
            ], style={'width': '100%', 'height': '600px', 'margin': 'auto'})
        ])
    elif selected_section == "autres":
        return html.Div([
            html.H4("Section : Autres statistiques")
        ])
