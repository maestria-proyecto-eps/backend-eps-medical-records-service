from sqlalchemy.orm import Session

from models.Especialidad import Especialidad


class EspecialidadRepository:
    def __init__(self, db: Session):
        self.db = db

    def exists_especialidad_by_id(self, id_especialidad):
        return self.db.query(self.db.query(Especialidad).filter(Especialidad.id_especialidad == id_especialidad).exists()).scalar()
