from pydantic import BaseModel


class DiagnosticoResponse(BaseModel):
    id_diagnostico: int
    nombre_enfermedad: str
    model_config={
        "from_attributes": True,
        "populate_by_name": True
    }