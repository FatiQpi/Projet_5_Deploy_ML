---
title: Technova API - Employee Attrition
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# 🔮 API de Prédiction d'Attrition RH (Technova)

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](./tests)

## Description

Ce projet expose une API de Machine Learning capable de prédire le risque de départ d'un employé (**Attrition**) pour l'entreprise **Technova**. Il s'inscrit dans le cadre du Projet 5 de la formation AI Engineer.

L'objectif est de fournir un outil d'aide à la décision pour les équipes RH, permettant d'identifier les profils à risque afin de proposer des actions de rétention. L'application stocke également chaque prédiction dans une base de données **PostgreSQL** pour un suivi (monitoring) futur.

🔗 **URL de l'API en production :** [https://huggingface.co/spaces/Fatih09/technova-api](https://huggingface.co/spaces/Fatih09/technova-api)  
📄 **Documentation interactive (Swagger UI) :** [https://fatih09-technova-api.hf.space/docs](https://fatih09-technova-api.hf.space/docs)
👉 **[Voir la fiche technique du modèle (Model Card)](MODEL_CARD.md)** pour les détails sur la performance et les biais.

---

## Architecture et Choix Techniques

* **API :** FastAPI (Python)
* **ML Engine :** Pipeline Scikit-learn (Préprocessing + XGBoost optimisé pour le Rappel)
* **Database :** PostgreSQL (Hébergé sur Supabase)
* **DevOps :** Docker & GitHub Actions (CI/CD)
* **Hébergement :** Hugging Face Spaces

### Structure du projet
* `app/` : Code source de l'API (`main.py`) et logique métier.
* `data/` : Contient le pipeline complet entraîné (`model.joblib`) incluant le préprocesseur et le modèle.
* `tests/` : Tests unitaires et fonctionnels (Pytest).
* `Dockerfile` : Configuration pour la conteneurisation.
* `requirements.txt` : Liste des dépendances Python.

---

## Installation et Démarrage Local

### Prérequis
* **Python 3.11+**
* Git
* Une URL de base de données PostgreSQL (ex: Supabase)

### 1. Cloner le projet
```bash
git clone [https://github.com/FatiQpi/Projet_5_Deploy_ML.git](https://github.com/FatiQpi/Projet_5_Deploy_ML.git)
cd Projet_5_Deploy_ML
```

### 2. Créer l'environnement virtuel

```Bash
python3 -m venv .venv
source .venv/bin/activate  # Sur Mac/Linux
# .venv\Scripts\activate   # Sur Windows
```

### 3. Installer les dépendances

```Bash
pip install -r requirements.txt
```

### 4. Configuration (.env) ⚠️ Important

Créez un fichier .env à la racine du projet pour connecter la base de données. Note : Utilisez le port 6543 (Mode Transaction Pooler) pour la compatibilité cloud.

```Plaintext
DATABASE_URL="postgresql://postgres.xvcehnhrcdoxlzeliwap:[YOUR-PASSWORD]@aws-1-eu-west-1.pooler.supabase.com:6543/postgres"
```
Remplacez [YOUR-PASSWORD] par le mot de passe que vous avez défini lors de la création de votre cluster de base de données (ex: Supabase).

Note: si vous utilisez Supabase, le mot de passe est celui saisi lors de la création du projet. Si vous l'avez oublié, vous pouvez le réinitialiser dans les paramètre de la base de données.

### 5.1 Initialiser la Base de Données

Générez l'architecture des tables (logs et historique) en exécutant le script de création:

```Bash
python create_db.py
```

### 5.2 Injecter la base de données Technova

Afin d'initialiser la base avec l'historique de l'entreprise et de pouvoir lancer des prédictions sur les collaborateurs actuels,
injectez les données des employés de Technova:

```bash
python inject_data.py
```

### 6. Lancer l'API

**En Local**
```Bash
uvicorn app.main:app --reload
```
L'API sera accessible sur http://127.0.0.1:8000. 
La documentation interactive est disponible sur http://127.0.0.1:8000/docs.

**En Production (Hugging Face)**

L'espace du projet sera accessible sur https://huggingface.co/spaces/Fatih09/technova-api
La documentation interactive (Swagger): https://fatih09-technova-api.hf.space/docs


#### Exemple d'utilisation 

L'API attend les données au format JSON spécifique à Technova.
Requête type(cURL):

```Bash
curl -X 'POST' \
  'https://fatih09-technova-api.hf.space/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "age": 41,
  "revenu_mensuel": 5993,
  "nombre_experiences_precedentes": 8,
  "annees_dans_l_entreprise": 6,
  "satisfaction_employee_environnement": 2,
  "note_evaluation_precedente": 3,
  "satisfaction_employee_nature_travail": 4,
  "satisfaction_employee_equipe": 4,
  "satisfaction_employee_equilibre_pro_perso": 1,
  "note_evaluation_actuelle": 3,
  "nombre_participation_pee": 1,
  "nb_formations_suivies": 0,
  "distance_domicile_travail": 1,
  "annees_depuis_la_derniere_promotion": 0,
  "niveau_education": 2,
  "Ratio_Fidelite": 0.15,
  "Ratio_Stagnation": 0,
  "genre": "Femme",
  "statut_marital": "Célibataire",
  "departement": "Ventes",
  "poste": "Cadre commercial",
  "heure_supplementaires": "Oui",
  "domaine_etude": "Sciences de la vie",
  "ayant_enfants": "Oui",
  "frequence_deplacement": "Rarement"
}'
```

Réponse attendue:

```JSON
{
  "prediction": "Reste",
  "probability_depart": 0.3782,
  "alert": false,
  "log_id": 4
}
```

## Tests et Qualité du Code
Le projet dispose d'une suite de tests automatisés couvrant l'API et l'accès aux données.

```Bash
# Lancer les tests
python -m pytest

# Vérifier la couverture (Doit être > 80%)
python -m pytest --cov=app tests/
```

## Maintenance et Monitoring
Un protocole de maintenance est établi pour garantir la fiabilité du modèle dans le temps :

* **Monitoring des Logs :** Vérifier périodiquement dans PostgreSQL la distribution des prédictions (via requêtes SQL) pour détecter une éventuelle dérive.

```SQL
SELECT prediction, COUNT(*) as nombre_employes FROM prediction_logs GROUP BY prediction;
```

* **Réentraînement :** Si la performance baisse ou si de nouvelles données sont disponibles, le modèle est réentraîné localement via le notebook Classifiez automatiquement des informations-P4.ipynb. Le nouveau fichier pipeline model.joblib est ensuite déployé.
* **Mise à jour API :** Toute modification du code sur la branche main et develop entraîne une exécution automatique des tests et un redéploiement via le pipeline CI/CD.

#### Auteur
Fatih B. - Étudiant AI Engineer