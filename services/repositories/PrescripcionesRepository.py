from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from models.Prescripciones import Prescripciones


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