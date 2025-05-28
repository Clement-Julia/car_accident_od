import pandas as pd
import plotly.express as px

grav_mapping = {
    'Indemne': 1,
    'Blessé léger': 2,
    'Blessé hospitalisé': 3,
    'Tué': 4
}

def plot_top_vehicules_graves(df):
    df['grav_num'] = df['grav'].map(grav_mapping)
    df_graves = df[df['grav'].isin(['Tué', 'Blessé hospitalisé'])]
    top_vehicules = df_graves['catv'].value_counts().head(10).reset_index()
    top_vehicules.columns = ['catv', 'nb_accidents']

    fig = px.bar(
        top_vehicules,
        x='nb_accidents',
        y='catv',
        orientation='h',
        title="Top 10 des types de véhicules impliqués dans des accidents graves",
        labels={'catv': 'Type de véhicule', 'nb_accidents': "Nombre d'accidents graves"},
        color='nb_accidents',
        color_continuous_scale='viridis'
    )
    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        template="plotly_dark"
    )
    return fig

def plot_gravite_moyenne_manv(df):
    df['grav_num'] = df['grav'].map(grav_mapping)
    df_manv = df.groupby('manv').agg(
        grav_moyenne=('grav_num', 'mean')
    ).reset_index()

    df_manv = df_manv.sort_values(by='grav_moyenne', ascending=False)
    global manv_order
    manv_order = df_manv['manv'].tolist()

    fig = px.bar(
        df_manv,
        x='grav_moyenne',
        y='manv',
        orientation='h',
        title="Gravité moyenne des accidents selon la manœuvre",
        labels={'manv': 'Manœuvre', 'grav_moyenne': 'Gravité moyenne'},
        color='grav_moyenne',
        color_continuous_scale='plasma_r'
    )
    fig.update_layout(
        yaxis={'categoryorder': 'array', 'categoryarray': manv_order, 'autorange': 'reversed'},
        template="plotly_dark"
    )
    return fig

def plot_nombre_accidents_manv(df):
    df['grav_num'] = df['grav'].map(grav_mapping)

    df_manv = df.groupby('manv').agg(
        nb_accidents=('grav_num', 'count')
    ).reset_index()

    df_manv['manv'] = pd.Categorical(df_manv['manv'], categories=manv_order, ordered=True)
    df_manv = df_manv.sort_values('manv')

    fig = px.bar(
        df_manv,
        x='nb_accidents',
        y='manv',
        orientation='h',
        title="Nombre d'accidents par manœuvre",
        labels={'manv': 'Manœuvre', 'nb_accidents': "Nombre d'accidents"}
    )
    fig.update_layout(
        yaxis={'categoryorder': 'array', 'categoryarray': manv_order, 'autorange': 'reversed'},
        coloraxis_showscale=False,
        template="plotly_dark"
    )
    return fig

def stats_nb_accidents_manv(df):
    global manv_order
    count_df = df['manv'].value_counts().reindex(manv_order).reset_index()
    count_df.columns = ['Manœuvre', 'Nombre d\'accidents']
    return count_df