import os
from flask import Flask, request, jsonify
from serpapi import GoogleSearch
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "TA_CLE_SERPAPI_ICI")

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
    mois = data.get('mois', '08')
    annee = data.get('annee', '2025')
    reseaux = data.get('reseaux', [])

    evenements = {
        "03": "Journée internationale du droit des femmes",
        "09": "Journée internationale du secourisme",
        "10": "Mois de la sensibilisation au cancer du sein",
    }

    evenement_du_mois = evenements.get(mois, None)

    postages = {}
    for reseau in reseaux:
        texte = f"Post automatique pour {reseau} en {mois}/{annee}."
        if evenement_du_mois:
            texte += f" C’est le moment de célébrer : {evenement_du_mois}."
        else:
            texte += " Restez vigilants toute l'année sur vos thématiques sécurité."

        hashtags = rechercher_hashtags("sécurité", reseau)

        postages[reseau] = {
            "texte": texte,
            "hashtags": hashtags
        }

    return jsonify({"postages": postages})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
