from pydantic import BaseModel


class MedicamentoResponse(BaseModel):
    codigo: int
    nombre_medicamento: str
    reg_invima: int
    principio_activo: str
    presentacion: str

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
