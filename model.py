import requests, json, os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Charger les variables d'environnement du fichier .env
load_dotenv()

POSTGRES_URI = os.getenv("POSTGRES_URI")

engine = create_engine(POSTGRES_URI)
conn = engine.connect()

def add_invoice(no, dt, total, mail):
    conn.execute(text(f"""
INSERT INTO steve.invoice (numerofact, creationdate, total, mail)
    VALUES (:numero, :date, :total, :mail)
ON conflict (numerofact) do update 
set total=:total, mail=:mail;
"""), {"numero":no, "date":dt, "total":total, "mail":mail})
    conn.commit()

def add_clients(nom, mail, datedenaissance, sexe, adresse):
    conn.execute(text(f"""
INSERT INTO steve.clients (nom, mail, datedenaissance, sexe, adresse)
    VALUES (:nom, :mail, :datedenaissance, :sexe, :adresse)
ON conflict (mail) do update 
set adresse=:adresse;
    """), {"nom":nom, "mail":mail, "datedenaissance":datedenaissance, "sexe":sexe, "adresse":adresse})
    conn.commit()