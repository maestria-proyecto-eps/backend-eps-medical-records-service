import math

from schemas.request import PreinscripcionRequest
from schemas.response.GenericPaginatedResponse import PaginatedResponse
from schemas.response.GenericResponse import Response
from schemas.response.Preinscripcionresponse import PreinscripcionResponse, PreinscripcionItemResponse
from services.repositories.MedicamentoRepository import MedicamentoRepository
from services.repositories.PrescripcionesRepository import PrescripcionesRepository
from models.Prescripciones import Prescripciones
from models.PrescripcionesItems import PrescripcionesItems


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
            if not item.duracion or item.duracion.strip() == "":
                return Response.error("El campo 'duracion' no puede estar vacio")
            if not self.repoMedicamentos.existe_medicamento_por_codigo(item.id_medicamento):
                return Response.error(f"El medicamento con código {item.id_medicamento} no existe")
        
        # Crear la prescripción principal
        preinscripcion = Prescripciones(
            id_atencion=preinscripcionData.id_atencion,
            tipo=preinscripcionData.tipo
        )
        
        # Crear los items relacionados
        for item_data in preinscripcionData.prescripciones_items:
            item = PrescripcionesItems(
                cantidad=item_data.cantidad,
                dosis=item_data.dosis,
                duracion=item_data.duracion,
                id_medicamento=item_data.id_medicamento
            )
            preinscripcion.prescripciones_items.append(item)
        
        self.repoPreinscripciones.crear_prescripcionConGuardado(preinscripcion)
        self.repoPreinscripciones.db.commit()
        self.repoPreinscripciones.db.refresh(preinscripcion)
        
        response = self.MapModelToDTO(preinscripcion)
        
        return Response.ok(response, "Preinscripción creada exitosamente")
    
    def GetPreinscripciones(self, idPreinscripcion: int, idAtencion: int, tipo: int, pag: int, cantidad: int):
        if(idPreinscripcion != None and idPreinscripcion <= 0):
            return Response.error("Id de preinscripción debe ser un número positivo")
        if(idAtencion != None and idAtencion <= 0):
            return Response.error("Id de atención debe ser un número positivo")
        if(tipo != None and tipo not in [1, 2, 3]):
            return Response.error("El campo 'tipo' tiene un valor inválido [1,2,3]")
        preinscripciones, totalElem = self.repoPreinscripciones.obtener_preinscripcionPorFiltros(idPreinscripcion, idAtencion, tipo, pag, cantidad)
        totalPags = math.ceil(totalElem / cantidad)
        response = [self.MapModelToDTO(pre) for pre in preinscripciones]
        return Response.ok(PaginatedResponse[PreinscripcionResponse](
        data=response,
        page=pag,
        pages=totalPags),"Datos obtenidos exitosamente")

    def MapModelToDTO(self, preinscripcion: Prescripciones) -> PreinscripcionResponse:
        items_response = [
            PreinscripcionItemResponse(
                id_items=item.id_items,
                id_medicamento=item.id_medicamento,
                cantidad=item.cantidad,
                dosis=item.dosis,
                duracion=item.duracion,
                id_preinscripcion=item.id_prescripcion
            )
            for item in preinscripcion.prescripciones_items
        ]
        
        return PreinscripcionResponse(
            id_preinscripcion=preinscripcion.id_prescripcion,
            id_atencion=preinscripcion.id_atencion,
            tipo=preinscripcion.tipo,
            prescripciones_items=items_response
        )
    
    def GetPreinscripcionesByDoctor(self, num_documento_doctor: int, pag: int, cantidad: int):
        if num_documento_doctor <= 0:
            return Response.error("Documento de doctor inválido")
        
        
        preinscripciones, totalElem = self.repoPreinscripciones.obtener_por_doctor(num_documento_doctor, pag, cantidad)
        totalPags = math.ceil(totalElem / cantidad) if cantidad > 0 else 0
        response = [self.MapModelToDTO(pre) for pre in preinscripciones]

        return Response.ok(
            PaginatedResponse[PreinscripcionResponse](
                data=response,
                page=pag,
                pages=totalPags
            ),
            "Datos obtenidos exitosamente"
        )


    def GetPreinscripcionesByPaciente(self, num_documento_paciente: int, pag: int, cantidad: int):
        if num_documento_paciente <= 0:
            return Response.error("Documento de paciente inválido")
        
        preinscripciones, totalElem = self.repoPreinscripciones.obtener_por_paciente(num_documento_paciente, pag, cantidad)
        totalPags = math.ceil(totalElem / cantidad) if cantidad > 0 else 0
        response = [self.MapModelToDTO(pre) for pre in preinscripciones]

        return Response.ok(
            PaginatedResponse[PreinscripcionResponse](
                data=response,
                page=pag,
                pages=totalPags
            ),
            "Datos obtenidos exitosamente"
        )