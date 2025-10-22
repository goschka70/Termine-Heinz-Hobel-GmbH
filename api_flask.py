from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/api/termine", methods=["GET"])
def get_termine():
    standort = request.args.get("standort", "")
    datum = request.args.get("datum", pd.Timestamp.now().date().isoformat())

    df = pd.read_csv("AMTermine.csv", sep=";", encoding="utf-8")
    df["Termin"] = pd.to_datetime(df["Termin"], errors="coerce")
    df = df[df["Termin"].dt.date == pd.to_datetime(datum).date()]
    df = df[df["Platz"].str.contains(standort, case=False, na=False)]

    result = df.sort_values("Termin").to_dict(orient="records")
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
