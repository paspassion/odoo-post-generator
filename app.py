import os, json, random
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta

app = Flask(__name__, static_folder='static')
CORS(app)

def scrape_site():
    base_url = "https://www.passion-prevention.com"
    produits, services, conseils = set(), set(), set()

    try:
        r = requests.get(f"{base_url}/shop", timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.select("a.oe_product"):
            titre = a.get("title") or a.text
            if titre:
                produits.add(titre.strip())
    except Exception as e:
        print("Erreur scraping produits:", e)

    # Exemples fixes
    services.update([
        "location de bornes éthylotests",
        "formation incendie",
        "formation habilitation électrique"
    ])
    conseils.update([
        "Testez-vous avant de prendre le volant.",
        "Vérifiez la date de péremption de vos extincteurs.",
        "Placez les extincteurs à portée visible."
    ])
    return list(produits), list(services), list(conseils)

def genere_post_scrape():
    produits, services, conseils = scrape_site()
    base_url = "https://www.passion-prevention.com"
    themes = [
        "Conseil sécurité incendie",
        "Prévention routière",
        "Équipement obligatoire en entreprise",
        "Témoignage client",
        "Promo location borne",
        "Formation obligatoire",
        "Alcool & événement festif"
    ]
    plateformes_possibles = [
        ["Facebook", "Instagram"],
        ["TikTok", "Reels Instagram"],
        ["LinkedIn", "Facebook"],
        ["LinkedIn", "Instagram"]
    ]
    hashtags_base = [
        "#Sécurité", "#Prévention", "#PassionPrévention", "#Incendie",
        "#TravailEnSécurité", "#Équipements", "#Formation", "#QHSE",
        "#Responsabilité", "#Risques", "#BTP"
    ]

    planning = []
    date = datetime.now()

    for i in range(7):
        jour = date + timedelta(days=i)
        theme = random.choice(themes)
        plateformes = random.choice(plateformes_possibles)
        produit = random.choice(produits) if produits else "un produit de sécurité"
        conseil = random.choice(conseils) if conseils else "Un bon réflexe sauve des vies."

        texte = f"🚨 {theme} : {conseil if 'Conseil' in theme else 'Découvrez notre solution ' + produit} sur {base_url}"

        planning.append({
            "date": jour.strftime("%d/%m/%Y (%A)"),
            "theme": theme,
            "texte": texte,
            "plateformes": ", ".join(plateformes),
            "hashtags": random.sample(hashtags_base, 10)
        })

    return planning

@app.route('/api/genere-post', methods=['GET'])
def generate():
    planning = genere_post_scrape()
    with open("historique.json", "w", encoding="utf-8") as f:
        json.dump(planning, f, indent=2, ensure_ascii=False)
    return jsonify(planning)

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
def static_file(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)