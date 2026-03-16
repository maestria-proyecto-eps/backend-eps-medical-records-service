from pydantic import BaseModel


class AppointmentResponse(BaseModel):
    id_cita: int
    id_paciente: int
    id_especialidad: int