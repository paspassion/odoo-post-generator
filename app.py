import os, random, json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

with open('contenu_site.json', encoding='utf-8') as f:
    CONTENU_SITE = json.load(f)

def generer_post(reseau):
    phrases = [
        f"🚨 Besoin de prévention ? Découvrez : {random.choice(CONTENU_SITE['produits'])} En libre accès ou en atelier encadré... ✔️ Livré partout en France. 📍 Plus d’infos : 🔗 www.passion-prevention.com",
        f"💡 Le conseil Passion Prévention : {random.choice(CONTENU_SITE['conseils'])} ✔️ Découvrez toutes nos solutions sur www.passion-prevention.com",
        f"📢 Nos services pour vous accompagner : {random.choice(CONTENU_SITE['services'])} — Contactez-nous sur www.passion-prevention.com",
        f"🎯 En entreprise, en collectivité ou en événement : optez pour {random.choice(CONTENU_SITE['produits'])} !"
    ]
    texte = random.choice(phrases)
    hashtags = ["#PassionPrévention", "#sécurité", "#prévention", "#QHSE", "#sécuritéTravail", "#formation", "#incendie", "#événementiel", "#risques", "#santé"]
    return texte, hashtags

@app.route('/api/genere-post', methods=['POST'])
def genere_post():
    data = request.get_json()
    reseaux = data.get("reseaux", [])
    postages = {}

    for r in reseaux:
        texte, hashtags = generer_post(r)
        postages[r] = {
            "texte": texte,
            "hashtags": hashtags
        }

    return jsonify({"postages": postages})

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
