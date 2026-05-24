from typing import List
from pydantic import BaseModel


class MedicamentoRegistro(BaseModel):
    codigo: int
    dosis: str
    duracion: int
    cantidad: int

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }


class RegistroHistoriaRequest(BaseModel):
    obervacion: str
    tratamiento: str
    id_diagnostico: int
    tipo_preinscripcion: int
    medicamentos: List[MedicamentoRegistro]

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
