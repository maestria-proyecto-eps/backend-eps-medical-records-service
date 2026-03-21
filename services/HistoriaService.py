from datetime import datetime
import uuid

from models.HistoriaClinica import HistoriaClinica
from schemas.request import HistoriaClinicaRequest
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

    def crear_historia(self, historia_data: HistoriaClinicaRequest):
        # Validar si ya existe una historia clínica para este paciente
        if self.repo.existe_historia_por_paciente(historia_data.id_paciente):
            return Response.error("Ya existe una historia clínica para este paciente")
        historia = HistoriaClinica(**historia_data.dict())
        historia.id_historia = uuid.uuid4()  # Generar un UUID para el id_historia
        historia.fecha_inicio = datetime.now().date()
        historia.fecha_ult_actualizacion = datetime.now().date()
        nueva_historia = self.repo.crear_historia(historia)
        historia_dto = HistoriaClinicaResponse.model_validate(nueva_historia)
        return Response.ok(historia_dto, "Historia clínica creada exitosamente")