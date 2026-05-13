from pydantic import BaseModel
from typing import List

class AdministracionMedCreate(BaseModel):
    id_enfermera: int
    id_hospitalizacion: int
    admin_med_items: List[int]

