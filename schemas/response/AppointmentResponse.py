from pydantic import BaseModel


class AppointmentResponse(BaseModel):
    id_cita: int
    id_paciente: int
    id_especialidad: int

    model_config={
        "from_attributes": True,
        "populate_by_name": True
    }