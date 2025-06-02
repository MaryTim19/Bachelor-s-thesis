from fastapi import FastAPI, Request, UploadFile, File, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ultralytics import YOLO
from PIL import Image
import io
import os
import shutil
import uuid

from database import SessionLocal, engine
from models import Base, Dress

# Ініціалізація таблиць у БД
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Папка зі статичними файлами
app.mount("/static", StaticFiles(directory="static"), name="static")

# Шаблони Jinja2
templates = Jinja2Templates(directory="templates")

# Модель YOLO
model = YOLO("models/best.pt")

# Класи
CLASS_NAMES = {
    0: "A-line",
    1: "Ballgown",
    2: "Mermaid",
    3: "Mini",
    4: "Sheath"
}

# Папка для зображень
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Сесія БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Головна сторінка
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "image_url": None
    })

# POST /predict — розпізнавання
@app.post("/predict")
async def predict(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        allowed_types = ["image/jpeg", "image/png", "image/webp"]
        if file.content_type not in allowed_types:
            return templates.TemplateResponse("index.html", {
                "request": request,
                "error": "🚫 Підтримуються лише формати JPG, PNG або WEBP.",
                "image_url": None
            })

        # Збереження зображення
        filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Завантаження зображення
        image = Image.open(file_path).convert("RGB")
        result = model(image)[0]
        probs = result.probs

        if probs:
            top_idx = int(probs.top1)
            confidence = float(probs.top1conf)

            if confidence < 0.5:
                return templates.TemplateResponse("index.html", {
                    "request": request,
                    "error": "🚫 На зображенні не розпізнано весільну сукню. Завантажте інше зображення.",
                    "image_url": f"/static/uploads/{filename}"
                })

            label = CLASS_NAMES.get(top_idx, "Unknown")
            suggested_dresses = db.query(Dress).filter(Dress.style == label).limit(3).all()

            return templates.TemplateResponse("index.html", {
                "request": request,
                "result": {
                    "label": label,
                    "confidence": round(confidence * 100, 2)
                },
                "image_url": f"/static/uploads/{filename}",
                "suggested": suggested_dresses
            })

        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "🤖 Модель не повернула ймовірностей.",
            "image_url": f"/static/uploads/{filename}"
        })

    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"🚫 Помилка: {str(e)}",
            "image_url": None
        })

# Каталог
@app.get("/catalog")
async def show_catalog(request: Request, db: Session = Depends(get_db)):
    dresses = db.query(Dress).all()
    return templates.TemplateResponse("catalog.html", {
        "request": request,
        "dresses": dresses
    })
