
import json
from datetime import datetime, timedelta

jours = {
    "02-08": "Journée de la prévention routière",
    "05-08": "Journée mondiale de la bière",
    "08-08": "Journée du chat"
}

with open("journees.json", "w", encoding="utf-8") as f:
    json.dump(jours, f, ensure_ascii=False, indent=2)
print("journees.json mis à jour")
