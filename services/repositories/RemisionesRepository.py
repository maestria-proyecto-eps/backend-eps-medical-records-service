from sqlalchemy.orm import Session

from models.Remisiones import Remisiones


class RemisionesRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_remision(self, fecha_expiracion, id_paciente, id_registro, id_especialidad):
        nueva_remision = Remisiones(
            expiracion=fecha_expiracion,
            id_paciente=id_paciente,
            id_registro=id_registro,
            id_especialidad=id_especialidad
        )
        self.db.add(nueva_remision)
        self.db.commit()
        self.db.refresh(nueva_remision)
        return nueva_remision

