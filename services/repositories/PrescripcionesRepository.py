from sqlalchemy.orm import Session

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
    
    def crear_prescripcionConGuardado(self, prescripcion_data: Preinscripcion):
        self.db.add(prescripcion_data)