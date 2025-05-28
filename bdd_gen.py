import pandas as pd
import sqlite3

# Charger le CSV
csv_path = "data/dataset_simplify.csv"  # Remplace par le chemin local si nécessaire
df = pd.read_csv(csv_path, low_memory=False)

# Connexion à SQLite
db_path = "bdd.db"
conn = sqlite3.connect(db_path)

# Nom de la table
table_name = "donnees_simplifiees"

# Export vers SQLite
df.to_sql(table_name, conn, if_exists="replace", index=False)

# Vérification : affichage de 5 lignes
print("Extrait de la base :")
for row in conn.execute(f"SELECT * FROM {table_name} LIMIT 5"):
    print(row)

# Fermer la connexion
conn.close()

print(f"\nBase SQLite créée : {db_path}, table : {table_name}")
