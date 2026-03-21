from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from dependencies import getHistoriaService
from schemas.request.HistoriaClinicaRequest import CrearHistoriaClinicaRequest
from schemas.response.HistoriaClinicaResponse import HistoriaClinicaResponse
from schemas.response.GenericResponse import Response
from services import HistoriaService


router = APIRouter(
    prefix="/pattient",
    tags=["patient"]
)

@router.get("/{id}/medical-history", response_model=Response[List[HistoriaClinicaResponse]])
def get_appoinment(id: int, service: HistoriaService = Depends(getHistoriaService)):
    model = service.getHistoriaByUserId(id)
    if(model.hasError==True and model.message =="No hay historia clínica para el paciente"):
         return model.toHttpResponse(status.HTTP_404_NOT_FOUND)
    return model.toHttpResponse()

@router.post("{id}/medical-history", response_model=Response[HistoriaClinicaResponse])
def crear_historia_clinica(id: int, service: HistoriaService = Depends(getHistoriaService)):
    """Crea una nueva historia clínica con id autoincremental"""
    historiaRq = CrearHistoriaClinicaRequest(id_paciente=id)
    model = service.crear_historia(historiaRq)
    if model.hasError:
        return model.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return model.toHttpResponse(status.HTTP_201_CREATED)