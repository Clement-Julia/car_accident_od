import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/formulaire", name="Saisie de données")

selected_cols = [
    "sexe", "catu", "catv", "atm", "lum", "col", "choc",
    "manv", "plan", "surf", "nbv", "secu1", "infra", "age","place"
]

# Dropdown options
dropdown_options = {
    "sexe": [
        {"label": "Homme", "value": "Homme"},
        {"label": "Femme", "value": "Femme"},
    ],
    "atm": [
        {"label": "Non renseigné", "value": "Non renseigné"},
        {"label": "Normale", "value": "Normale"},
        {"label": "Pluie légère", "value": "Pluie légère"},
        {"label": "Pluie forte", "value": "Pluie forte"},
        {"label": "Neige / grêle", "value": "Neige / grêle"},
        {"label": "Brouillard / fumée", "value": "Brouillard / fumée"},
        {"label": "Vent fort / tempête", "value": "Vent fort / tempête"},
        {"label": "Temps éblouissant", "value": "Temps éblouissant"},
        {"label": "Temps couvert", "value": "Temps couvert"},
        {"label": "Autre", "value": "Autre"}
    ],
    "lum": [
        {"label": "Plein jour", "value": "Plein jour"},
        {"label": "Crépuscule ou aube", "value": "Crépuscule ou aube"},
        {"label": "Nuit sans éclairage public", "value": "Nuit sans éclairage public"},
        {"label": "Nuit avec éclairage non allumé", "value": "Nuit avec éclairage non allumé"},
        {"label": "Nuit avec éclairage allumé", "value": "Nuit avec éclairage allumé"}
    ],
    "catu": [
        {"label": "Conducteur", "value": "Conducteur"},
        {"label": "Passager", "value": "Passager"},
        {"label": "Piéton", "value": "Piéton"}
    ],
    "choc": [
        {"label": "Non renseigné", "value": "Non renseigné"},
        {"label": "Aucun", "value": "Aucun"},
        {"label": "Avant", "value": "Avant"},
        {"label": "Avant droit", "value": "Avant droit"},
        {"label": "Avant gauche", "value": "Avant gauche"},
        {"label": "Arrière", "value": "Arrière"},
        {"label": "Arrière droit", "value": "Arrière droit"},
        {"label": "Arrière gauche", "value": "Arrière gauche"},
        {"label": "Côté droit", "value": "Côté droit"},
        {"label": "Côté gauche", "value": "Côté gauche"},
        {"label": "Chocs multiple", "value": "Chocs multiples / tonneaux"}
    ],
    "plan": [
        {"label": "Non renseigné", "value": "Non renseigné"},
        {"label": "Partie rectiligne", "value": "Partie rectiligne"},
        {"label": "En courbe à gauche", "value": "Courbe à gauche"},
        {"label": "En courbe à droite", "value": "Courbe à droite"},
        {"label": "En S", "value": "En S"}
    ],
    "surf": [
        {"label": "Non renseigné", "value": "Non renseigné"},
        {"label": "Normale", "value": "Normale"},
        {"label": "Mouillé", "value": "Mouillée"},
        {"label": "Flaques", "value": "Flaques"},
        {"label": "Inondée", "value": "Inondée"},
        {"label": "Enneigée", "value": "Enneigée"},
        {"label": "Boue", "value": "Boue"},
        {"label": "Verglacée", "value": "Verglacée"},
        {"label": "Corps gras - huile", "value": "Corps gras / huile"},
        {"label": "Autre", "value": "Autre"}
    ],
    "secu1": [
        {"label": "Non renseigné", "value": "Non renseigné"},
        {"label": "Non renseigné", "value": "Aucun équipement"},
        {"label": "Ceinture", "value": "Ceinture"},
        {"label": "Casque", "value": "Casque"},
        {"label": "Dispositif enfant", "value": "Dispositif enfants"},
        {"label": "Gilet réfléchissant", "value": "Gilet réfléchissant"},
        {"label": "Airbag (2RM/3RM)", "value": "Airbag (2RM/3RM)"},
        {"label": "Gants (2RM/3RM)", "value": "Gants (2RM/3RM)"},
        {"label": "Gants + Airbag (2RM/3RM)", "value": "Gants + Airbag (2RM/3RM)"},
        {"label": "Non déterminable", "value": "Non déterminable"},
        {"label": "Autre", "value": "Autre"}
    ],
    "infra": [
        {"label": "Non renseigné", "value": "Non renseigné"},
        {"label": "Aucun", "value": "Aucun"},
        {"label": "Souterrain - tunnel", "value": "Tunnel"},
        {"label": "Pont - autopont", "value": "Pont"},
        {"label": "Bretelle d’échangeur ou de raccordement", "value": "Bretelle d’échangeur"},
        {"label": "Voie ferrée", "value": "Voie ferrée"},
        {"label": "Carrefour aménagé", "value": "Carrefour aménagé"},
        {"label": "Zone piétonne", "value": "Zone piétonne"},
        {"label": "Zone de péage", "value": "Zone de péage"},
        {"label": "Chantier", "value": "Chantier"},
        {"label": "Autre", "value": "Autre"}
    ],
    "manv": [
        {"label": "Manoeuvre principale avant l’accident : Non renseigné", "value": "Non renseigné"},
        {"label": "Manoeuvre principale avant l’accident : Inconnue", "value": "Inconnue"},
        {"label": "Manoeuvre principale avant l’accident : Sans changement de direction", "value": "Sans changement de direction"},
        {"label": "Manoeuvre principale avant l’accident : Même sens, même file", "value": "Même sens, même file"},
        {"label": "Manoeuvre principale avant l’accident : Entre 2 files", "value": "Entre 2 files"},
        {"label": "Manoeuvre principale avant l’accident : En marche arrière", "value": "En marche arrière"},
        {"label": "Manoeuvre principale avant l’accident : À contresens", "value": "À contresens"},
        {"label": "Manoeuvre principale avant l’accident : Franchissement du terre-plein", "value": "Franchissement du terre-plein"},
        {"label": "Manoeuvre principale avant l’accident : Couloir bus, même sens", "value": "Couloir bus, même sens"},
        {"label": "Manoeuvre principale avant l’accident : Couloir bus, sens inverse", "value": "Couloir bus, sens inverse"},
        {"label": "Manoeuvre principale avant l’accident : Insertion", "value": "Insertion"},
        {"label": "Manoeuvre principale avant l’accident : Demi-tour", "value": "Demi-tour"},
        {"label": "Manoeuvre principale avant l’accident : Changement file à gauche", "value": "Changement file à gauche"},
        {"label": "Manoeuvre principale avant l’accident : Changement file à droite", "value": "Changement file à droite"},
        {"label": "Manoeuvre principale avant l’accident : Déport à gauche", "value": "Déport à gauche"},
        {"label": "Manoeuvre principale avant l’accident : Déport à droite", "value": "Déport à droite"},
        {"label": "Manoeuvre principale avant l’accident : Tourne à gauche", "value": "Tourne à gauche"},
        {"label": "Manoeuvre principale avant l’accident : Tourne à droite", "value": "Tourne à droite"},
        {"label": "Manoeuvre principale avant l’accident : Dépassement gauche", "value": "Dépassement gauche"},
        {"label": "Manoeuvre principale avant l’accident : Dépassement droite", "value": "Dépassement droite"},
        {"label": "Manoeuvre principale avant l’accident : Traverse chaussée", "value": "Traverse chaussée"},
        {"label": "Manoeuvre principale avant l’accident : Stationnement", "value": "Stationnement"},
        {"label": "Manoeuvre principale avant l’accident : Évitement", "value": "Évitement"},
        {"label": "Manoeuvre principale avant l’accident : Ouverture de porte", "value": "Ouverture de porte"},
        {"label": "Manoeuvre principale avant l’accident : Arrêté", "value": "Arrêté"},
        {"label": "Manoeuvre principale avant l’accident : Stationné avec occupants", "value": "Stationné avec occupants"},
        {"label": "Manoeuvre principale avant l’accident : Sur trottoir", "value": "Sur trottoir"},
        {"label": "Manoeuvre principale avant l’accident : Autre", "value": "Autre"}
    ],
    "col": [
        {"label": "Non renseigné", "value": "Non renseigné"},
        {"label": "Deux véhicules - frontale", "value": "Frontale (2 véhicules)"},
        {"label": "Deux véhicules – par l’arrière", "value": "Par l’arrière (2 véhicules)"},
        {"label": "Deux véhicules – par le coté", "value": "Par le côté (2 véhicules)"},
        {"label": "Trois véhicules et plus – en chaîne", "value": "En chaîne (≥3 véhicules)"},
        {"label": "Trois véhicules et plus - collisions multiples", "value": "Collisions multiples (≥3 véhicules)"},
        {"label": "Autre collision", "value": "Autre collision"},
        {"label": "Sans collision", "value": "Sans collision"},

    ],
    "catv": [
        {"label": "Voiture", "value": "Voiture"},
        {"label": "Poids lourd", "value": "Poids lourd"},
        {"label": "Deux-roues motorisé", "value": "Deux-roues motorisé"},
        {"label": "Deux-roues non motorisé", "value": "Deux-roues non motorisé"},
        {"label": "Vélo", "value": "Vélo"},
        {"label": "Trains", "value": "Trains"},
        {"label": "Transport collectif", "value": "Transport collectif"},
        {"label": "Autres", "value": "Autres"}
    ]
}

def generate_input(col):
    if col in dropdown_options:
        return dbc.Form([
            dbc.Label(col.capitalize(), html_for=f"input-{col}"),
            dcc.Dropdown(
                id=f"input-{col}",
                options=dropdown_options[col],
                placeholder=f"Choisir {col.capitalize()}",
                style={"width": "100%"}
            )
        ])
    elif col == "age":
        return dbc.Form([
            dbc.Label(col.capitalize(), html_for=f"input-{col}"),
            dcc.Input(id=f"input-{col}", type="number", placeholder=f"Saisir {col}", style={"width": "100%"})
        ])
    elif col == "place":
        return dbc.Form([
            html.Img(src="/assets/aide_form_place.png", style={"width": "100%", "marginTop": "10px"}),
            dbc.Label("Place", html_for=f"input-{col}"),
            dcc.Input(id=f"input-{col}", type="text", placeholder="Saisir la place", style={"width": "100%"}),
            html.Br()
        ])
    else:
        return dbc.Form([
            dbc.Label(col.capitalize(), html_for=f"input-{col}"),
            dcc.Input(id=f"input-{col}", type="text", placeholder=f"Saisir {col}", style={"width": "100%"})
        ])

layout = dbc.Container([
    html.H2("Saisie d'un accident", className="my-4 text-center"),

    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col(generate_input(col), width=6) for col in selected_cols
            ], className="g-3"),

            html.Div(className="d-flex justify-content-center my-3", children=[
                dbc.Button("Soumettre", id="submit-button", color="primary", n_clicks=0)
            ]),

            html.Hr(),

            dbc.Alert(id="form-output", is_open=False, color="success", duration=4000)
        ])
    ], style={"padding": "20px", "boxShadow": "0px 0px 10px lightgray"})
], fluid=True)


@dash.callback(
    Output("form-output", "children"),
    Output("form-output", "is_open"),
    Input("submit-button", "n_clicks"),
    [State(f"input-{col}", "value") for col in selected_cols]
)
def handle_form(n_clicks, *values):
    if n_clicks > 0:
        data = dict(zip(selected_cols, values))
        return f"Données enregistrées : {data}", True
    return "", False
