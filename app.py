
from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = "data.json"

# Charger les données
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        paris = json.load(f)
else:
    paris = []

next_id = max([p["id"] for p in paris], default=0) + 1

@app.route("/")
def index():
    stats = {
        "total": len(paris),
        "gagnes": sum(1 for p in paris if p["resultat"] == "Gagné"),
        "perdus": sum(1 for p in paris if p["resultat"] == "Perdu"),
        "annules": sum(1 for p in paris if p["resultat"] == "Annulé"),
        "mise_totale": round(sum(p["mise"] for p in paris), 2),
        "gain_total": round(sum(p["gain"] for p in paris), 2)
    }
    stats["profit"] = stats["gain_total"] - stats["mise_totale"]
    stats["taux_reussite"] = round(stats["gagnes"] / stats["total"] * 100, 2) if stats["total"] else 0
    return render_template("index.html", paris=paris, stats=stats)

@app.route("/ajouter", methods=["POST"])
def ajouter():
    global next_id
    pari = {
        "id": next_id,
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
    next_id += 1
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(paris, f, indent=4, ensure_ascii=False)
    return redirect(url_for("index"))

@app.route("/supprimer/<int:pari_id>")
def supprimer(pari_id):
    global paris
    paris = [p for p in paris if p["id"] != pari_id]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(paris, f, indent=4, ensure_ascii=False)
    return redirect(url_for("index"))
