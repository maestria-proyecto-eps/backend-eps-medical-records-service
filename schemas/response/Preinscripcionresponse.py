from typing import List

from pydantic import BaseModel


class PreinscripcionItemResponse(BaseModel):
    id_items: int
    id_medicamento: int
    cantidad: int
    dosis: str
    duracion: int
    id_preinscripcion: int
    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }

class PreinscripcionResponse(BaseModel):
    id_preinscripcion: int
    id_atencion: int
    tipo: int
    prescripciones_items: List[PreinscripcionItemResponse]

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }