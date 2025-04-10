from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

paris = []
next_id = 1

@app.route("/")
def index():
    return render_template("index.html", paris=paris)

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
    return redirect(url_for("index"))

@app.route("/modifier/<int:pari_id>", methods=["GET", "POST"])
def modifier(pari_id):
    pari = next((p for p in paris if p["id"] == pari_id), None)
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

        return redirect(url_for("index"))

    return render_template("modifier.html", pari=pari)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
