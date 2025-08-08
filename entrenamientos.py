from fastapi import APIRouter, HTTPException
from database import db
from models import EntrenamientoBase, EntrenamientoDB
from bson.objectid import ObjectId

router = APIRouter(
    prefix="/entrenamientos",
    tags=["Entrenamientos"]
)


@router.get("/", response_model=list[EntrenamientoDB])
async def listar_entrenamientos():
    entrenamientos = []
    cursor = db.entrenamientos.find()
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # Mongo ObjectId a string
        entrenamientos.append(doc)
    return entrenamientos


@router.post("/", response_model=EntrenamientoDB)
async def crear_entrenamiento(data: EntrenamientoBase):
    try:
        doc = data.model_dump()  # ✅ Usar model_dump() en Pydantic v2
        result = await db.entrenamientos.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return doc
    except Exception as e:
        print("💥 ERROR AL GUARDAR:", e)
        raise HTTPException(status_code=500, detail="Error interno")


@router.delete("/{id}")
async def eliminar_entrenamiento(id: str):
    result = await db.entrenamientos.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Entrenamiento no encontrado")
    return {"mensaje": "Entrenamiento eliminado"}
