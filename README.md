# API de Prédiction d'Attrition RH 

Ce projet expose une API de Machine Learning capable de prédire si un employé est susceptible de quitter l'entreprise. Il s'inscrit dans le cadre du Projet 5 de ma formation AI Engineer.

## Description

L'application utilise un modèle **XGBoost** entraîné sur des données RH. Elle permet via une API REST (FastAPI) d'envoyer les caractéristiques d'un employé et de recevoir :
- La prédiction (Départ / Reste).
- La probabilité associée.

## Architecture

- **API :** FastAPI
- **ML Engine :** Scikit-learn, XGBoost
- **Data :** Pandas
- **Gestion de version :** Git & GitHub

## Installation et Démarrage

### Prérequis
- Python 3.9+
- Pip

### 1. Cloner le projet
```bash
git clone https://github.com/FatiQpi/Projet_5_Deploy_ML.git
cd projet_5_deploy_ml
```
### 2. Crée l'environnement virtuel
```bash
python3 -m venv .venv
.venv/bin/activate  # Sur Mac/Linux
.venv\Scripts\activate   # Sur Windows
```
### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```
### 4. Lancer L'API
```bash
uvicorn app.main:app --reload
```
