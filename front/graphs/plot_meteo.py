import plotly.express as px

def plot_gravite_meteo_interactif(df):
    gravite_par_atm = df.dropna(subset=['grav_num', 'atm'])
    gravite_par_atm = gravite_par_atm.groupby('atm')['grav_num'].mean().reset_index()
    gravite_par_atm = gravite_par_atm.sort_values(by='grav_num', ascending=False)

    fig = px.bar(
        gravite_par_atm,
        x="atm",
        y="grav_num",
        title="Gravité moyenne des accidents par condition météo",
        labels={"atm": "Condition météo", "grav_num": "Gravité moyenne"},
        color="grav_num",
        color_continuous_scale="viridis"
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_nombre_accidents_meteo(df_unique):
    df_filtered = df_unique[df_unique['atm'] != 'Normale']
    df_atm = df_filtered['atm'].value_counts().reset_index()
    df_atm.columns = ['atm', 'nb_accidents']

    fig = px.bar(
        df_atm,
        x='atm',
        y='nb_accidents',
        title="Nombre d'accidents selon les conditions météorologiques (hors 'Normale')",
        labels={"atm": "Conditions météo", "nb_accidents": "Nombre d'accidents"},
        color='nb_accidents',
        color_continuous_scale="blues"
    )
    fig.update_layout(xaxis_tickangle=30)
    return fig


def plot_catr_atm(df_unique):
    df_grouped = df_unique.groupby(['catr', 'atm']).size().reset_index(name='nb_accidents')
    df_grouped = df_grouped[df_grouped['atm'] != 'Normale']

    fig = px.bar(
        df_grouped,
        x='catr',
        y='nb_accidents',
        color='atm',
        barmode='group',
        title="Nombre d'accidents par type de route et conditions météorologiques (hors 'Normale')",
        labels={
            "catr": "Type de route",
            "nb_accidents": "Nombre d'accidents",
            "atm": "Condition météo"
        }
    )
    fig.update_layout(
        xaxis_tickangle=70,
        legend_title_text="Météo",
        legend=dict(x=1.05, y=1)
    )
    return fig
