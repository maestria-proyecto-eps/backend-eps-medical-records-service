from sqlalchemy.orm import Session

from models.Persona import Persona


class PersonaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_usuario_by_num_documento(self, num_documento):
        return self.db.query(Persona).filter(Persona.num_documento == num_documento).first()