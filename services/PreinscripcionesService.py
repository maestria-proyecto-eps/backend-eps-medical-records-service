from schemas.request import PreinscripcionRequest
from schemas.response.GenericResponse import Response
from schemas.response.Preinscripcionresponse import PreinscripcionResponse
from services.repositories.MedicamentoRepository import MedicamentoRepository
from services.repositories.PrescripcionesRepository import PrescripcionesRepository
from models.Prescripciones import Prescripciones


class PreinscripcionesService:
    def __init__(self, repoPreinscripciones: PrescripcionesRepository,
                 repoMedicamentos: MedicamentoRepository):
        self.repoPreinscripciones = repoPreinscripciones
        self.repoMedicamentos = repoMedicamentos

    def AddPreinscripcion(self, preinscripcionData: PreinscripcionRequest):

        #Validaciones importantes
        if preinscripcionData.tipo not in [1, 2, 3]:  # Ejemplo de valores válidos
            return Response.error("El campo 'tipo' tiene un valor inválido [1,2,3]")
        if preinscripcionData.id_atencion <= 0:
            return Response.error("El campo 'id_atencion' debe ser un número positivo")
        for item in preinscripcionData.prescripciones_items:
            if item.cantidad <= 0:
                return Response.error("El campo 'cantidad' en items debe ser un número positivo")
            if not item.dosis or item.dosis.strip() == "" or len(item.dosis) > 50:
                return Response.error("El campo 'dosis' en items no puede estar vacío y debe tener hasta 50 caracteres")
            if item.duracion <= 0:
                return Response.error("El campo 'duracion' en items debe ser un número positivo")
            if not self.repoMedicamentos.existe_medicamento_por_codigo(item.id_medicamento):
                return Response.error(f"El medicamento con código {item.id_medicamento} no existe")
        
        preinscripcion= Prescripciones(**preinscripcionData.model_dump())
        self.repoPreinscripciones.crear_prescripcionConGuardado(preinscripcion)
        self.repoPreinscripciones.db.commit()
        self.repoPreinscripciones.db.refresh(preinscripcion)
        return Response.ok(PreinscripcionResponse.model_validate(preinscripcion), "Preinscripción creada exitosamente")