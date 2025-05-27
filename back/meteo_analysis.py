import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, "..", "data", "dataset_simplify.csv")
df = pd.read_csv(data_path)
df_unique = df.drop_duplicates("Num_Acc")

grav_mapping = {
    'Indemne': 1,
    'Blessé léger': 2,
    'Blessé hospitalisé': 3,
    'Tué': 4
}
df['grav_num'] = df['grav'].map(grav_mapping)

def plot_gravite_meteo():
    gravite_par_atm = df.dropna(subset=['grav_num', 'atm'])
    gravite_par_atm = gravite_par_atm.groupby('atm')['grav_num'].mean().reset_index()
    gravite_par_atm = gravite_par_atm.sort_values(by='grav_num', ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=gravite_par_atm, x='atm', y='grav_num', palette='viridis')
    plt.title("Gravité moyenne des accidents par condition météo")
    plt.xlabel("Condition météo")
    plt.ylabel("Gravité moyenne")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_nombre_accidents_meteo_sans_normale():
    df_filtered = df_unique[df_unique['atm'] != 'Normale']
    df_atm = df_filtered['atm'].value_counts().reset_index()
    df_atm.columns = ['atm', 'nb_accidents']

    plt.figure(figsize=(10, 6))
    sns.barplot(x='atm', y='nb_accidents', data=df_atm)
    plt.title("Nombre d'accidents selon les conditions météorologiques (hors 'Normale')")
    plt.xlabel("Conditions météo")
    plt.ylabel("Nombre d'accidents")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

def plot_catr_atm_sans_normale():
    df_grouped = df_unique.groupby(['catr', 'atm']).size().reset_index(name='nb_accidents')
    df_grouped = df_grouped[df_grouped['atm'] != 'Normale']

    plt.figure(figsize=(12, 6))
    sns.barplot(x='catr', y='nb_accidents', hue='atm', data=df_grouped)
    plt.title("Nombre d'accidents par type de route et conditions météorologiques (hors 'Normale')")
    plt.xlabel("Type de route")
    plt.ylabel("Nombre d'accidents")
    plt.xticks(rotation=70)
    plt.legend(title="Météo", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_gravite_meteo()
    plot_nombre_accidents_meteo_sans_normale()
    plot_catr_atm_sans_normale()
