import pandas as pd
import plotly.express as px
import os

current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, "..", "data", "dataset_simplify.csv")
df = pd.read_csv(data_path)

grav_mapping = {
    'Indemne': 1,
    'Blessé léger': 2,
    'Blessé hospitalisé': 3,
    'Tué': 4
}
df['grav_num'] = df['grav'].map(grav_mapping)

def plot_top_vehicules_graves():
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
    fig.update_layout(yaxis=dict(autorange="reversed"))
    fig.show()

def plot_gravite_moyenne_manv():
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
        color_continuous_scale='magma_r'
    )
    fig.update_layout(
        yaxis={'categoryorder': 'array', 'categoryarray': manv_order, 'autorange': 'reversed'}
    )
    fig.show()


def plot_nombre_accidents_manv():
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
        coloraxis_showscale=False
    )
    fig.show()


if __name__ == "__main__":
    plot_top_vehicules_graves()
    plot_gravite_moyenne_manv()
    plot_nombre_accidents_manv()
