#!/home/deck/.openclaw/workspace/skills/plantnet-identify/venv/bin/python3
"""
E*NKI PlantNet Identification Script
Identifies plants via Pl@ntNet API from image URL or local file.
Usage: python3 identify.py <image_url_or_path> [organ] [lang]
"""

import sys
import os
import json
import requests
from pathlib import Path

API_KEY = os.environ.get("PLANTNET_API_KEY")
API_URL = "https://my-api.plantnet.org/v2/identify/all"

TOXIC_FAMILIES = ["Solanaceae", "Ranunculaceae", "Euphorbiaceae", "Apocynaceae", "Araceae"]

BIODYNAMIC_TYPES = {
    "root": ["Apiaceae", "Amaryllidaceae", "Asparagaceae"],
    "fruit": ["Solanaceae", "Cucurbitaceae", "Rosaceae", "Fabaceae"],
    "flower": ["Asteraceae", "Lamiaceae", "Boraginaceae"],
    "leaf": ["Brassicaceae", "Chenopodiaceae", "Amaranthaceae"],
}

def get_plant_type(family):
    for plant_type, families in BIODYNAMIC_TYPES.items():
        if family in families:
            return plant_type
    return "leaf"

def generate_enki_advice(result):
    species = result.get("species", "")
    family = result.get("family", "")
    plant_type = get_plant_type(family)
    common = result.get("common_name", species)

    advice = f"{common} identifié(e). "
    advice += f"Plante de type '{plant_type}' selon la biodynamie. "

    type_advice = {
        "root": "Privilégiez les interventions (semis, récolte, travail du sol) les jours Racine du calendrier lunaire. Évitez l'arrosage excessif.",
        "fruit": "Les jours Fruit sont idéaux pour la récolte et la taille. Favorisez un sol riche en compost mûr.",
        "flower": "Travaillez cette plante lors des jours Fleur. Attention aux gelées tardives — protégez les bourgeons.",
        "leaf": "Les jours Feuille favorisent la croissance foliaire. Arrosez tôt le matin, jamais en plein soleil.",
    }
    advice += type_advice.get(plant_type, "Observez les cycles lunaires pour optimiser vos interventions.")
    return advice

def identify_from_url(image_url, organ="auto", lang="fr"):
    if not API_KEY:
        print(json.dumps({"error": "API_KEY_MISSING", "message": "Définissez PLANTNET_API_KEY dans vos variables d'environnement. Inscription gratuite sur https://my.plantnet.org/"}))
        sys.exit(1)

    params = {
        "api-key": API_KEY,
        "lang": lang,
        "include-related-images": False,
    }

    # Handle local file vs URL
    if Path(image_url).exists():
        with open(image_url, "rb") as f:
            files = [("images", (Path(image_url).name, f, "image/jpeg"))]
            data = {"organs": [organ if organ != "auto" else "auto"]}
            response = requests.post(API_URL, params=params, files=files, data=data, timeout=30)
    else:
        # URL-based identification
        data = {
            "images": [image_url],
            "organs": [organ if organ != "auto" else "auto"],
        }
        response = requests.post(API_URL, params=params, json=data, timeout=30)

    if response.status_code == 404:
        print(json.dumps({"error": "NO_MATCH", "message": "Aucune plante reconnue. Essayez une photo plus nette ou un autre angle."}))
        sys.exit(0)

    if response.status_code == 429:
        print(json.dumps({"error": "RATE_LIMIT", "message": "Limite de 500 requêtes/jour atteinte. Réessayez demain."}))
        sys.exit(0)

    if response.status_code != 200:
        print(json.dumps({"error": "API_ERROR", "message": f"Erreur API PlantNet: {response.status_code}"}))
        sys.exit(1)

    data = response.json()
    results = data.get("results", [])

    if not results:
        print(json.dumps({"error": "NO_MATCH", "message": "Aucune correspondance trouvée."}))
        sys.exit(0)

    best = results[0]
    species_info = best.get("species", {})
    species_name = species_info.get("scientificNameWithoutAuthor", "Unknown")
    common_names = species_info.get("commonNames", [])
    common_name = common_names[0] if common_names else species_name
    family = species_info.get("family", {}).get("scientificNameWithoutAuthor", "")
    score = round(best.get("score", 0) * 100, 1)
    gbif_id = species_info.get("gbif", {}).get("id")
    gbif_link = f"https://www.gbif.org/species/{gbif_id}" if gbif_id else None

    is_toxic = family in TOXIC_FAMILIES
    is_edible = family in ["Rosaceae", "Fabaceae", "Apiaceae", "Brassicaceae", "Cucurbitaceae"]

    top_matches = [
        {
            "species": r.get("species", {}).get("scientificNameWithoutAuthor", ""),
            "score": round(r.get("score", 0) * 100, 1)
        }
        for r in results[:3]
    ]

    result = {
        "species": species_name,
        "common_name": common_name,
        "confidence": score,
        "family": family,
        "gbif_link": gbif_link,
        "edible": is_edible,
        "toxic": is_toxic,
        "top_matches": top_matches,
        "low_confidence": score < 60,
    }

    result["enki_advice"] = generate_enki_advice(result)

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "USAGE", "message": "Usage: python3 identify.py <image_url_or_path> [organ] [lang]"}))
        sys.exit(1)

    image_input = sys.argv[1]
    organ = sys.argv[2] if len(sys.argv) > 2 else "auto"
    lang = sys.argv[3] if len(sys.argv) > 3 else "fr"

    identify_from_url(image_input, organ, lang)
