import dash
import dash_leaflet as dl
from dash import html, dcc, Input, Output
import sqlite3
import os
import pandas as pd
import requests

dash.register_page(__name__, name="Statistiques", path="/statistique")

API_URL = "http://localhost:5001"  # ou ton IP réelle si distribué

def get_vehicule_types():
    r = requests.get(f"{API_URL}/vehicule-types")
    return r.json()
def get_grav_accident():
    r = requests.get(f"{API_URL}/grav-types")
    return r.json()

def get_filtered_points(catv,grav_type, start_year, end_year):
    params = {"catv": catv,"grav": grav_type, "start": start_year, "end": end_year}
    r = requests.get(f"{API_URL}/points", params=params)
    return r.json()



# Layout initial de la page
layout = html.Div([
    html.H2("Exploration des statistiques"),
    dcc.Dropdown(
        id="section_selector",
        options=[
            {"label": "Cartographie", "value": "carto"},
            {"label": "Statistiques météo", "value": "meteo"},
            {"label": "Statistiques temporelles", "value": "temporal"},
            {"label": "Autres statistiques", "value": "autres"}
        ],
        value="meteo",
        clearable=False,
        style={"width": "300px", "marginBottom": "20px"}
    ),
    html.Div(id="section_content")
])

# Callback pour afficher la section choisie
@dash.callback(
    Output("section_content", "children"),
    Input("section_selector", "value")
)
def update_section(selected_section):
    if selected_section == "meteo":
        return html.Div([
            html.H4("Section : Statistiques météo"),
            html.P("Ici se trouveront les graphiques interactifs liés à la météo.")
        ])
    elif selected_section == "autres":
        return html.Div([
            html.H4("Section : Autres statistiques"),
            html.P("Ici se trouveront d'autres indicateurs.")
        ])
    elif selected_section == "temporal":
        return html.Div([
            html.H4("Section : Statistiques temporelles"),
            html.P("Ici se trouveront les graphiques interactifs liés au temps.")
        ])
    elif selected_section == "carto":
        # Prépare le dropdown avec les différents types de véhicules
        vehicule_types = get_vehicule_types()
        vehicule_dropdown = html.Div([
            html.Label("Filtrer par type de véhicule (catv) :"),
            dcc.Dropdown(
                id="vehicule_selector",
                options=[{"label": v, "value": v} for v in vehicule_types],
                value="",
                placeholder="Sélectionner un type de véhicule",
                className="carto_select"
            )  
        ])
        grav_accident = get_grav_accident()
        grav_dropdown = html.Div([
            html.Label("Filtrer par gravitée d'accident (grav) :"),
            dcc.Dropdown(
                id="grav_selector",
                options=[{"label":grav, "value": grav} for grav in grav_accident],
                value="",
                placeholder="Sélectionner une gravité d'accident",
                className="carto_select"
            )
        ])
        period_range = html.Div([
            html.Label("Période à afficher (années) :"),
            dcc.RangeSlider(
                id='year_range',
                min=2014,
                max=2023,
                step=1,
                value=[2014, 2023],
                marks={year: str(year) for year in range(2014, 2024)},
                tooltip={"placement": "bottom", "always_visible": True},
                allowCross=False
            )
        ])
        # La section Carto intègre le dropdown pour filtrer et la carte avec un groupe de marqueurs
        return html.Div([
            html.H4("Section : Cartographie"),
            html.Div([vehicule_dropdown,grav_dropdown]),
            period_range,
            dl.Map(id="map", center=[46.5, 2.5], zoom=6, children=[
                dl.TileLayer(), 
            dl.GeoJSON(
                id="geojson_cluster",
                cluster=True,
                zoomToBoundsOnClick=True,
                options={"pointToLayer": None}  
            )
            ], style={'width': '100%', 'height': '600px', 'margin': 'auto'})
        ])

@dash.callback(
    Output("geojson_cluster", "data"),
    Input("vehicule_selector", "value"),
    Input("grav_selector", "value"),
    Input("year_range", "value")
)
def update_geojson(selected_type,grav_type, year_range):
    if not selected_type or not year_range:
        return {"type": "FeatureCollection", "features": []}
    
    catv = selected_type if selected_type else "all"
    grav = grav_type if grav_type else "all"

    points = get_filtered_points(catv,grav, year_range[0], year_range[1])

    features = []
    for p in points:
        popup_text = f"""\
            Type : {p['catv']}
            Météo : {p['atm']}
            Collision : {p['col']}
            Chaussée : {p['surf']}
            Manœuvre : {p['manv']}
            Gravité : {p['grav']}"""

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [p["lon"], p["lat"]]
            },
            "properties": {
                "popup": popup_text
            }
        })

    return {"type": "FeatureCollection", "features": features}