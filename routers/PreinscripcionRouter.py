from typing import List

from fastapi import APIRouter, Depends, status

from dependencies import (
    getPreinscripcionService,
    get_current_doctor_user,
    get_current_patient_user
)
from schemas.request.PreinscripcionRequest import PreinscripcionRequest
from schemas.response.GenericPaginatedResponse import PaginatedResponse
from schemas.response.GenericResponse import Response
from schemas.response.Preinscripcionresponse import PreinscripcionResponse
from services.PreinscripcionesService import PreinscripcionesService
from core.dependencias import RequireRole

router = APIRouter(
    prefix="/prescriptions",
    tags=["prescriptions"]
)

@router.post("/", response_model=Response[List[PreinscripcionResponse]], dependencies=[Depends(RequireRole(["Médico"]))])
def addPreinscripcion(preinscripcionData: PreinscripcionRequest, service: PreinscripcionesService = Depends(getPreinscripcionService)):
    result = service.AddPreinscripcion(preinscripcionData)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse()

@router.get("/", response_model=Response[PaginatedResponse[PreinscripcionResponse]], dependencies=[Depends(RequireRole(["Médico", "Paciente"]))])
def getPreinscripciones(idPreinscripcion: int = None, idAtencion: int = None, tipo: int = None, pag: int = 1, cantidad: int = 10,
                        service: PreinscripcionesService = Depends(getPreinscripcionService)):
    result = service.GetPreinscripciones(idPreinscripcion, idAtencion, tipo, pag, cantidad)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse()

@router.get("/doctors/me", response_model=Response[PaginatedResponse[PreinscripcionResponse]], dependencies=[Depends(RequireRole(["Médico"]))])
def getMisPreinscripcionesDoctor(
    pag: int = 1,
    cantidad: int = 10,
    service: PreinscripcionesService = Depends(getPreinscripcionService),
    current_user = Depends(get_current_doctor_user),
):
    result = service.GetPreinscripcionesByDoctor(current_user["num_documento"], pag, cantidad)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse()


@router.get("/patients/me", response_model=Response[PaginatedResponse[PreinscripcionResponse]], dependencies=[Depends(RequireRole(["Paciente"]))])
def getMisPreinscripcionesPaciente(
    pag: int = 1,
    cantidad: int = 10,
    service: PreinscripcionesService = Depends(getPreinscripcionService),
    current_user = Depends(get_current_patient_user),
):
    result = service.GetPreinscripcionesByPaciente(current_user["num_documento"], pag, cantidad)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse()