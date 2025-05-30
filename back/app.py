from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "bdd.db")

@app.route("/vehicule-types")
def get_vehicule_types():
    conn = sqlite3.connect(DB_PATH)
    df = conn.execute("SELECT DISTINCT catv FROM accidents").fetchall()
    conn.close()
    return jsonify([r[0] for r in df if r[0]])

@app.route('/grav-types')
def get_grav_accident_types():
    conn = sqlite3.connect(DB_PATH)
    df = conn.execute("SELECT DISTINCT grav FROM accidents").fetchall()
    conn.close()
    return jsonify([r[0] for r in df if r[0]])

@app.route("/points")
def get_filtered_points():
    catv = request.args.get("catv")
    start_year = request.args.get("start")
    end_year = request.args.get("end")
    grav = request.args.get("grav")

    if not start_year or not end_year:
        return jsonify([])

    query = """
    SELECT lat, long, atm, col, surf, manv, grav
    FROM accidents
    WHERE strftime('%Y', date) BETWEEN ? AND ?
    AND lat IS NOT NULL AND long IS NOT NULL
    """

    params = [start_year,end_year]

    if catv and catv != "all":
        query += "AND catv = ? "
        params.append(catv)
    if grav and grav != "all":
        query += " AND grav = ? "
        params.append(grav)

    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(query, params).fetchall()
    conn.close()

    results = []
    for lat, lon, atm, col, surf, manv, grav in rows:
        results.append({
            "lat": lat,
            "lon": lon,
            "atm": atm,
            "col": col,
            "surf": surf,
            "manv": manv,
            "catv": catv,
            "grav": grav
        })

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
