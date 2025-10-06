from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from typing import Optional
from datetime import date, datetime


class EntrenamientoBase(BaseModel):
    nombre: str
    descripcion: str
    duracionEstimada: Optional[str] = None
    fechaInicio: Optional[date] = None
    observaciones: Optional[str] = None

    def to_mongo(self):
        doc = self.model_dump()
        if self.fechaInicio:
            doc["fechaInicio"] = datetime.combine(self.fechaInicio, datetime.min.time())
        return doc


class EntrenamientoDB(EntrenamientoBase):
    id: str = Field(alias="_id")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
