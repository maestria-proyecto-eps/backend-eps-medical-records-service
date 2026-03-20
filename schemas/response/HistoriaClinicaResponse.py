from datetime import date
from typing import List

from pydantic import BaseModel


class RegistroHistoriaResponse(BaseModel):
    id_registro: int
    observaciones: str
    tratamiento: str
    id_cita: int
    id_diagnostico: int
    nombre_enfermedad: str

    model_config={
        "from_attributes": True,
        "populate_by_name": True
    }


class HistoriaClinicaResponse(BaseModel):
    id_historia: int
    id_paciente: int
    fecha_inicio: date
    fecha_ult_actualizacion: date
    registros_historia: List[RegistroHistoriaResponse] = []
    
    model_config={
        "from_attributes": True,
        "populate_by_name": True
    }