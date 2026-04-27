from sqlalchemy import func, select, union
from sqlalchemy.orm import Session, selectinload

from models.Prescripciones import Prescripciones
from models.Cita import Cita
from models.Agenda import Agenda
from models.AtencionUrgencias import AtencionUrgencias
from models.AtencionHospitalizacion import AtencionHospitalizacion
from models.Hospitalizacion import Hospitalizacion
from models.Triage import Triage

class PrescripcionesRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear_prescripcion(self, prescripcion_data: dict):
        """Crea una nueva prescripción (sin commit, para usar en transacciones)"""
        nueva_prescripcion = Prescripciones(**prescripcion_data)
        self.db.add(nueva_prescripcion)
        # No hacer commit aquí, se hace en la transacción
        return nueva_prescripcion
    
    def crear_prescripcionConGuardado(self, prescripcion_data: Prescripciones):
        self.db.add(prescripcion_data)
    def obtener_preinscripcionPorFiltros(self, idPreinscripcion:int, idAtencion:int, tipo:int, pag: int, cantidad: int):
        query = select(Prescripciones).options(selectinload(Prescripciones.prescripciones_items))
        if idPreinscripcion is not None:
            query = query.where(Prescripciones.id_prescripcion == idPreinscripcion)
        if idAtencion is not None:
            query = query.where(Prescripciones.id_atencion == idAtencion)
        if tipo is not None:
            query = query.where(Prescripciones.tipo == tipo)
            
        count_query = select(func.count()).select_from(query.subquery())
        total = self.db.execute(count_query).scalar_one()
        offset = (pag - 1) * cantidad

        query = (
            query
            .offset(offset)
            .limit(cantidad)
        )

        result = self.db.execute(query)
        prescripciones = result.scalars().all()
    
        return prescripciones, total
        
    def obtener_por_doctor(self, num_doc_doctor: int, pag: int, cantidad: int):
        q1 = (
            select(Prescripciones.id_prescripcion)
            .join(Cita, (Prescripciones.tipo == 1) & (Prescripciones.id_atencion == Cita.id_cita))
            .join(Agenda, Cita.id_agenda == Agenda.id_agenda)
            .where(Agenda.id_doctor == num_doc_doctor)
        )

        q2 = (
            select(Prescripciones.id_prescripcion)
            .join(AtencionUrgencias, (Prescripciones.tipo == 2) & (Prescripciones.id_atencion == AtencionUrgencias.id_urgencia))
            .where(AtencionUrgencias.id_doctor == num_doc_doctor)
        )

        q3 = (
            select(Prescripciones.id_prescripcion)
            .join(AtencionHospitalizacion, (Prescripciones.tipo == 3) & (Prescripciones.id_atencion == AtencionHospitalizacion.id_atencionh))
            .where(AtencionHospitalizacion.id_doctor == num_doc_doctor)
        )

        union_query = union(q1, q2, q3).subquery()

        count_query = select(func.count()).select_from(union_query)
        total = self.db.execute(count_query).scalar_one()

        offset = (pag - 1) * cantidad

        ids_query = (
            select(union_query.c.id_prescripcion)
            .order_by(union_query.c.id_prescripcion.desc())
            .offset(offset)
            .limit(cantidad)
        )
        ids = [row[0] for row in self.db.execute(ids_query).all()]

        if not ids:
            return [], total

        query = (
            select(Prescripciones)
            .options(selectinload(Prescripciones.prescripciones_items))
            .where(Prescripciones.id_prescripcion.in_(ids))
        )

        prescripciones = self.db.execute(query).scalars().all()
        return prescripciones, total


    def obtener_por_paciente(self, num_doc_paciente: int, pag: int, cantidad: int):
        q1 = (
            select(Prescripciones.id_prescripcion)
            .join(Cita, (Prescripciones.tipo == 1) & (Prescripciones.id_atencion == Cita.id_cita))
            .where(Cita.id_paciente == num_doc_paciente)
        )

        q2 = (
            select(Prescripciones.id_prescripcion)
            .join(AtencionUrgencias, (Prescripciones.tipo == 2) & (Prescripciones.id_atencion == AtencionUrgencias.id_urgencia))
            .join(Triage, AtencionUrgencias.id_triage == Triage.id_triage)
            .where(Triage.id_paciente == num_doc_paciente)
        )

        q3 = (
            select(Prescripciones.id_prescripcion)
            .join(AtencionHospitalizacion, (Prescripciones.tipo == 3) & (Prescripciones.id_atencion == AtencionHospitalizacion.id_atencionh))
            .join(Hospitalizacion, AtencionHospitalizacion.id_hospitalizacion == Hospitalizacion.id_hospitalizacion)
            .join(AtencionUrgencias, Hospitalizacion.id_urgencia == AtencionUrgencias.id_urgencia)
            .join(Triage, AtencionUrgencias.id_triage == Triage.id_triage)
            .where(Triage.id_paciente == num_doc_paciente)
        )

        union_query = union(q1, q2, q3).subquery()

        count_query = select(func.count()).select_from(union_query)
        total = self.db.execute(count_query).scalar_one()

        offset = (pag - 1) * cantidad

        ids_query = (
            select(union_query.c.id_prescripcion)
            .order_by(union_query.c.id_prescripcion.desc())
            .offset(offset)
            .limit(cantidad)
        )
        ids = [row[0] for row in self.db.execute(ids_query).all()]

        if not ids:
            return [], total

        query = (
            select(Prescripciones)
            .options(selectinload(Prescripciones.prescripciones_items))
            .where(Prescripciones.id_prescripcion.in_(ids))
        )

        prescripciones = self.db.execute(query).scalars().all()
        return prescripciones, total