import os, random
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__, static_folder='static')
CORS(app)

def scrape_contenu():
    url = "https://www.passion-prevention.com/shop"
    produits, services, conseils = [], [], []

    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for prod in soup.select('.oe_product.oe_grid.oe-height'):
            titre = prod.select_one('.product_title a')
            if titre:
                nom = titre.text.strip()
                if nom not in produits:
                    produits.append(nom)

        services = [
            "formation incendie", "habilitation électrique", "location d’extincteurs",
            "location de bornes éthylotests", "formation évacuation", "plan d’intervention"
        ]
        conseils = [
            "Testez-vous avant de prendre le volant.",
            "Pensez à signaler les sorties de secours.",
            "Placez les extincteurs en accès visible.",
            "Ne surchargez pas les multiprises."
        ]
    except Exception as e:
        print("Erreur scraping:", e)

    return {
        "produits": produits,
        "services": services,
        "conseils": conseils
    }

def generer_post(r):
    contenu = scrape_contenu()
    theme = random.choice(["sécurité incendie", "équipement obligatoire", "prévention routière"])
    texte = ""

    if theme == "sécurité incendie":
        produit = random.choice(contenu['produits'])
        texte = f"🔥 Sécurité Incendie : Découvrez notre {produit} pour protéger vos équipes. 📍 Plus d’infos sur www.passion-prevention.com"
    elif theme == "prévention routière":
        conseil = random.choice(contenu['conseils'])
        texte = f"🚗 Conseil prévention routière : {conseil} 📍 Plus d’infos sur www.passion-prevention.com"
    else:
        service = random.choice(contenu['services'])
        texte = f"✅ Prévention au travail : Notre service de {service} est là pour vous accompagner. 📍 www.passion-prevention.com"

    hashtags = [
        "#Sécurité", "#Prévention", "#Formation", "#QHSE", "#TravailEnSécurité",
        "#Responsabilité", "#PassionPrévention", "#Risques", "#Incendie", "#Équipements"
    ]
    random.shuffle(hashtags)

    return {
        "date": datetime.now().strftime("%d/%m/%Y (%A)"),
        "theme": theme,
        "texte": texte,
        "plateformes": [r],
        "hashtags": hashtags[:10]
    }

@app.route('/api/genere-post', methods=['POST'])
def genere_post():
    data = request.get_json()
    reseaux = data.get("reseaux", ["Facebook", "Instagram"])
    posts = []

    for r in reseaux:
        post = generer_post(r)
        posts.append(post)

    with open("historique.json", "w", encoding="utf-8") as f:
        import json
        json.dump(posts, f, indent=2, ensure_ascii=False)

    return jsonify(posts)

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
