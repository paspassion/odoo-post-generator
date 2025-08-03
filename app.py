import os, random, json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__, static_folder='static')  # déclaration du dossier static
CORS(app)

# Clé API (optionnelle si non utilisée)
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "91ab2470b52f1166f64f1267c08e3a3792c1df343c4936a597fb3e0a762c66f3")

# Chargement des données
with open('contenu_site.json', encoding='utf-8') as f:
    CONTENU_SITE = json.load(f)

with open('journees.json', encoding='utf-8') as f:
    JOURNEES = json.load(f)

def journee_du_jour():
    today = datetime.now()
    return JOURNEES.get(today.strftime("%d-%m"))

from datetime import datetime, timedelta

def journees_a_venir(n=5):
    today = datetime.now()
    resultats = []
    for i in range(1, 31):  # 30 prochains jours
        d = today + timedelta(days=i)
        cle = d.strftime("%d-%m")  # format '02-08'
        if cle in JOURNEES:
            resultats.append({
                "date": d.strftime("%d/%m/%Y"),  # format lisible
                "evenement": JOURNEES[cle]
            })
            if len(resultats) >= n:
                break
    return resultats


# ANCIEN MOTEUR SUPPRIMÉ

def generate_rich_post(product):
    import random
    titre = product["title"]
    desc = product["description"][:200].strip()

    intro = random.choice([
        f"🔴 POST SÉCURITÉ – {titre}",
        f"🛡️ Focus produit : {titre}",
        f"🎯 Mettez en avant : {titre}",
        f"🚨 Besoin de prévention ? Découvrez : {titre}"
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

    texte = f"{intro}\n{desc}\n{contexte}\n{appel}\n\n📍 Plus d’infos :\n🔗 www.passion-prevention.com"

    mots = set(texte.lower().replace("’", "'").split())
    base_tags = {"#sécurité", "#prévention", "#PassionPrévention"}
    dyn_tags = {
        f"#{m.strip('.,!?').lower()}"
        for m in mots
        if len(m) > 4 and m[0].isalpha() and not m.startswith("www")
    }

    hashtags = list((base_tags | dyn_tags) - {"#https", "#www", "#com"})
    return {
        "reseau": "multi",
        "titre": titre,
        "texte": texte,
        "hashtags": sorted(hashtags)[:12]
    }


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

# ✅ Route principale pour servir index.html
@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

# ✅ Démarrage de l'application (compatible Render)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)