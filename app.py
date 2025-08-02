import os, random, json
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "91ab2470b52f1166f64f1267c08e3a3792c1df343c4936a597fb3e0a762c66f3")

with open('contenu_site.json', encoding='utf-8') as f:
    CONTENU_SITE = json.load(f)

with open('journees.json', encoding='utf-8') as f:
    JOURNEES = json.load(f)

def journee_du_jour():
    today = datetime.now()
    return JOURNEES.get(today.strftime("%d-%m"))

def journees_a_venir(n=5):
    today = datetime.now()
    resultats = []
    for i in range(1, 31):
        d = today + timedelta(days=i)
        cle = d.strftime("%d-%m")
        if cle in JOURNEES:
            resultats.append({"date": d.strftime("%d/%m/%Y"), "evenement": JOURNEES[cle]})
            if len(resultats) >= n:
                break
    return resultats

def generer_post(event, reseau):
    phrases = [
        f"🎯 En cette {event}, pensez à nos {random.choice(CONTENU_SITE['produits'])}",
        f"🚨 Pour {event}, découvrez nos {random.choice(CONTENU_SITE['services'])}",
        f"💡 Conseil du jour ({event}) : {random.choice(CONTENU_SITE['conseils'])}",
        f"📢 Aujourd'hui c’est {event} — engagez-vous avec Passion Prévention !"
    ]
    texte = random.choice(phrases)
    hashtags = ["#sécurité", "#prévention", "#PassionPrévention"]
    return texte, hashtags

@app.route('/api/genere-post', methods=['POST'])
def genere_post():
    data = request.get_json()
    mois, annee, reseaux = data.get("mois"), data.get("annee"), data.get("reseaux", [])
    event = journee_du_jour() or "la sécurité au quotidien"
    avenir = journees_a_venir()

    postages = {}
    for r in reseaux:
        texte, hashtags = generer_post(event, r)
        postages[r] = {
            "texte": texte,
            "hashtags": hashtags,
            "avenir": avenir
        }

    return jsonify({"postages": postages})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render injecte ce PORT
    app.run(host='0.0.0.0', port=port)



