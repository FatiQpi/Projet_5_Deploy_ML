import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Initialisation
app = FastAPI(
    title="Technova API Attrition",
    description="API de prédiction de départ employé pour Technova",
    version="1.0.0"
)

# Chargement du modèle
try:
    model = joblib.load("data/new_model_attrition.joblib")
except Exception as e:
    print(f"ERREUR : Impossible de charger le modèle. {e}")
    model = None

# Modèle de Données 
class EmployeeData(BaseModel):
    # --- Variables Numériques ---
    age: int = Field(..., example=41, description="Age de l'employé")
    revenu_mensuel: float = Field(..., example=5993.0)
    nombre_experiences_precedentes: int = Field(..., example=8)
    annees_dans_l_entreprise: int = Field(..., example=6)
    
    # Satisfaction & Notes (1 à 4)
    satisfaction_employee_environnement: int = Field(..., example=2)
    note_evaluation_precedente: int = Field(..., example=3)
    satisfaction_employee_nature_travail: int = Field(..., example=4)
    satisfaction_employee_equipe: int = Field(..., example=4)
    satisfaction_employee_equilibre_pro_perso: int = Field(..., example=1)
    note_evaluation_actuelle: int = Field(..., example=3)
    
    # Autres Variables Numériques
    nombre_participation_pee: int = Field(..., example=1)
    nb_formations_suivies: int = Field(..., example=0)
    distance_domicile_travail: float = Field(..., example=1.0)
    annees_depuis_la_derniere_promotion: int = Field(..., example=0)
    niveau_education: int = Field(..., example=2, description="Niveau d'étude (1-5)")
    
    # Ratios
    Ratio_Fidelite: float = Field(..., example=0.15)
    Ratio_Stagnation: float = Field(..., example=0.0)

    # --- Variables Catégorielles ---
    genre: str = Field(..., example="Femme")
    statut_marital: str = Field(..., example="Célibataire")
    departement: str = Field(..., example="Ventes")
    poste: str = Field(..., example="Cadre commercial")
    heure_supplementaires: str = Field(..., example="Oui")
    domaine_etude: str = Field(..., example="Sciences de la vie")
    ayant_enfants: str = Field(..., example="Oui")
    frequence_deplacement: str = Field(..., example="Rarement")

# Endpoints
@app.get("/")
def read_root():
    return {"status": "online", "message": "API Technova Ready"}

@app.post("/predict")
def predict(employee: EmployeeData):
    if not model:
        raise HTTPException(status_code=500, detail="Modèle non chargé")
    
    try:
        # Conversion Pydantic -> DataFrame
        input_data = employee.model_dump()
        df = pd.DataFrame([input_data])
        
        # Prédiction
        prediction = model.predict(df)
        probas = model.predict_proba(df)
        
        result = "Départ" if prediction[0] == 1 else "Reste"
        score = probas[0][1] # Probabilité de départ

        return {
            "prediction": result,
            "probability_depart": round(float(score), 4),
            "alert": bool(score > 0.5) # Alerte si probabilité > 50%
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur de traitement : {str(e)}")