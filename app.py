from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
paris = []

@app.route("/")
def index():
    return render_template("index.html", paris=paris)

@app.route("/ajouter", methods=["POST"])
def ajouter():
    pari = {
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
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
