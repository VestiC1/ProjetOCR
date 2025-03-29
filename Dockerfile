# Étape 1 : Utiliser une image Python officielle
FROM python:3.12-slim

# Étape 2 : Installer Tesseract OCR et ses dépendances système
RUN apt-get update && apt-get install -y tesseract-ocr imagemagick zbar-tools ffmpeg libsm6 libxext6 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Étape 3 : Définir le répertoire de travail dans le conteneur
WORKDIR /App

# Étape 4 : Copier les fichiers nécessaires dans le conteneur
COPY . .

# Étape 5 : Mise à jour de pip
RUN pip install --upgrade pip

# Étape 6 : Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Étape 7 : Installer les dépendances Python
RUN pip install .

# Étape 8 : Exposer le port utilisé par FastAPI
EXPOSE 8000

# Étape 9 : Commande pour exécuter l'application
CMD ["uvicorn", "App.main:app", "--host", "0.0.0.0", "--port", "8000"]