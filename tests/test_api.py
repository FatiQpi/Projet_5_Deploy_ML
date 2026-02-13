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

# --- TEST FONCTIONNEL POST  ---
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

    # --- TEST FONCTIONNEL GET ---
def test_get_log_scenario():
    """
    Scénario complet : 
    On fait une prédiction
    On récupère l'ID du log
    On interroge la route GET /logs/{id} pour vérifier que c'est bien sauvegardé
    """
    #  Prédiction
    payload = {
        "age": 45,
        "revenu_mensuel": 8000.0,
        "nombre_experiences_precedentes": 5,
        "annees_dans_l_entreprise": 10,
        "satisfaction_employee_environnement": 4,
        "note_evaluation_precedente": 3,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 4,
        "satisfaction_employee_equilibre_pro_perso": 3,
        "note_evaluation_actuelle": 3,
        "nombre_participation_pee": 1,
        "nb_formations_suivies": 3,
        "distance_domicile_travail": 5.0,
        "annees_depuis_la_derniere_promotion": 2,
        "niveau_education": 4,
        "Ratio_Fidelite": 0.1,
        "Ratio_Stagnation": 0.0,
        "genre": "Homme",
        "statut_marital": "Marié",
        "departement": "Ventes",
        "poste": "Manager",
        "heure_supplementaires": "Non",
        "domaine_etude": "Commerce",
        "ayant_enfants": "Oui",
        "frequence_deplacement": "Rarement"
    }
    
    # POST
    response_post = client.post("/predict", json=payload)
    assert response_post.status_code == 200
    data = response_post.json()
    
    # On récupère l'ID
    log_id = data["log_id"]
    
    # Vérification GET
    response_get = client.get(f"/logs/{log_id}")
    assert response_get.status_code == 200
    
    # On vérifie le contenu
    log_data = response_get.json()
    assert log_data["id"] == log_id
    assert log_data["prediction"] in ["Départ", "Reste"]