from pydantic import BaseModel
from datetime import date


class RemisionRequest(BaseModel):
    id_registro: int
    id_especialidad: int
    fecha_expiracion: date

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }