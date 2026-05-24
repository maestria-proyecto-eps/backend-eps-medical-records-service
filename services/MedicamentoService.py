from schemas.response.MedicamentoResponse import MedicamentoResponse
from schemas.response.GenericResponse import Response
from services.repositories.MedicamentoRepository import MedicamentoRepository


class MedicamentoService:
    def __init__(self, repo: MedicamentoRepository):
        self.repo = repo

    def getMedicamento(self, nombre: str = None):
        if nombre is not None and len(nombre) < 2:
            return Response.error("El nombre debe tener al menos 2 caracteres")

        medicamentos = self.repo.get_medicamento_by_filters( nombre)
        data = [MedicamentoResponse.model_validate(m) for m in medicamentos]
        return Response.ok(data, "Medicamentos obtenidos exitosamente")
