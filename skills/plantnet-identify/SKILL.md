---
name: plantnet-identify
description: Identify plants, detect diseases, and provide biodynamic care recommendations using Pl@ntNet API. Supports image URLs and local files. Returns species name, confidence score, care tips aligned with lunar calendar, and treatment recommendations.
emoji: 🌿
version: 1.0.0
homepage: https://github.com/eNudimmud/enki-openclaw
metadata:
  openclaw:
    requires:
      env:
        - PLANTNET_API_KEY
      bins:
        - curl
        - python3
    primaryEnv: PLANTNET_API_KEY
    install:
      - kind: pip
        packages: [requests]
---

# 🌿 Pl@ntNet Plant Identification Skill

E*NKI uses this skill to identify plants from images, diagnose potential issues, and offer biodynamic care recommendations aligned with the lunar calendar.

## When to use this skill

- User sends a photo of a plant and asks "what is this?" or "what's wrong with my plant?"
- User describes symptoms on a plant (yellowing leaves, spots, wilting...)
- User wants care recommendations for a specific plant
- User wants to know if a plant is edible, medicinal, or toxic

## How to invoke

```bash
{baseDir}/scripts/identify.py <image_url_or_path> [organ] [lang]
```

**organ** (optional): `leaf`, `flower`, `fruit`, `bark`, `auto` (default: `auto`)
**lang** (optional): `fr`, `en`, `es`, `de`, `pt` (default: `fr`)

The script uses its own venv with `requests` installed.

## Usage Examples

From image URL:
```bash
python3 {baseDir}/scripts/identify.py "https://example.com/plant.jpg" leaf
```

From local file:
```bash
python3 {baseDir}/scripts/identify.py "/path/to/photo.jpg" auto
```

## Response format

The script returns a JSON object:

```json
{
  "species": "Solanum lycopersicum",
  "common_name": "Tomato",
  "confidence": 94.2,
  "family": "Solanaceae",
  "gbif_link": "https://www.gbif.org/species/...",
  "edible": true,
  "toxic": false,
  "top_matches": [
    {"species": "Solanum lycopersicum", "score": 0.942},
    {"species": "Solanum melongena", "score": 0.041}
  ],
  "enki_advice": "Tomate détectée. Plante racine selon le calendrier biodynamique..."
}
```

## E*NKI behavior instructions

When this skill returns a result:

1. **Announce the identification clearly**: species name + common name + confidence score
2. **Cross with the lunar calendar** if the lunar skill is active: is today a good day for this plant type (root/flower/fruit/leaf)?
3. **Give biodynamic care advice** tailored to E*NKI's philosophy — no synthetic chemicals, respect natural cycles
4. **Flag toxicity prominently** if `toxic: true` — always warn the user
5. **If confidence < 60%**, say so and ask the user for a clearer photo or different organ

## Error handling

- `API_KEY_MISSING` → Tell user to set PLANTNET_API_KEY environment variable (free at identify.plantnet.org)
- `IMAGE_UNREACHABLE` → Ask user to send the image directly or verify the URL
- `NO_MATCH` → Apologize, suggest retaking photo in better light or different angle
- `RATE_LIMIT` → Pl@ntNet free tier is 500 req/day. If hit, notify user and retry tomorrow

## API Details

- **Endpoint**: `https://my-api.plantnet.org/v2/identify/all`
- **Free tier**: 500 requests/day — no credit card required
- **Signup**: https://my.plantnet.org/
- **Supported organs**: leaf, flower, fruit, bark, habit, other
- **Supported languages**: fr, en, es, de, pt (response language follows user locale)
