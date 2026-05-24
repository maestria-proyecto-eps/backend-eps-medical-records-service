from pydantic import BaseModel
from datetime import date


class RemisionResponse(BaseModel):
    id_remision: int
    expiracion: date
    id_paciente: int
    id_registro: int
    id_especialidad: int

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
