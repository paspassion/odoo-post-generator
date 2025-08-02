from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import random
import json
from datetime import datetime

# Initialisation Flask
app = Flask(__name__)
CORS(app)

# Lecture du contenu
with open('contenu_site.json', encoding='utf-8') as f:
    CONTENU_SITE = json.load(f)

with open('journees.json', encoding='utf-8') as f:
    JOURNEES_MONDALES = json.load(f)

def journee_du_jour():
    today = datetime.now().strftime("%d-%m")
    return JOURNEES_MONDALES.get(today)

def journees_a_venir(n=5):
    aujourd_hui = datetime.now()
    resultats = []
    for k, v in JOURNEES_MONDALES.items():
        try:
            date_obj = datetime.strptime(k, "%d-%m").replace(year=aujourd_hui.year)
            if date_obj >= aujourd_hui:
                resultats.append((date_obj, v))
        except:
            continue
    resultats = sorted(resultats)[:n]
    return [{"date": d.strftime("%d-%m"), "intitule": t} for d, t in resultats]

@app.route('/api/genere-post', methods=['POST'])
def genere_post():
    data = request.get_json()
    mois = data.get('mois')
    annee = data.get('annee')
    reseaux = data.get('reseaux', [])

    evenement = journee_du_jour()
    posts = {}

    for r in reseaux:
        if evenement:
            texte = f"📅 En cette {evenement}, pensez à votre sécurité avec {random.choice(CONTENU_SITE['produits'])}."
        else:
            texte = f"🔒 Chez Passion Prévention, la sécurité c’est toute l’année ! Découvrez : {random.choice(CONTENU_SITE['services'])}."

        if r == "facebook":
            texte += " Rejoignez-nous pour plus de conseils."
        elif r == "instagram":
            texte += " Inspirez-vous avec nos astuces sécurité !"
        elif r == "linkedin":
            texte += " Nos formations pro sont là pour vous."
        elif r == "tiktok":
            texte += " À tester en vidéo !"

        hashtags = ["#Sécurité", "#Prévention", "#PassionPrévention"]
        posts[r] = {"texte": texte, "hashtags": hashtags}

    return jsonify({"postages": posts, "journees_a_venir": journees_a_venir()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
