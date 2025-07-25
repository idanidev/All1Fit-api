from fastapi import APIRouter, HTTPException
from database import db
from bson.objectid import ObjectId
from models import EntrenamientoBase, EntrenamientoDB

router = APIRouter()

@router.get("/entrenamientos", response_model=list[EntrenamientoDB])
async def listar_entrenamientos():
    entrenamientos = []
    cursor = db.entrenamientos.find()
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        entrenamientos.append(doc)
    return entrenamientos

@router.post("/entrenamientos", response_model=EntrenamientoDB)
async def crear_entrenamiento(data: EntrenamientoBase):
    try:
        doc = data.to_mongo()  # 👈 transformación aquí
        result = await db.entrenamientos.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return doc
    except Exception as e:
        print("💥 ERROR AL GUARDAR:", e)
        raise HTTPException(status_code=500, detail="Error interno")
