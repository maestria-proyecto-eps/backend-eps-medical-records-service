from sqlalchemy.orm import Session

from models.PrescripcionesItems import PrescripcionesItems


class PrescripcionesItemsRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear_prescripcion_item(self, item_data: dict):
        """Crea un nuevo item de prescripción (sin commit, para usar en transacciones)"""
        nuevo_item = PrescripcionesItems(**item_data)
        self.db.add(nuevo_item)
        # No hacer commit aquí, se hace en la transacción
        return nuevo_item