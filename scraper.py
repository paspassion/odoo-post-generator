
import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.passion-prevention.com/shop"
def extraire_site():
    contenu = {"produits": [], "services": [], "conseils": []}
    r = requests.get(URL)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for h6 in soup.find_all("h6"):
        text = h6.get_text(strip=True)
        if text:
            contenu["produits"].append(text)
    r2 = requests.get("https://www.passion-prevention.com/formation")
    soup2 = BeautifulSoup(r2.text, "html.parser")
    for li in soup2.find_all("li"):
        txt = li.get_text(strip=True)
        if "formation" in txt.lower():
            contenu["services"].append(txt)
    r3 = requests.get("https://www.passion-prevention.com/blog/1")
    soup3 = BeautifulSoup(r3.text, "html.parser")
    for titre in soup3.find_all("h1"):
        contenu["conseils"].append(titre.get_text(strip=True))
    for key in contenu:
        contenu[key] = list(set(contenu[key]))[:30]
    with open("contenu_site.json", "w", encoding="utf-8") as f:
        json.dump(contenu, f, ensure_ascii=False, indent=2)
    print("contenu_site.json mis à jour")

if __name__ == "__main__":
    extraire_site()
