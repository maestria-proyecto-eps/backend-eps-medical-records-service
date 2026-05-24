from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from dependencies import getMedicamentoService
from schemas.response.MedicamentoResponse import MedicamentoResponse
from schemas.response.GenericResponse import Response
from services import MedicamentoService
from core.dependencias import get_usuario_actual

router = APIRouter(
    prefix="/medicamentos",
    tags=["medicamentos"],
    dependencies=[Depends(get_usuario_actual)]
)


@router.get("/search", response_model=Response[List[MedicamentoResponse]])
def get_medicamentos( nombre: str=None, service: MedicamentoService = Depends(getMedicamentoService)):
    model = service.getMedicamento(nombre)
    if model.hasError:
        return model.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return model.toHttpResponse()
