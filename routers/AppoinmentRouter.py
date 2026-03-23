from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status

from dependencies import getCitaService
from schemas.request.RegistroHistoriaRequest import RegistroHistoriaRequest
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

@router.post("/{id}/consultation", response_model=Response[AppointmentResponse])
def create_consultation(id: int, registro: RegistroHistoriaRequest, service: CitatService = Depends(getCitaService)):
    model = service.crear_registro_historia(registro, id)
    if(model.hasError ):
         if model.message =="La cita no existe":
              return model.toHttpResponse(status.HTTP_404_NOT_FOUND)
         if model.message =="La cita ya tiene un registro asociado":
              return model.toHttpResponse(status.HTTP_409_CONFLICT)
         if model.message.startswith("Error al crear registro"):
               return model.toHttpResponse(status.HTTP_500_INTERNAL_SERVER_ERROR)
         else:
              return model.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return model.toHttpResponse(status.HTTP_201_CREATED)
