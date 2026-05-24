from fastapi import APIRouter
from fastapi import Depends
from starlette import status

from dependencies import getCitaService
from schemas.request.RegistroHistoriaRequest import RegistroHistoriaRequest
from schemas.request.RemisionRequest import RemisionRequest
from schemas.response.AppointmentResponse import AppointmentResponse
from schemas.response.RemisionResponse import RemisionResponse
from schemas.response.GenericResponse import Response
from services.CitaService import CitatService
from core.dependencias import RequireRole

router = APIRouter(
    prefix="/appoinment",
    tags=["Appoinment"],
    
)

@router.get("/{id}/consultation-context", response_model=Response[AppointmentResponse], dependencies=[Depends(RequireRole(["Médico"]))])
def get_appoinment(id: int, service: CitatService = Depends(getCitaService)):
    model = service.getRegistroCitaById(id)
    if(model.hasError and model.message =="La cita no existe"):
         return model.toHttpResponse(status.HTTP_404_NOT_FOUND)
    if(model.hasError and model.message =="La cita ya tiene un registro asociado"):
         return model.toHttpResponse(status.HTTP_409_CONFLICT)
    return model.toHttpResponse()

@router.post("/{id}/consultation", response_model=Response[AppointmentResponse], dependencies=[Depends(RequireRole(["Médico"]))])
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

@router.post("/{id}/remision", response_model=Response[RemisionResponse], dependencies=[Depends(RequireRole(["Médico"]))])
def create_remision(id: int, remision: RemisionRequest, service: CitatService = Depends(getCitaService)):
    model = service.crear_remision(id, remision)
    if model.hasError:
        if model.message == "La cita no existe":
            return model.toHttpResponse(status.HTTP_404_NOT_FOUND)
        if model.message == "La especialidad no existe":
            return model.toHttpResponse(status.HTTP_422_UNPROCESSABLE_ENTITY)
        if model.message == "La fecha de expiración debe ser una fecha futura":
            return model.toHttpResponse(status.HTTP_422_UNPROCESSABLE_ENTITY)
        if model.message == "El id_registro no pertenece a la cita":
            return model.toHttpResponse(status.HTTP_403_FORBIDDEN)
        return model.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return model.toHttpResponse(status.HTTP_201_CREATED)
