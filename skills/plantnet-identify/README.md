# 🌿 plantnet-identify — E*NKI Plant Recognition Skill

Skill OpenClaw pour E*NKI permettant l'identification de plantes et le diagnostic agricole via l'API Pl@ntNet.

## Installation

1. Obtenir une clé API gratuite sur [my.plantnet.org](https://my.plantnet.org/) (500 req/jour, sans carte bancaire)

2. Cloner dans ton workspace skills :
```bash
cd ~/.openclaw/workspace/skills/
git clone https://github.com/eNudimmud/enki-openclaw/skills/plantnet-identify
```

3. Configurer la clé API dans `~/.openclaw/openclaw.json` :
```json
{
  "skills": {
    "entries": {
      "plantnet-identify": {
        "env": {
          "PLANTNET_API_KEY": "ta-clé-ici"
        }
      }
    }
  }
}
```

4. Installer la dépendance Python :
```bash
pip install requests
```

## Utilisation

Envoie simplement une photo de plante à E*NKI avec un message comme :
- "Qu'est-ce que c'est comme plante ?"
- "Ma tomate a des taches, c'est quoi ?"
- "Identifie cette feuille"

E*NKI se charge du reste — identification, conseils biodynamiques, et croisement avec le calendrier lunaire si le skill lunar est actif.

## Modèle de monétisation

| Service | Prix suggéré | Coût API | Marge |
|---------|-------------|----------|-------|
| Identification simple | 0.50 USDC | 0.00 (free tier) | 100% |
| Diagnostic complet | 1.00 USDC | 0.00 | 100% |
| Rapport mensuel plantes | 5.00 USDC | 0.00 | 100% |

## Limites

- 500 requêtes/jour en free tier — suffisant pour démarrer
- Photos floues ou en mauvaise lumière → résultats moins précis
- Pl@ntNet couvre >30 000 espèces végétales

## Licence

MIT — cohérent avec la philosophie E*NKI de partage souverain.
