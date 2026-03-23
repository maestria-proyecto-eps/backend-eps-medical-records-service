from datetime import datetime
import uuid

from models.HistoriaClinica import HistoriaClinica
from schemas.response.HistoriaClinicaResponse import HistoriaClinicaResponse
from schemas.response.GenericResponse import Response
from services.repositories import HistoriaRepository


class HistoriaService:
    def __init__(self, repo: HistoriaRepository):
        self.repo = repo

    def getHistoriaByUserId(self, id_usuario):
        historias = self.repo.get_by_patient_id(id_usuario)
        if not historias:
            return Response.error("No hay historia clínica para el paciente")

        historias_dto = [HistoriaClinicaResponse.model_validate(historia) for historia in historias]
        return Response.ok(historias_dto, "Historias clínicas obtenidas exitosamente")