from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError

from database import db
from models import EntrenamientoBase, EntrenamientoDB

router = APIRouter(
    prefix="/entrenamientos",
    tags=["Entrenamientos"]
)


@router.get("")
@router.get("/", response_model=List[EntrenamientoDB])
async def listar_entrenamientos() -> List[EntrenamientoDB]:
    try:
        documentos = (
            await db.entrenamientos
            .find()
            .sort("fechaInicio", 1)
            .to_list(length=None)
        )
    except PyMongoError as exc:
        print("ERROR AL LEER ENTRENAMIENTOS:", exc)
        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar con la base de datos"
        ) from exc
    except Exception as exc:  # Fallback para cualquier otro error inesperado
        print("ERROR INESPERADO AL LISTAR ENTRENAMIENTOS:", exc)
        raise HTTPException(
            status_code=500,
            detail="Error interno al obtener los entrenamientos"
        ) from exc

    entrenamientos: List[EntrenamientoDB] = []
    for doc in documentos:
        doc["_id"] = str(doc["_id"])  # Mongo ObjectId a string
        if "fechaInicio" in doc and isinstance(doc["fechaInicio"], datetime):
            doc["fechaInicio"] = doc["fechaInicio"].date()
        entrenamientos.append(EntrenamientoDB.model_validate(doc))

    return entrenamientos


@router.post("/", response_model=EntrenamientoDB)
async def crear_entrenamiento(data: EntrenamientoBase):
    try:
        doc = data.to_mongo()
        result = await db.entrenamientos.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return EntrenamientoDB.model_validate(doc)
    except Exception as e:
        print("ERROR AL GUARDAR:", e)
        raise HTTPException(status_code=500, detail="Error interno")


@router.delete("/{id}")
async def eliminar_entrenamiento(id: str):
    result = await db.entrenamientos.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Entrenamiento no encontrado")
    return {"mensaje": "Entrenamiento eliminado"}
