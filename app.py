import os, random, json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__, static_folder='static')
CORS(app)

# Données
with open('journees.json', encoding='utf-8') as f:
    JOURNEES = json.load(f)
with open('extracted_products.json', encoding='utf-8') as f:
    PRODUITS = json.load(f)

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
            resultats.append({
                "date": d.strftime("%d/%m/%Y"),
                "evenement": JOURNEES[cle]
            })
            if len(resultats) >= n:
                break
    return resultats

def generate_rich_post(product):
    titre = product["title"]
    desc = product.get("description", "").strip()[:200]

    intro = random.choice([
        "🔴 POST SÉCURITÉ – " + titre,
        "🛡️ Focus produit : " + titre,
        "🎯 Mettez en avant : " + titre,
        "🚨 Besoin de prévention ? Découvrez : " + titre
    ])

    contexte = random.choice([
        "Soirée ? Festival ? Mariage ?",
        "Sur vos événements festifs...",
        "En entreprise comme en collectivité...",
        "Pour vos animations de prévention...",
        "En libre accès ou en atelier encadré..."
    ])

    appel = random.choice([
        "✔️ Disponible dès aujourd’hui.",
        "✔️ À utiliser avec modération.",
        "✔️ Inclus dans nos packs événementiels.",
        "✔️ Livré partout en France.",
        "✔️ Compatible avec nos animations sécurité."
    ])

    texte = intro + "\n" + desc + "\n" + contexte + "\n" + appel + "\n\n📍 Plus d’infos :\n🔗 www.passion-prevention.com"
    mots = set(texte.lower().replace("’", "'").split())
    base_tags = {"#sécurité", "#prévention", "#PassionPrévention"}
    dyn_tags = {
        "#" + m.strip(".,!?").lower()
        for m in mots
        if len(m) > 4 and m[0].isalpha() and not m.startswith("www")
    }
    hashtags = list((base_tags | dyn_tags) - {"#https", "#www", "#com"})
    return {
        "titre": titre,
        "texte": texte,
        "hashtags": sorted(hashtags)[:12]
    }

@app.route('/api/genere-post', methods=['POST'])
def genere_post():
    data = request.get_json()
    reseaux = data.get("reseaux", [])
    avenir = journees_a_venir()
    postages = {}
    for reseau in reseaux:
        p = random.choice(PRODUITS)
        post = generate_rich_post(p)
        post["avenir"] = avenir
        postages[reseau] = post
    return jsonify({"postages": postages})

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)