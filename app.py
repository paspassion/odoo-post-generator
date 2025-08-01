import os
from flask import Flask, request, jsonify
from serpapi import GoogleSearch
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "91ab2470b52f1166f64f1267c08e3a3792c1df343c4936a597fb3e0a762c66f3")

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
    mois = data.get('mois', 'août')
    reseaux = data.get('reseaux', [])

    postages = {}
    for reseau in reseaux:
        mot_cle = "sécurité"
        hashtags = rechercher_hashtags(mot_cle, reseau)
        texte = f"Post automatique pour {reseau} en {mois} – restez vigilant !"
        postages[reseau] = {
            "texte": texte,
            "hashtags": hashtags
        }
    return jsonify({"postages": postages})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
