from typing import List

from fastapi import APIRouter, Depends, status

from dependencies import getPreinscripcionService
from schemas.request.PreinscripcionRequest import PreinscripcionRequest
from schemas.response.GenericPaginatedResponse import PaginatedResponse
from schemas.response.GenericResponse import Response
from schemas.response.Preinscripcionresponse import PreinscripcionResponse
from services.PreinscripcionesService import PreinscripcionesService


router = APIRouter(
    prefix="/prescriptions",
    tags=["prescriptions"]
)

@router.post("/", response_model=Response[List[PreinscripcionResponse]])
def addPreinscripcion(preinscripcionData: PreinscripcionRequest, service: PreinscripcionesService = Depends(getPreinscripcionService)):
    result = service.AddPreinscripcion(preinscripcionData)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse()

@router.get("/", response_model=Response[PaginatedResponse[PreinscripcionResponse]])
def getPreinscripciones(idPreinscripcion: int = None, idAtencion: int = None, tipo: int = None, pag: int = 1, cantidad: int = 10,
                        service: PreinscripcionesService = Depends(getPreinscripcionService)):
    result = service.GetPreinscripciones(idPreinscripcion, idAtencion, tipo, pag, cantidad)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse()