import os
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

# Charger les variables d'environnement du fichier .env
load_dotenv()

# Création URL avec la fonction sqlalchemy :
POSTGRES_URI = URL.create(
    drivername = "postgresql+psycopg2",   
    username   = os.environ.get('DB_USER'),
    password   = os.environ.get('DB_PASSWORD'),
    host       = os.environ.get('DB_HOST'),
    port       = os.environ.get('DB_PORT', 5432),
    database   = os.environ.get('DB_NAME')
)

engine = create_engine(POSTGRES_URI)
conn = engine.connect()

def add_factures(no, dt, total, mail):
    conn.execute(text(f"""
INSERT INTO steve.factures (numerofact, creationdate, total, mail)
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