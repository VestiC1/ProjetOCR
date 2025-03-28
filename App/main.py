from fastapi import FastAPI, Request, Form, Depends, HTTPException, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

import os
import sys
from pathlib import Path

from App.services.outils import charger_image, pil_to_cv2
from App.services.qr_code import extraction_qrcode
from App.services.segmentation import segmenter_image
from App.services.ocr import extraction_texte
from App.services.parseur import extraction_texte_qrcode, extraction_texte_facture, extraction_texte_table

from datetime import datetime
import statistics

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "webapp/templates"))

FACTURES_DIR = Path(r"C:\Users\steve\Documents\Formation IA\ProjetOCR\ProjetOCR\factures")

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "webapp/static")), name="static")

# Simulation d'une session utilisateur (à remplacer par un vrai système d'authentification)
fake_users_db = {"admin": "password"}
session = {"user": None}

def login_required(request: Request):
    return session["user"]

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("accueil.html", {"request": request, "user": session["user"]})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if fake_users_db.get(username) == password:
        session["user"] = username
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Identifiants incorrects"})

@app.get("/logout")
async def logout():
    session["user"] = None
    return RedirectResponse("/", status_code=303)

@app.get("/factures")
async def view_factures(request: Request, user: str = Depends(login_required)):
    if not session["user"]:
        return templates.TemplateResponse("acces_refuse.html", {"request": request})
    return templates.TemplateResponse("factures.html", {"request": request, "user": user})

@app.get("/ajout_facture")
async def add_facture(request: Request, user: str = Depends(login_required)):
    if not session["user"]:
        return templates.TemplateResponse("acces_refuse.html", {"request": request})
    return templates.TemplateResponse("ajout_facture.html", {"request": request, "user": user})

@app.get("/monitoring")
async def monitoring(request: Request, user: str = Depends(login_required)):
    if not session["user"]:
        return templates.TemplateResponse("acces_refuse.html", {"request": request})
    return templates.TemplateResponse("monitoring.html", {"request": request, "user": user})

# Route pour récupérer la liste des factures
@app.get("/list_factures")
async def list_factures():
    factures = {}
    for year_folder in sorted(FACTURES_DIR.iterdir()):
        if year_folder.is_dir():
            factures[year_folder.name] = [f.name for f in year_folder.iterdir() if f.suffix == ".png"]
    return factures

# Route pour afficher une facture sélectionnée
@app.get("/view_facture/{year}/{filename}")
async def view_facture(year: str, filename: str):
    facture_path = FACTURES_DIR / year / filename
    if not facture_path.exists():
        return {"error": "Facture non trouvée"}
    return FileResponse(facture_path)

def extract_year(filename):
    return filename.split('_')[1]

@app.post("/upload_facture")
async def upload_facture(
    request: Request, 
    file: UploadFile = File(...), 
    user: str = Depends(login_required)
):
    start_time = datetime.now()  # Début du traitement

    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        logs_erreurs.append(f"{datetime.now()} - Erreur : Format non supporté ({file.filename})")
        return JSONResponse(status_code=400, content={"error": "Format de fichier non supporté"})

    upload_dir = Path("factures_upload")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / file.filename
    view_path = f"/view_facture/{extract_year(file.filename)}/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
        image = charger_image(nom_du_fichier=str(file_path))
        segments, rectangles = segmenter_image(image)

        zone1, zone2, zone3 = segments
        data_z1 = extraction_texte(zone1)
        data_z2 = extraction_texte(zone2)
        data_qr = extraction_qrcode(image=pil_to_cv2(zone3))

        texte_qr = extraction_texte_qrcode(data_qr)
        texte1 = extraction_texte_facture(data_z1)
        texte2 = extraction_texte_table(data_z2)

        temps_traitement = (datetime.now() - start_time).total_seconds()

        # Ajouter la facture traitée
        factures_importees.append({
            "nom": file.filename,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "status": "OK",
            "temps_traitement": temps_traitement
        })

        return templates.TemplateResponse("ajout_facture.html", {
            "request": request, 
            "user": user, 
            "file_path": str(view_path),
            "texte_qr": texte_qr,
            "texte1": texte1,
            "texte2": texte2
        })
    
    except Exception as e:
        logs_erreurs.append(f"{datetime.now()} - Erreur lors du traitement de {file.filename}: {str(e)}")

        factures_importees.append({
            "nom": file.filename,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "status": "Échec",
            "temps_traitement": 0
        })

        return templates.TemplateResponse("ajout_facture.html", {
            "request": request, 
            "user": user, 
            "error": f"Erreur de traitement : {str(e)}"
        })

    
# Stockage temporaire des données (à remplacer par une base de données)
factures_importees = []
logs_erreurs = []

@app.get("/monitoring_data")
async def get_monitoring_data():
    if not factures_importees:
        temps_moyen = "Pas encore de données"
    else:
        temps_moyen = round(statistics.mean([facture["temps_traitement"] for facture in factures_importees]), 2)

    return {
        "factures": factures_importees[-10:],  # Récupère les 10 dernières factures
        "temps_moyen": temps_moyen,
        "logs": logs_erreurs[-5:]  # Récupère les 5 derniers logs d'erreurs
    }

@app.post("/reset_monitoring")
async def reset_monitoring(user: str = Depends(login_required)):
    global factures_importees, logs_erreurs
    factures_importees = []
    logs_erreurs = []
    return JSONResponse(status_code=200, content={"message": "Historique et logs réinitialisés"})

@app.get("/dashboard")
async def dashboard(request: Request, user: str = Depends(login_required)):
    if not session["user"]:
        return templates.TemplateResponse("acces_refuse.html", {"request": request})
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})

@app.get("/dashboard_data")
async def dashboard_data():
    total_factures = len(factures_importees)
    total_erreurs = len(logs_erreurs)

    # Calculate success rate
    if total_factures > 0:
        success_rate = round((total_factures - total_erreurs) / total_factures * 100, 2)
    else:
        success_rate = 0

    # Compter les statuts
    statuts = {"OK": 0, "Échec": 0}
    for facture in factures_importees:
        if facture["status"] == "OK":
            statuts["OK"] += 1
        elif facture["status"] == "Échec":
            statuts["Échec"] += 1

    return JSONResponse(content={
        "total_factures": total_factures,
        "taux_succes": success_rate,
        "nb_erreurs": total_erreurs,
        "statuts": statuts
    })