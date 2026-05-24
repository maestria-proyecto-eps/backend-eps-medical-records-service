from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from dependencies import getDiagnosticoService
from schemas.response.DiagnostcoResponse import DiagnosticoResponse
from schemas.response.GenericResponse import Response
from services import CatalogoDiagnosticoService
from core.dependencias import get_usuario_actual

router = APIRouter(
    prefix="/diagnosticos",
    tags=["diagnosticos"],
    dependencies=[Depends(get_usuario_actual)]
)

@router.get("/search", response_model=Response[List[DiagnosticoResponse]])
def get_diagnosticos(id: int=None, nombre: str=None, service: CatalogoDiagnosticoService = Depends(getDiagnosticoService)):
    model = service.getDiagnostico(id,nombre)
    if(model.hasError==True):
         return model.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return model.toHttpResponse()