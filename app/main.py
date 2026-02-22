import pandas as pd
import joblib
import os
import json
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, JSON, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime, timezone
from dotenv import load_dotenv

# --- CONFIGURATION DE LA BASE DE DONNÉES ---
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Création du moteur de connexion
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Définition de la table de logs des prédictions
class PredictionLogs(Base):
    __tablename__ = "prediction_logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    input_data = Column(JSON)
    prediction = Column(String)
    probability = Column(Float)
    alert = Column(Boolean)

# Définition de la table historique des données d'employés
class HistoricalData(Base):
    __tablename__ = "historical_data"
    id = Column(Integer, primary_key=True, index=True)
    employee_profile = Column(JSON, nullable=False)
    target_attrition = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# Fonction utilitaire pour gérer la session DB 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- INITIALISATION API ---
app = FastAPI(
    title="Technova API Attrition",
    description="API de prédiction de départ employé pour Technova (avec Logging)",
    version="1.0.0"
)

# Chargement du modèle
try:
    model = joblib.load("data/new_model_attrition.joblib")
except Exception as e:
    print(f"ERREUR : Impossible de charger le modèle. {e}")
    model = None

# Modèle de Données (INPUT)
class EmployeeData(BaseModel):
    # --- Variables Numériques ---
    age: int = Field(..., example=41, description="Age de l'employé")
    revenu_mensuel: float = Field(..., example=5993.0)
    nombre_experiences_precedentes: int = Field(..., example=8)
    annees_dans_l_entreprise: int = Field(..., example=6)
    
    # Satisfaction & Notes
    satisfaction_employee_environnement: int = Field(..., example=2)
    note_evaluation_precedente: int = Field(..., example=3)
    satisfaction_employee_nature_travail: int = Field(..., example=4)
    satisfaction_employee_equipe: int = Field(..., example=4)
    satisfaction_employee_equilibre_pro_perso: int = Field(..., example=1)
    note_evaluation_actuelle: int = Field(..., example=3)
    
    # Divers
    nombre_participation_pee: int = Field(..., example=1)
    nb_formations_suivies: int = Field(..., example=0)
    distance_domicile_travail: float = Field(..., example=1.0)
    annees_depuis_la_derniere_promotion: int = Field(..., example=0)
    niveau_education: int = Field(..., example=2)
    
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

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"status": "online", "message": "API Technova Ready & Connected to DB"}

@app.post("/predict")
def predict(employee: EmployeeData, db: Session = Depends(get_db)):
    """
    Reçoit les données employé, prédit le départ, et enregistre le tout en base de données.
    """
    if not model:
        raise HTTPException(status_code=500, detail="Modèle non chargé")
    
    try:
        # Conversion Pydantic -> DataFrame
        input_data = employee.model_dump()
        df = pd.DataFrame([input_data])
        
        # Prédiction
        prediction = model.predict(df)
        probas = model.predict_proba(df)
        
        result_text = "Départ" if prediction[0] == 1 else "Reste"
        prob_depart = float(probas[0][1])
        is_alert = bool(prob_depart > 0.5)

        # LOGGING EN BASE DE DONNÉES
        # On crée l'enregistrement
        log_entry = PredictionLogs(
            input_data=input_data,  
            prediction=result_text,
            probability=prob_depart,
            alert=is_alert
        )
        # On l'ajoute à la session et on commit
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry) # On récupère l'ID créé

        # Retour de la réponse API
        return {
            "prediction": result_text,
            "probability_depart": round(prob_depart, 4),
            "alert": is_alert,
            "log_id": log_entry.id #On renvoie l'ID du log pour preuve
        }

    except Exception as e:
        # En cas d'erreur, on log l'erreur dans la console serveur
        print(f"Erreur lors de la prédiction : {e}")
        raise HTTPException(status_code=400, detail=f"Erreur de traitement : {str(e)}")
    
@app.get("/logs/{log_id}")
def get_log(log_id: int, db: Session = Depends(get_db)):
    """
    Récupère un historique de prédiction par son ID.
    Permet de vérifier les données d'entrée et le résultat stocké.
    """
    # Recherche dans la base de données
    log = db.query(PredictionLogs).filter(PredictionLogs.id == log_id).first()
    
    # Si l'ID n'existe pas, on renvoie une erreur 404
    if log is None:
        raise HTTPException(status_code=404, detail="Log introuvable (ID inconnu)")
    
    return log

@app.get("/predict/employee/{emp_id}")
def predict_existing_employee(emp_id: int, db: Session = Depends(get_db)):
    """
    Récupère un employé de la base historique et génère une prédiction.
    """
    if not model:
        raise HTTPException(status_code=500, detail="Modèle non chargé")

    # chercher l'employé dans la base de données historique
    employe = db.query(HistoricalData).filter(HistoricalData.id == emp_id).first()
    
    if not employe:
        raise HTTPException(status_code=404, detail=f"Employé {emp_id} introuvable.")

    try:
        # Récupérer le profil et le mettre dans un DataFrame
        input_data = employe.employee_profile
        df = pd.DataFrame([input_data])
        
        # Prédiction
        prediction = model.predict(df)
        probas = model.predict_proba(df)
        
        result_text = "Départ" if prediction[0] == 1 else "Reste"
        prob_depart = float(probas[0][1])
        is_alert = bool(prob_depart > 0.5)

      # ---  SAUVEGARDE DANS LES LOGS ---
        log_entry = PredictionLogs(
            input_data=input_data,  
            prediction=result_text,
            probability=prob_depart,
            alert=is_alert
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)

        return {
            "id_employe": emp_id,
            "prediction": result_text,
            "probability_depart": round(prob_depart, 4),
            "alert": is_alert,
            "log_id": log_entry.id # On renvoie aussi l'ID du log pour vérifier
        }
    except Exception as e:
        print(f"Erreur sur l'employé existant {emp_id} : {e}")
        raise HTTPException(status_code=400, detail=f"Erreur de traitement : {str(e)}")