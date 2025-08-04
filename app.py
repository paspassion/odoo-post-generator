import os, random
import requests
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

def scraper_produits():
    url = "https://www.passion-prevention.com/shop"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    produits = [p.get_text(strip=True) for p in soup.select(".oe_product, .product_title") if p.get_text(strip=True)]
    return produits if produits else ["borne éthylotest", "extincteur", "gilet haute visibilité"]

themes = [
    "Conseil sécurité incendie",
    "Vidéo TikTok Borne",
    "Promo location borne",
    "Témoignage client",
    "Prévention routière",
    "Astuce sécurité électrique",
    "Équipement obligatoire en entreprise"
]

reseaux_par_theme = {
    "Conseil sécurité incendie": ["Facebook", "Instagram", "LinkedIn"],
    "Vidéo TikTok Borne": ["TikTok", "Instagram"],
    "Promo location borne": ["Facebook", "Instagram", "LinkedIn", "TikTok"],
    "Témoignage client": ["Facebook", "LinkedIn"],
    "Prévention routière": ["Facebook", "Instagram"],
    "Astuce sécurité électrique": ["LinkedIn", "Facebook"],
    "Équipement obligatoire en entreprise": ["LinkedIn", "Instagram"]
}

hashtags_generaux = [
    "#Sécurité", "#Prévention", "#Risques", "#Formation", "#Équipements",
    "#PassionPrévention", "#TravailEnSécurité", "#QHSE", "#Incendie", "#BTP", "#Responsabilité"
]

@app.route('/api/genere-post', methods=["POST"])
def genere_post():
    produits = scraper_produits()
    posts = []
    start_date = datetime.today()
    for i in range(4):  # génère 4 posts
        date = start_date + timedelta(days=i * 3)
        theme = random.choice(themes)
        texte = f"🚨 {theme} : Découvrez notre solution {random.choice(produits)} sur www.passion-prevention.com"
        hashtags = random.sample(hashtags_generaux, 10)
        posts.append({
            "date": date.strftime("%d/%m/%Y"),
            "jour": date.strftime("%A"),
            "theme": theme,
            "texte": texte,
            "reseaux": reseaux_par_theme[theme],
            "hashtags": hashtags
        })
    return jsonify({"posts": posts})

@app.route('/')
def root():
    return send_from_directory('static', 'index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)