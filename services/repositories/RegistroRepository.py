from sqlalchemy.orm import Session

from models.RegistroHistoria import RegistroHistoria


class RegistroRepository:
    def __init__(self, db: Session):
        self.db = db
    def exists_by_id_cita(self, id_cita: int) -> bool:
        return self.db.query(self.db.query(RegistroHistoria).filter(RegistroHistoria.id_cita == id_cita).exists()).scalar()

