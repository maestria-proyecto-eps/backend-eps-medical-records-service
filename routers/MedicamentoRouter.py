from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from dependencies import getMedicamentoService
from schemas.response.MedicamentoResponse import MedicamentoResponse
from schemas.response.GenericResponse import Response
from services import MedicamentoService


router = APIRouter(
    prefix="/medicamentos",
    tags=["medicamentos"]
)


@router.get("/search", response_model=Response[List[MedicamentoResponse]])
def get_medicamentos( nombre: str=None, service: MedicamentoService = Depends(getMedicamentoService)):
    model = service.getMedicamento(nombre)
    if model.hasError:
        return model.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return model.toHttpResponse()
