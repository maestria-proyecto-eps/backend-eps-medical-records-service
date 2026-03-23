from datetime import datetime
import uuid
from schemas.request.RegistroHistoriaRequest import RegistroHistoriaRequest
from schemas.response.AppointmentResponse import AppointmentResponse
from schemas.response.GenericResponse import Response
from schemas.response.HistoriaClinicaResponse import RegistroHistoriaResponse
from services.repositories.CitaRepository import CitaRepository
from services.repositories.RegistroRepository import RegistroRepository
from services.repositories.CatalogoDiagnosticoRepository import CatalogoDiagnosticoRepository
from services.repositories.MedicamentoRepository import MedicamentoRepository
from services.repositories.PrescripcionesRepository import PrescripcionesRepository
from services.repositories.PrescripcionesItemsRepository import PrescripcionesItemsRepository
from services.repositories.HistoriaRepository import HistoriaRepository
from models.HistoriaClinica import HistoriaClinica
from sqlalchemy.orm import Session


class CitatService:
    def __init__(self, repo: CitaRepository, repoRegistro: RegistroRepository, 
                 repoCatalogoDiagnostico: CatalogoDiagnosticoRepository,
                 repoMedicamento: MedicamentoRepository ,
                 repoPrescripciones: PrescripcionesRepository ,
                 repoPrescripcionesItems: PrescripcionesItemsRepository,
                 repoHistoria: HistoriaRepository ):
        self.repo = repo
        self.repoRegistro = repoRegistro
        self.repoCatalogoDiagnostico = repoCatalogoDiagnostico
        self.repoMedicamento = repoMedicamento
        self.repoPrescripciones = repoPrescripciones
        self.repoPrescripcionesItems = repoPrescripcionesItems
        self.repoHistoria = repoHistoria

    def getRegistroCitaById(self, id_cita):
        if(self.repoRegistro.exists_by_id_cita(id_cita)):
            return Response.error("La cita ya tiene un registro asociado")

        cita = self.repo.get_cita_by_id(id_cita)
        if cita is None:
            return Response.error("La cita no existe")
        return Response.ok(AppointmentResponse.model_validate(cita),"Cita obtenida exitosamente")

    def crear_registro_historia(self, registro_data: RegistroHistoriaRequest, id_cita: int):
        """Crea un registro de historia clínica con validaciones y transacción"""
        
        # 1. Validar que la cita exista
        cita = self.repo.get_cita_by_id(id_cita)
        if cita is None:
            return Response.error("La cita no existe")
        
        # 2. Validar que ya no tenga un registro asociado
        if self.repoRegistro.exists_by_id_cita(id_cita):
            return Response.error("La cita ya tiene un registro asociado")

        # 3. Obtener o crear historia clínica del paciente
        id_paciente = cita.id_paciente
        historias = self.repoHistoria.get_by_patient_id(id_paciente)
        if historias:
            historia = historias[0]
            crear_historia = False
        else:
            historia = HistoriaClinica(
                id_historia=uuid.uuid4(),
                id_paciente=id_paciente,
                fecha_inicio=datetime.now().date(),
                fecha_ult_actualizacion=datetime.now().date()
            )
            crear_historia = True
        
        # 4. Validar campos string (máximo 50 caracteres)
        if len(registro_data.obervacion) > 50:
            return Response.error("El campo 'obervacion' no puede exceder 50 caracteres")
        
        if len(registro_data.tratamiento) > 50:
            return Response.error("El campo 'tratamiento' no puede exceder 50 caracteres")
        
        # 5. Validar que id_diagnostico exista
        if not self.repoCatalogoDiagnostico.existe_diagnostico_por_id(registro_data.id_diagnostico):
            return Response.error(f"El diagnóstico con id {registro_data.id_diagnostico} no existe")
        # 5.1 Validar que tipopreinscripcion tenga valores validos
        if registro_data.tipo_preinscripcion not in [1, 2, 3]:  # Ejemplo de valores válidos
            return Response.error("El campo 'tipo_preinscripcion' tiene un valor inválido [1,2,3]")

        # 6. Validar medicamentos
        for med in registro_data.medicamentos:
            # Validar que el código exista
            if not self.repoMedicamento.existe_medicamento_por_codigo(med.codigo):
                return Response.error(f"El medicamento con código {med.codigo} no existe")
            
            # Validar dosis entre 0 y 50
            if len(med.dosis) > 50:
                return Response.error(f"La dosis del medicamento {med.codigo} debe ser de max 50 caracteres")
            
            # Validar duración > 0
            if med.duracion <= 0:
                return Response.error(f"La duración del medicamento {med.codigo} debe ser mayor a 0")
            
            # Validar cantidad > 0
            if med.cantidad <= 0:
                return Response.error(f"La cantidad del medicamento {med.codigo} debe ser mayor a 0")

        # 7. Ejecutar transacción
        try:
            db_session = self.repoRegistro.db
            
            if crear_historia:
                self.repoHistoria.crear_historia(historia)

            self.repoHistoria.actualizar_fecha_historia(historia.id_historia)

            prescripcion_id = None
            if registro_data.medicamentos:
                prescripcion_dict = {
                    "id_atencion": id_cita,
                    "tipo": registro_data.tipo_preinscripcion
                }
                nueva_prescripcion = self.repoPrescripciones.crear_prescripcion(prescripcion_dict)
                db_session.flush() 
                prescripcion_id = nueva_prescripcion.id_prescripcion

                for med in registro_data.medicamentos:
                    item_dict = {
                        "cantidad": med.cantidad,
                        "dosis": med.dosis,
                        "duracion": med.duracion,
                        "id_prescripcion": prescripcion_id,
                        "id_medicamento": med.codigo
                    }
                    self.repoPrescripcionesItems.crear_prescripcion_item(item_dict)

            registro_dict = {
                "observaciones": registro_data.obervacion,
                "tratamiento": registro_data.tratamiento,
                "id_historia": historia.id_historia,
                "id_cita": id_cita,
                "id_diagnostico": registro_data.id_diagnostico
            }
            nuevo_registro = self.repoRegistro.crear_registro(registro_dict)
            db_session.commit()

            return Response.ok(RegistroHistoriaResponse.model_validate(nuevo_registro), "Registro de historia creado exitosamente")

        except Exception as e:
            db_session.rollback()
            return Response.error(f"Error al crear registro: {str(e)}")