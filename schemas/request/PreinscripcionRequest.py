from typing import List

from pydantic import BaseModel

from schemas.request.RegistroHistoriaRequest import MedicamentoRegistro


class PreinscripcionItemRequest(BaseModel):
    id_medicamento: int
    cantidad: int
    dosis: str
    duracion: str
    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }


class PreinscripcionRequest(BaseModel):
    id_atencion: int
    tipo: int
    prescripciones_items: List[PreinscripcionItemRequest]

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }