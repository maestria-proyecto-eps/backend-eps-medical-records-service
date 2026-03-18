from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from dependencies import getHistoriaService
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