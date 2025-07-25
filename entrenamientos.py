from fastapi import APIRouter, HTTPException
from database import db
from models import EntrenamientoBase, EntrenamientoDB


async def listar_entrenamientos():
    entrenamientos = []
    cursor = db.entrenamientos.find()
    async for doc in cursor:
        entrenamientos.append(doc)
    return entrenamientos

async def crear_entrenamiento(data: EntrenamientoBase):
    try:
        result = await db.entrenamientos.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return doc
    except Exception as e:
        print("💥 ERROR AL GUARDAR:", e)
        raise HTTPException(status_code=500, detail="Error interno")
