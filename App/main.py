from fastapi import FastAPI, Request, Form, Depends, HTTPException, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

import os
import sys
from pathlib import Path
from pprint import pprint

from App.services.outils import charger_image, pil_to_cv2
from App.services.qr_code import extraction_qrcode
from App.services.segmentation import segmenter_image
from App.services.ocr import extraction_texte
from App.services.parseur import extraction_texte_qrcode, extraction_texte_facture, extraction_texte_table

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "webapp/templates"))

FACTURES_DIR = Path(r"C:\Users\steve\Documents\Formation IA\ProjetOCR\ProjetOCR\factures")

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "webapp/static")), name="static")

# Simulation d'une session utilisateur (à remplacer par un vrai système d'authentification)
fake_users_db = {"admin": "password"}
session = {"user": None}

def login_required(request: Request):
    if not session["user"]:
        raise HTTPException(status_code=403, detail="Vous devez être connecté pour accéder à cette page.")
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
    return templates.TemplateResponse("factures.html", {"request": request, "user": user})

@app.get("/ajout_facture")
async def add_facture(request: Request, user: str = Depends(login_required)):
    return templates.TemplateResponse("ajout_facture.html", {"request": request, "user": user})

@app.get("/monitoring")
async def monitoring(request: Request, user: str = Depends(login_required)):
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
    # Vérifier le type de fichier
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return JSONResponse(status_code=400, content={"error": "Format de fichier non supporté"})
    
    # Créer un dossier pour la facture
    upload_dir = Path("factures_upload")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Chemin complet du fichier
    file_path = upload_dir / file.filename
    view_path = f"/view_facture/{extract_year(file.filename)}/{file.filename}"
    # Sauvegarder le fichier
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    try:
        # Charger et traiter l'image
        image = charger_image(nom_du_fichier=str(file_path))
        segments, rectangles = segmenter_image(image)

        zone1, zone2, zone3 = segments

        # Extraction OCR et QR
        data_z1 = extraction_texte(zone1)
        data_z2 = extraction_texte(zone2)
        data_qr = extraction_qrcode(image=pil_to_cv2(zone3))

        texte_qr = extraction_texte_qrcode(data_qr)
        texte1 = extraction_texte_facture(data_z1)
        texte2 = extraction_texte_table(data_z2)

        return templates.TemplateResponse("ajout_facture.html", {
            "request": request, 
            "user": user, 
            "file_path": str(view_path),
            "texte_qr": texte_qr,
            "texte1": texte1,
            "texte2": texte2
        })
    
    except Exception as e:
        return templates.TemplateResponse("ajout_facture.html", {
            "request": request, 
            "user": user, 
            "error": f"Erreur de traitement : {str(e)}"
        })