import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.passion-prevention.com"

def extraire_contenu_site():
    contenu = {"produits": [], "services": [], "conseils": []}
    try:
        r = requests.get(URL)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        for h2 in soup.find_all('h2'):
            texte = h2.get_text(strip=True)
            if len(texte) > 10:
                contenu["produits"].append(texte)

        for p in soup.find_all('p'):
            texte = p.get_text(strip=True)
            if 20 < len(texte) < 150:
                contenu["conseils"].append(texte)

        for key in contenu:
            contenu[key] = list(set(contenu[key]))[:30]

        with open('contenu_site.json', 'w', encoding='utf-8') as f:
            json.dump(contenu, f, ensure_ascii=False, indent=2)

        print("Contenu extrait et sauvegardé dans contenu_site.json")
    except Exception as e:
        print("Erreur scraping :", e)

if __name__ == "__main__":
    extraire_contenu_site()
