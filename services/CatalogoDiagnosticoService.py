from schemas.response.DiagnostcoResponse import DiagnosticoResponse
from schemas.response.AppointmentResponse import AppointmentResponse
from schemas.response.GenericResponse import Response
from services.repositories.CatalogoDiagnosticoRepository import CatalogoDiagnosticoRepository


class CatalogoDiagnosticoService:
    def __init__(self, repo: CatalogoDiagnosticoRepository):
        self.repo = repo

    def getDiagnostico(self, id_diagnostico: int=None, nombre: str=None):
        if(nombre is not None and len(nombre)<2):
            return Response.error("El nombre debe tener al menos 2 caracteres")
        diagnostico = self.repo.get_catalogo_by_filters(id_diagnostico, nombre)
        data = [DiagnosticoResponse.model_validate(d) for d in diagnostico]
        return Response.ok(data, "Diagnóstico obtenido exitosamente")