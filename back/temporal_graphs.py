import pandas as pd
import plotly.express as px

def load_temporal_data(df):
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])

    df['annee'] = df['date'].dt.year
    df['mois'] = df['date'].dt.month
    df['jour_semaine'] = df['date'].dt.dayofweek
    df['heure'] = df['date'].dt.hour
    df['grav'] = df['grav'].astype(str).str.strip()

    return df

def plot_accidents_mois(df):
    mois_labels = {
        1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
        7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
    }
    df['mois_label'] = df['mois'].map(mois_labels)
    df['mois'] = df['mois'].astype(int)

    fig = px.histogram(df, x='mois_label', title="Accidents par mois", template="plotly_dark",
                 category_orders={"mois_label": list(mois_labels.values())})
    return fig

def plot_accidents_jour(df):
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    df['jour_label'] = df['jour_semaine'].map(dict(zip(range(7), jours)))
    fig = px.histogram(df, x='jour_label', title="Accidents par jour de la semaine", template="plotly_dark",
                 category_orders={"jour_label": jours})
    return fig

def plot_accidents_heure(df):
    return px.histogram(df, x='heure', title="Accidents par heure", nbins=24, template="plotly_dark")

def plot_tendance_annuelle(df):
    df_agg = df.groupby('annee').size().reset_index(name='count')
    fig = px.line(df_agg, x='annee', y='count', title="Tendance annuelle des accidents", template="plotly_dark")
    fig.update_xaxes(dtick=1, tickformat=".0f")
    return fig

def plot_age_annee(df):
    df = df.dropna(subset=['an_nais'])
    df['an_nais'] = pd.to_numeric(df['an_nais'], errors='coerce')
    df = df.dropna(subset=['an_nais'])

    df['annee'] = df['date'].dt.year
    df['age'] = df['annee'] - df['an_nais']

    bins = [0, 18, 30, 45, 60, 75, 90, 120]
    labels = ['<18', '18-29', '30-44', '45-59', '60-74', '75-89', '90+']
    df['tranche_age'] = pd.cut(df['age'], bins=bins, labels=labels)

    df_group = df.groupby(['annee', 'tranche_age']).size().reset_index(name='count')

    fig = px.bar(
        df_group, x='tranche_age', y='count', color='annee', barmode='group',
        title="Nombre d’accidents par tranche d’âge et par année",
        template="plotly_dark"
    )
    return fig

def plot_heatmap_jour_heure(df):
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    df['jour_label'] = df['jour_semaine'].map(dict(zip(range(7), jours)))
    pivot = df.pivot_table(index='heure', columns='jour_label', aggfunc='size', fill_value=0)
    fig = px.imshow(pivot[jours], title="Intensité des accidents par jour et heure", 
                    labels=dict(x="Jour de la semaine", y="Heure", color="Nombre d'accidents"),
                    template="plotly_dark", aspect="auto")
    return fig

def stats_top_zones_temporelles(df):
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    df['jour_label'] = df['jour_semaine'].map(dict(zip(range(7), jours)))
    top = df.groupby(['jour_label', 'heure']).size().reset_index(name='count')
    top_sorted = top.sort_values(by='count', ascending=False).head(10)
    top_sorted.columns = ['Jour', 'Heure', 'Nombre d\'accidents']
    return top_sorted


def plot_accidents_heure_gravite(df):
    ordre_gravite = ["Indemne", "Blessé léger", "Blessé hospitalisé", "Tué"]
    df_filtered = df[df['grav'].isin(ordre_gravite)].copy()

    fig = px.histogram(
        df_filtered, x='heure', color='grav', barmode='group',
        category_orders={'grav': ordre_gravite},
        title="Accidents par heure et gravité", template="plotly_dark",
        labels={"grav": "Gravité"}
    )
    return fig

def plot_gravite_annee(df):
    ordre_gravite = ["Indemne", "Blessé léger", "Blessé hospitalisé", "Tué"]
    df_filtered = df[df['grav'].isin(ordre_gravite)].copy()

    fig = px.histogram(
        df_filtered, x='annee', color='grav', barmode='stack',
        category_orders={'grav': ordre_gravite},
        title="Répartition des gravités par année", template="plotly_dark",
        labels={"grav": "Gravité"}
    )
    fig.update_xaxes(dtick=1, tickformat=".0f")
    return fig

def stats_gravite_annee(df):
    ordre = ["Indemne", "Blessé léger", "Blessé hospitalisé", "Tué"]
    df_grav = df[df['grav'].isin(ordre)].copy()
    total = df_grav.groupby('annee').size()
    stats = df_grav.groupby(['annee', 'grav']).size().unstack(fill_value=0)
    stats = stats.divide(total, axis=0) * 100
    stats = stats[ordre].round(1).reset_index()
    return stats

def plot_accidents_jour_catr(df):
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    df['jour_label'] = df['jour_semaine'].map(dict(zip(range(7), jours)))
    df_filtered = df.dropna(subset=['catr', 'jour_label'])

    exclude_labels = [
        "Hors réseau public",
        "Autre",
        "Parking ouvert à la circulation"
    ]
    df_filtered = df_filtered[~df_filtered['catr'].isin(exclude_labels)]

    fig = px.histogram(
        df_filtered, x='jour_label', color='catr', barmode='group',
        category_orders={'jour_label': jours},
        title="Accidents par jour de la semaine et type de route", template="plotly_dark",
        labels={"catr": "Type de route"}
    )
    return fig



