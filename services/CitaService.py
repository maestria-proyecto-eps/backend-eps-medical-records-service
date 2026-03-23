from datetime import datetime, date
import uuid
from schemas.request.RegistroHistoriaRequest import RegistroHistoriaRequest
from schemas.request.RemisionRequest import RemisionRequest
from schemas.response.AppointmentResponse import AppointmentResponse
from schemas.response.GenericResponse import Response
from schemas.response.HistoriaClinicaResponse import RegistroHistoriaResponse
from schemas.response.RemisionResponse import RemisionResponse
from services.repositories import PersonaRepository
from services.repositories.CitaRepository import CitaRepository
from services.repositories.RegistroRepository import RegistroRepository
from services.repositories.CatalogoDiagnosticoRepository import CatalogoDiagnosticoRepository
from services.repositories.MedicamentoRepository import MedicamentoRepository
from services.repositories.PrescripcionesRepository import PrescripcionesRepository
from services.repositories.PrescripcionesItemsRepository import PrescripcionesItemsRepository
from services.repositories.HistoriaRepository import HistoriaRepository
from services.repositories.EspecialidadRepository import EspecialidadRepository
from services.repositories.RemisionesRepository import RemisionesRepository
from models.HistoriaClinica import HistoriaClinica


class CitatService:
    def __init__(self, repo: CitaRepository, repoRegistro: RegistroRepository, 
                 repoCatalogoDiagnostico: CatalogoDiagnosticoRepository,
                 repoMedicamento: MedicamentoRepository ,
                 repoPrescripciones: PrescripcionesRepository ,
                 repoPrescripcionesItems: PrescripcionesItemsRepository,
                 repoHistoria: HistoriaRepository,
                 repoEspecialidad: EspecialidadRepository,
                 repoRemisiones: RemisionesRepository,
                 repoPersona: PersonaRepository):
        self.repo = repo
        self.repoRegistro = repoRegistro
        self.repoCatalogoDiagnostico = repoCatalogoDiagnostico
        self.repoMedicamento = repoMedicamento
        self.repoPrescripciones = repoPrescripciones
        self.repoPrescripcionesItems = repoPrescripcionesItems
        self.repoHistoria = repoHistoria
        self.repoEspecialidad = repoEspecialidad
        self.repoPersona= repoPersona
        self.repoRemisiones = repoRemisiones

    def getRegistroCitaById(self, id_cita):
        if(self.repoRegistro.exists_by_id_cita(id_cita)):
            return Response.error("La cita ya tiene un registro asociado")

        cita = self.repo.get_cita_by_id(id_cita)
        if cita is None:
            return Response.error("La cita no existe")
        info_paciente = self.repoPersona.get_usuario_by_num_documento(cita.id_paciente)
        infoEspecialidad = self.repoEspecialidad.get_especialidad_by_id(cita.id_especialidad)
        data = AppointmentResponse.model_validate(cita).model_dump()

        data["nombreUsuario"] = (
        f"{info_paciente.nombres} {info_paciente.apellidos}"
        if info_paciente else "No encontrado"
        )
        data["nombreEspecialidad"] = (
            infoEspecialidad.nombre_especialidad
            if infoEspecialidad else "No encontrado"
        )



        return Response.ok(data,"Cita obtenida exitosamente")

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

    def crear_remision(self, id_cita: int, remision_data: RemisionRequest):
        # 1. Validar que la cita existe
        cita = self.repo.get_cita_by_id(id_cita)
        if cita is None:
            return Response.error("La cita no existe")

        # 2. Validar especialidad
        if not self.repoEspecialidad.exists_especialidad_by_id(remision_data.id_especialidad):
            return Response.error("La especialidad no existe")

        # 3. Validar expiración futura
        if remision_data.fecha_expiracion <= date.today():
            return Response.error("La fecha de expiración debe ser una fecha futura")

        # 4. Validar que el registro pertenece a esta cita
        if not self.repoRegistro.exists_by_id_registro_and_id_cita(remision_data.id_registro, id_cita):
            return Response.error("El id_registro no pertenece a la cita")

        nueva_remision = self.repoRemisiones.add_remision(
            fecha_expiracion=remision_data.fecha_expiracion,
            id_paciente=cita.id_paciente,
            id_registro=remision_data.id_registro,
            id_especialidad=remision_data.id_especialidad
        )
        remision_response = RemisionResponse.model_validate(nueva_remision)
        return Response.ok(remision_response, "Remisión creada exitosamente")