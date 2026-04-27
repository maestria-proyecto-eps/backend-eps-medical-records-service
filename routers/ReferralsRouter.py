from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status

from dependencies import getCitaService
from schemas.response.GenericResponse import Response
from schemas.response.RemisionResponse import RemisionResponse
from services.CitaService import CitatService


router = APIRouter(
    prefix="/referrals",
    tags=["Referrals"]
)


@router.get("/", response_model=Response[list[RemisionResponse]])
def get_referrals(
    id_especialidad: int = None,
    id_paciente: int = None,
    vigente: bool = None,
    service: CitatService = Depends(getCitaService)
):
    model = service.get_referrals(
        id_especialidad=id_especialidad,
        id_paciente=id_paciente,
        vigente=vigente
    )
    return model.toHttpResponse(status.HTTP_200_OK)


@router.get("/patients/{patient_id}", response_model=Response[list[RemisionResponse]])
def get_referrals_by_patient_id(
    patient_id: int,
    service: CitatService = Depends(getCitaService)
):
    model = service.get_referrals_by_patient_id(patient_id)
    return model.toHttpResponse(status.HTTP_200_OK)