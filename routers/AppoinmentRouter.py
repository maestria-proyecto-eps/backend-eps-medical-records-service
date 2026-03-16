from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status

from dependencies import getCitaService
from schemas.response.AppointmentResponse import AppointmentResponse
from schemas.response.GenericResponse import Response
from services.CitaService import CitatService


router = APIRouter(
    prefix="/appoinment",
    tags=["Appoinment"]
)

@router.get("/{id}/consultation-context", response_model=Response[AppointmentResponse])
def get_appoinment(id: int, service: CitatService = Depends(getCitaService)):
    model = service.getRegistroCitaById(id)
    if(model.hasError and model.message =="La cita no existe"):
         return model.toHttpResponse(status.HTTP_404_NOT_FOUND)
    if(model.hasError and model.message =="La cita ya tiene un registro asociado"):
         return model.toHttpResponse(status.HTTP_409_CONFLICT)
    return model.toHttpResponse()
