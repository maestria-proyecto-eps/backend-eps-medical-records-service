from sqlalchemy.orm import Session, joinedload

from models import Cita


class CitaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_cita(self, cita_data):
        # Logic to create a new Cita in the database
        pass

    def get_cita_by_id(self, cita_id):
        return self.db.query(Cita).options(joinedload(Cita.agenda)).filter(Cita.id_cita == cita_id).first()