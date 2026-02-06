print("---le fichier est lu---")
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone 
from dotenv import load_dotenv

# Charger le fichier .env depuis la racine
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(" ERREUR : Variable DATABASE_URL introuvable!")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print("Connexion à Supabase en cours...")

Base = declarative_base()
engine = create_engine(DATABASE_URL)

# Définition des Tables 

class HistoricalData(Base):
    __tablename__ = "historical_data"
    id = Column(Integer, primary_key=True, index=True)
    employee_profile = Column(JSON, nullable=False)
    target_attrition = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class PredictionLogs(Base):
    __tablename__ = "prediction_logs"
    id = Column(Integer, primary_key=True, index=True)
    # CORRECTION ICI 👇
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    input_data = Column(JSON, nullable=False)
    prediction = Column(String, nullable=False)
    probability = Column(Float, nullable=False)
    alert = Column(Boolean, default=False)

# Exécution
if __name__ == "__main__":
    try:
        print("Création des tables...")
        Base.metadata.create_all(bind=engine)
        print("Les tables sont créées sur Supabase !")
    except Exception as e:
        print(f" ERREUR : {e}")