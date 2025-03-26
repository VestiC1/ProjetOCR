from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from fastapi import Depends
from fastapi import HTTPException

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "webapp/templates"))

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
