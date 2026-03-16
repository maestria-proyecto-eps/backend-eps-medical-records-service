from schemas.response.AppointmentResponse import AppointmentResponse
from schemas.response.GenericResponse import Response
from services.repositories.CitaRepository import CitaRepository
from services.repositories.RegistroRepository import RegistroRepository


class CitatService:
    def __init__(self, repo: CitaRepository, repoRegistro: RegistroRepository):
        self.repo = repo
        self.repoRegistro = repoRegistro

    def getRegistroCitaById(self, id_cita):
        if(self.repoRegistro.exists_by_id_cita(id_cita)):
            return Response.Error("La cita ya tiene un registro asociado")
        cita = self.repo.get(id_cita)
        if(cita is None):
            return Response.Error("La cita no existe")
        return Response.ok(AppointmentResponse.model_validate(cita),"Cita obtenida exitosamente")