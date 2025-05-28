import pandas as pd
import plotly.express as px

ordre_gravite = ["Indemne", "Blessé léger", "Blessé hospitalisé", "Tué"]
regroupement = {
        'Voiture': 'Voiture',
        'Véhicule utilitaire': 'Voiture',
        'Poids lourd > 7.5t': 'Poids lourd',
        'Poids lourd <= 7.5t': 'Poids lourd',
        'PL + remorque': 'Poids lourd',
        'Tracteur + semi-remorque': 'Poids lourd',
        'Tracteur routier seul': 'Poids lourd',
        'Quad lourd': 'Deux-roues',
        'Quad léger': 'Deux-roues',
        'Voiturette': 'Deux-roues',
        'Scooter <= 50 cm3': 'Deux-roues',
        'Scooter > 50 cm3': 'Deux-roues',
        'Scooter > 125 cm3': 'Deux-roues',
        'Scooter <= 125 cm3': 'Deux-roues',
        'Cyclomoteur <50cm3': 'Deux-roues',
        'Moto > 125 cm3': 'Deux-roues',
        'Moto <= 125 cm3': 'Deux-roues',
        '3RM > 50 cm3': 'Deux-roues',
        '3RM <= 50 cm3': 'Deux-roues',
        'Bicyclette': 'Deux-roues',
        'EDP motorisé': 'Deux-roues',
        'EDP non motorisé': 'Deux-roues',
        'VAE': 'Deux-roues',
        'Train': 'Autres',
        'Tramway': 'Autres',
        'Autocar': 'Transport collectif',
        'Autobus': 'Transport collectif',
        'Engin spécial': 'Autres',
        'Indéterminable': 'Autres',
        'Non renseigné': 'Autres',
        'Autre': 'Autres'
    }

def clean_grav(df):
    df['grav'] = df['grav'].astype(str).str.strip()
    return df[df['grav'].isin(ordre_gravite)].copy()

def age_moyen_gravite(df):
    df_filtered = clean_grav(df)
    df_filtered = df_filtered.dropna(subset=['an_nais', 'date'])
    df_filtered['an_nais'] = pd.to_numeric(df_filtered['an_nais'], errors='coerce')
    df_filtered['age'] = pd.to_datetime(df_filtered['date']).dt.year - df_filtered['an_nais']
    df_filtered = df_filtered.dropna(subset=['age'])
    df_agg = df_filtered.groupby('grav')['age'].mean().reset_index()
    return px.bar(df_agg, x='grav', y='age', title="Âge moyen par gravité",
                  labels={"age": "Âge moyen", "grav": "Gravité"},
                  category_orders={'grav': ordre_gravite},
                  template="plotly_dark")

def age_moyen_gravite_stats(df):
    df_filtered = df[df['grav'].isin(["Indemne", "Blessé léger", "Blessé hospitalisé", "Tué"])].copy()
    df_filtered = df_filtered.dropna(subset=['an_nais', 'date'])
    df_filtered['an_nais'] = pd.to_numeric(df_filtered['an_nais'], errors='coerce')
    df_filtered['age'] = pd.to_datetime(df_filtered['date']).dt.year - df_filtered['an_nais']
    df_filtered = df_filtered.dropna(subset=['age'])

    stats = df_filtered.groupby('grav')['age'].agg(['mean', 'std']).round(1).reset_index()
    stats.columns = ['Gravité', 'Âge moyen', 'Écart-type']

    ordre_gravite = ["Indemne", "Blessé léger", "Blessé hospitalisé", "Tué"]
    stats['Gravité'] = pd.Categorical(stats['Gravité'], categories=ordre_gravite, ordered=True)
    stats = stats.sort_values('Gravité')

    return stats

def gravite_sexe(df):
    df_filtered = clean_grav(df)
    df_filtered = df_filtered[df_filtered['sexe'].isin(['Homme', 'Femme'])]

    return px.histogram(
        df_filtered, x='sexe', color='grav', barmode='group',
        title="Gravité selon le sexe", labels={"sexe": "Sexe"},
        category_orders={'grav': ordre_gravite},
        template="plotly_dark"
    )

def gravite_sexe_stats(df):
    df_filtered = clean_grav(df)
    df_filtered = df_filtered[df_filtered['sexe'].isin(['Homme', 'Femme'])]

    total = df_filtered.groupby('sexe').size().rename("total")
    stats = df_filtered.groupby(['sexe', 'grav']).size().unstack(fill_value=0)
    stats = stats.divide(total, axis=0) * 100
    return stats.round(1).reset_index()

def gravite_catv(df):
    df_filtered = clean_grav(df)
    df_filtered['type_vehicule'] = df_filtered['catv'].map(regroupement).fillna('Autres')

    return px.histogram(
        df_filtered, x='type_vehicule', color='grav', barmode='group',
        title="Type de véhicules impliqués selon la gravité",
        labels={"type_vehicule": "Type de véhicule"},
        category_orders={'grav': ordre_gravite},
        template="plotly_dark"
    )

def gravite_catv_stats(df):
    df_filtered = df[df['grav'].isin(ordre_gravite)].copy()
    df_filtered['type_vehicule'] = df_filtered['catv'].map(regroupement).fillna('Autres')

    total = df_filtered.groupby('type_vehicule').size().rename("total")
    stats = df_filtered.groupby(['type_vehicule', 'grav']).size().unstack(fill_value=0)
    stats = stats[ordre_gravite]
    stats = stats.divide(total, axis=0) * 100
    return stats.round(1).reset_index()
