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


def db_connect():
    return engine.connect()

def db_close(conn):
    conn.close()


def create_clients(conn):
    conn.execute(text(f"""
        CREATE TABLE steve.clients (
            nom varchar(50) NULL,
            mail varchar(50) NOT NULL,
            date_de_naissance date NULL,
            sexe varchar(1) NULL,
            adresse varchar(200) NULL,
            CONSTRAINT clients_pk PRIMARY KEY (mail)
        );
    """)
    )
    conn.commit()

def create_factures(conn):
    conn.execute(text(f"""
        CREATE TABLE steve.factures (
            numero_facture varchar(14) NOT NULL,
            creation_date timestamp NULL,
            total float8 NULL,
            mail varchar(50) NULL,
            CONSTRAINT factures_pk PRIMARY KEY (numero_facture),
            CONSTRAINT factures_clients_fk FOREIGN KEY (mail) REFERENCES steve.clients(mail)
        );
    """)
    )
    conn.commit()

def create_factures_produits(conn):
    conn.execute(text(f"""
        CREATE TABLE steve.factures_produits (
            id serial NOT NULL,
            numero_facture varchar(14) NULL,
            produit varchar(60) NULL,
            quantité int4 NULL,
            prix_unitaire float8 NULL,
            CONSTRAINT produits_pk PRIMARY KEY (id),
            CONSTRAINT produits_factures_fk FOREIGN KEY (numero_facture) REFERENCES steve.factures(numero_facture)
        );
    """)
    )
    conn.commit()

def create_all(conn):
    create_clients(conn)
    create_factures(conn)
    create_factures_produits(conn)


def drop_clients(conn):
    conn.execute(text(f"""
        DROP TABLE steve.clients cascade;
    """))
    conn.commit()

def drop_factures(conn):
    conn.execute(text(f"""
        DROP TABLE steve.factures cascade;
    """))
    conn.commit()

def drop_factures_produits(conn):
    conn.execute(text(f"""
        DROP TABLE steve.factures_produits cascade;
    """))
    conn.commit()

def drop_all(conn):
    drop_clients(conn)
    drop_factures(conn)
    drop_factures_produits(conn)


def add_clients(conn, nom, mail, datedenaissance, sexe, adresse):
    conn.execute(text(f"""
            INSERT INTO steve.clients (nom, mail, date_de_naissance, sexe, adresse)
                VALUES (:nom, :mail, :date_de_naissance, :sexe, :adresse)
            ON conflict (mail) do update 
            set adresse=:adresse;
        """),
    {"nom":nom, "mail":mail, "date_de_naissance":datedenaissance, "sexe":sexe, "adresse":adresse})
    conn.commit()

def add_factures(conn, numerofacture, creationdate, total, mail):
    conn.execute(text(f"""
            INSERT INTO steve.factures (numero_facture, creation_date, total, mail)
                VALUES (:numero_facture, :creation_date, :total, :mail)
            ON conflict (numero_facture) do update 
            set total=:total, mail=:mail;
        """), 
    {"numero_facture":numerofacture, "creation_date":creationdate, "total":total, "mail":mail}
    )
    conn.commit()

def add_factures_produits(conn, numero_facture, produit, quantite, prix_unitaire ):
    conn.execute(text("""
            INSERT INTO steve.factures_produits (numero_facture, produit, quantité, prix_unitaire)
                VALUES (:numero_facture, :produit, :quantité, :prix_unitaire)
        """),
    {"numero_facture":numero_facture, "produit":produit, "quantité":quantite, "prix_unitaire":prix_unitaire}                 
    )
    conn.commit()


if __name__ == "__main__":
    # Création des tables
    conn = db_connect()

    #create_factures_produits(conn)
    #drop_all(conn)
    #create_all(conn)

    db_close(conn)