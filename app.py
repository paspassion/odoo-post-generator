import os
from datetime import datetime
from flask import Flask, request, jsonify
from serpapi import GoogleSearch
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "TA_CLE_SERPAPI_ICI")

# Dictionnaire des journées mondiales importantes (jour-mois : nom)
JOURNEES_MONDALES = {
    "02-04": "Journée mondiale de sensibilisation à l’autisme",
    "06-11": "Journée mondiale de la prévention des risques professionnels",
    "28-04": "Journée mondiale de la sécurité et de la santé au travail",
    "25-11": "Journée internationale pour l’élimination de la violence à l’égard des femmes",
    # Ajoute d’autres journées au besoin
}

def journee_du_jour():
    today = datetime.now()
    cle = today.strftime("%d-%m")
    return JOURNEES_MONDALES.get(cle, None)

def rechercher_hashtags(mot_cle, reseau):
    query = f"site:{reseau}.com #{mot_cle}"
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": 10
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        hashtags = {}
        for item in results.get("organic_results", []):
            title = item.get("title", "")
            for word in title.split():
                if word.startswith("#"):
                    hashtags[word] = hashtags.get(word, 0) + 1
        sorted_tags = sorted(hashtags.items(), key=lambda x: x[1], reverse=True)
        top_tags = [tag for tag, _ in sorted_tags[:10]]
        return top_tags if top_tags else ["#sécurité", "#prévention"]
    except Exception as e:
        print("Erreur SerpAPI:", e)
        return ["#sécurité", "#prévention"]

@app.route('/api/genere-post', methods=['POST'])
def genere_post():
    data = request.get_json()
    mois = data.get('mois', None)
    annee = data.get('annee', None)
    reseaux = data.get('reseaux', [])

    evenement_du_jour = journee_du_jour()

    postages = {}
    for reseau in reseaux:
        # Texte de base selon jour ou non
        if evenement_du_jour:
            texte = f"Aujourd'hui, c'est {evenement_du_jour} ! Chez Passion Prévention, nous sommes mobilisés pour votre sécurité."
        else:
            texte = "Chez Passion Prévention, votre sécurité est notre priorité toute l'année !"

        # Personnalisation simple par réseau social
        if reseau == "linkedin":
            texte += " Découvrez nos formations et équipements professionnels adaptés."
        elif reseau == "tiktok":
            texte += " Testez nos bornes éthylotest en vidéo ! #fun #sécurité"
        elif reseau == "facebook":
            texte += " Rejoignez notre communauté et restez informés des bonnes pratiques."
        elif reseau == "instagram":
            texte += " Suivez-nous pour des astuces et conseils en prévention."

        hashtags = rechercher_hashtags("sécurité", reseau)

        postages[reseau] = {
            "texte": texte,
            "hashtags": hashtags
        }

    return jsonify({"postages": postages})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
