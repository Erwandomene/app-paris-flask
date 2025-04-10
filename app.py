
from flask import Flask, render_template, request, redirect, url_for
from uuid import uuid4
import json
import os
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "data.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        paris = json.load(f)
else:
    paris = []

@app.route("/")
def index():
    total = len(paris)
    nb_gagnes = sum(1 for p in paris if p["resultat"] == "Gagné")
    nb_perdus = sum(1 for p in paris if p["resultat"] == "Perdu")
    nb_annules = sum(1 for p in paris if p["resultat"] == "Annulé")
    nb_encours = sum(1 for p in paris if p["resultat"] == "En cours")
    mise_totale = sum(p["mise"] for p in paris)
    gain_total = sum(p["gain"] for p in paris)
    taux_reussite = round((nb_gagnes / total) * 100, 2) if total > 0 else 0
    profit = round(gain_total - mise_totale, 2)

    stats = {
        "total": total,
        "taux_reussite": taux_reussite,
        "mise_totale": round(mise_totale, 2),
        "gain_total": round(gain_total, 2),
        "profit": profit
    }

    resultats_count = {
        "Gagné": nb_gagnes,
        "Perdu": nb_perdus,
        "Annulé": nb_annules,
        "En cours": nb_encours
    }

    profit_par_mois = defaultdict(float)
    for p in paris:
        try:
            date_obj = datetime.strptime(p["date"], "%Y-%m-%d")
            mois = date_obj.strftime("%Y-%m")
            profit_par_mois[mois] += p["gain"]
        except:
            pass

    profit_par_mois = dict(sorted(profit_par_mois.items()))

    return render_template("index.html", paris=paris, stats=stats,
                           resultats=resultats_count, profits=profit_par_mois)

@app.route("/ajouter", methods=["POST"])
def ajouter():
    pari = {
        "id": str(uuid4()),
        "date": request.form["date"],
        "match": request.form["match"],
        "competition": request.form["competition"],
        "type": request.form["type_pari"],
        "cote": float(request.form["cote"]),
        "mise": float(request.form["mise"]),
        "bookmaker": request.form["bookmaker"],
        "resultat": request.form["resultat"],
        "commentaire": request.form["commentaire"]
    }
    if pari["resultat"] == "Gagné":
        pari["gain"] = round(pari["mise"] * pari["cote"] - pari["mise"], 2)
    elif pari["resultat"] == "Perdu":
        pari["gain"] = -pari["mise"]
    else:
        pari["gain"] = 0
    paris.append(pari)
    sauvegarder()
    return redirect(url_for("index"))

@app.route("/modifier/<id>", methods=["GET", "POST"])
def modifier(id):
    pari = next((p for p in paris if p["id"] == id), None)
    if not pari:
        return "Pari introuvable", 404

    if request.method == "POST":
        pari["date"] = request.form["date"]
        pari["match"] = request.form["match"]
        pari["competition"] = request.form["competition"]
        pari["type"] = request.form["type_pari"]
        pari["cote"] = float(request.form["cote"])
        pari["mise"] = float(request.form["mise"])
        pari["bookmaker"] = request.form["bookmaker"]
        pari["resultat"] = request.form["resultat"]
        pari["commentaire"] = request.form["commentaire"]

        if pari["resultat"] == "Gagné":
            pari["gain"] = round(pari["mise"] * pari["cote"] - pari["mise"], 2)
        elif pari["resultat"] == "Perdu":
            pari["gain"] = -pari["mise"]
        else:
            pari["gain"] = 0
        sauvegarder()
        return redirect(url_for("index"))

    return render_template("modifier.html", pari=pari)

@app.route("/supprimer/<id>")
def supprimer(id):
    global paris
    paris = [p for p in paris if p["id"] != id]
    sauvegarder()
    return redirect(url_for("index"))

def sauvegarder():
    with open(DATA_FILE, "w") as f:
        json.dump(paris, f, indent=4)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
