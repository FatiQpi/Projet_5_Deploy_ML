import pandas as pd
import os
import json
from sqlalchemy import create_engine, Column, Integer, JSON, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone
from dotenv import load_dotenv

# Configuration et Connexion
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base = declarative_base()

# On redéfinit la classe pour que ce script soit indépendant
class HistoricalData(Base):
    __tablename__ = "historical_data"
    id = Column(Integer, primary_key=True, index=True)
    employee_profile = Column(JSON, nullable=False)
    target_attrition = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

def inject_data():
    csv_file = "data/attrition_clean.csv"
    
    # Vérification présence fichier
    if not os.path.exists(csv_file):
        print(f" ERREUR : Le fichier '{csv_file}' est introuvable à la racine !")
        return

    print(f" Lecture du fichier {csv_file}...")
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Erreur de lecture CSV : {e}")
        return
    
    print(f" Début de l'injection de {len(df)} employés vers Supabase...")
    
    buffer = []
    count = 0
    
    for index, row in df.iterrows():
        # Vérification de la présence de la colonne 'cible'
        if 'cible' not in row:
            print(f"ERREUR Ligne {index} : Colonne 'cible' introuvable !")
            continue 

        target = int(row['cible'])
        profile_data = row.drop('cible').to_dict()

        # Création de l'objet SQL
        record = HistoricalData(
            target_attrition=target,
            employee_profile=profile_data
        )
        buffer.append(record)
        count += 1
        
        # Envoi par paquets de 50 pour optimiser
        if len(buffer) >= 50:
            session.add_all(buffer)
            session.commit()
            buffer = []
            print(f"   ... {count} lignes insérées")

    # Envoyer le reste
    if buffer:
        session.add_all(buffer)
        session.commit()

    print(f"TERMINÉ ! {count} lignes ont été ajoutées à la base de données.")

if __name__ == "__main__":
    inject_data()