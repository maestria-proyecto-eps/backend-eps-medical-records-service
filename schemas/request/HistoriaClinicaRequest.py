from pydantic import BaseModel


class CrearHistoriaClinicaRequest(BaseModel):
    id_paciente: int

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
