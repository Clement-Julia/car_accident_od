import pandas as pd
import sqlite3


csv_path = "data/dataset_simplify.csv"
table_name = "accidents"
df = pd.read_csv(csv_path, low_memory=False)

db_path = "data/bdd.db"
conn = sqlite3.connect(db_path)


df.to_sql(table_name, conn, if_exists="replace", index=False)

print("Extrait de la base :")
for row in conn.execute(f"SELECT * FROM {table_name} LIMIT 5"):
    print(row)


conn.close()

print(f"\nBase SQLite créée : {db_path}, table : {table_name}")
