import pytest
from fastapi.testclient import TestClient
from app.main import app

# Client de test 
client = TestClient(app)

# --- TEST UNITAIRE ---
def test_read_root():
    """Vérifie juste que l'API fonctionne"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

# --- TEST FONCTIONNEL  ---
def test_predict_valid_employee():
    """Vérifie le cycle complet : Données -> Prédiction -> Réponse"""
    payload = {
        "age": 30,
        "revenu_mensuel": 4000.0,
        "nombre_experiences_precedentes": 2,
        "annees_dans_l_entreprise": 5,
        "satisfaction_employee_environnement": 3,
        "note_evaluation_precedente": 3,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 3,
        "satisfaction_employee_equilibre_pro_perso": 3,
        "note_evaluation_actuelle": 3,
        "nombre_participation_pee": 1,
        "nb_formations_suivies": 2,
        "distance_domicile_travail": 10.0,
        "annees_depuis_la_derniere_promotion": 1,
        "niveau_education": 3,
        "Ratio_Fidelite": 0.1,
        "Ratio_Stagnation": 0.2,
        "genre": "Femme",
        "statut_marital": "Célibataire",
        "departement": "R&D",
        "poste": "Scientifique",
        "heure_supplementaires": "Non",
        "domaine_etude": "Sciences",
        "ayant_enfants": "Non",
        "frequence_deplacement": "Rarement"
    }
    
    response = client.post("/predict", json=payload)
    
    # On veut un statut 200 OK
    assert response.status_code == 200
    # On veut une prédiction (Départ ou Reste)
    assert response.json()["prediction"] in ["Départ", "Reste"]
    # On vérifie que l'alerte est un booléen
    assert isinstance(response.json()["alert"], bool)

# --- TEST ROBUSTESSE (Cas d'erreur 1 : Donnée manquante) ---
def test_predict_missing_field():
    """Si on oublie l'âge, l'API doit refuser proprement"""
    payload = {
        "revenu_mensuel": 4000.0
    }
    response = client.post("/predict", json=payload)
    # 422 = Erreur de validation Pydantic
    assert response.status_code == 422 

# --- TEST ROBUSTESSE (Cas d'erreur 2 : Mauvais type) ---
def test_predict_invalid_type():
    """Si on envoie du texte au lieu d'un nombre, l'API doit refuser"""
    payload = {
        "age": "Trente ans", 
        "revenu_mensuel": 4000.0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422