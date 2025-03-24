import requests, os
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

# Charger les variables d'environnement du fichier .env
load_dotenv()

CONTAINER_URL = os.getenv("CONTAINER_URL")
CONTAINER_SAS = os.getenv("CONTAINER_SAS")

# Dossier où seront stockées les factures
LOCAL_STORAGE = "factures"

def fetch_file_list(year):
    """ Récupère la liste des fichiers PNG pour une année donnée """
    url = f"{CONTAINER_URL}/invoices-{year}?restype=container&comp=list&{CONTAINER_SAS}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Erreur {response.status_code} lors de la récupération des fichiers pour {year}")
        return []
    
    # Parsing XML pour extraire les noms de fichiers
    root = ET.fromstring(response.text)
    files = [blob.find("Name").text for blob in root.findall(".//Blob") if blob.find("Name").text.endswith(".png")]
    print(f"📂 {len(files)} fichiers trouvés pour {year}")
    return files

def download_file(year, file_name):
    """ Télécharge un fichier PNG et l'enregistre dans le bon dossier """
    file_url = f"{CONTAINER_URL}/invoices-{year}/{file_name}?{CONTAINER_SAS}"
    response = requests.get(file_url, stream=True)
    
    if response.status_code == 200:
        os.makedirs(f"{LOCAL_STORAGE}/{year}", exist_ok=True)
        file_path = f"{LOCAL_STORAGE}/{year}/{file_name}"
        
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        
        print(f"✅ Téléchargé : {file_path}")
    else:
        print(f"❌ Erreur {response.status_code} - Impossible de télécharger {file_name}")


def main():
    """ Boucle sur les années et télécharge les fichiers PNG """
    for year in range(2018, 2026):
        print(f"📂 Traitement de l'année {year}...")
        files = fetch_file_list(year)
        for file_name in files:
            download_file(year, file_name)

if __name__ == "__main__":
    main()