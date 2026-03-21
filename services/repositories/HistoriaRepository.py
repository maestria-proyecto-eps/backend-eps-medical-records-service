from sqlalchemy.orm import Session, joinedload

from models.HistoriaClinica import HistoriaClinica
from models.RegistroHistoria import RegistroHistoria


class HistoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_patient_id(self, id_paciente: int):
        return (
            self.db.query(HistoriaClinica)
            .options(
                joinedload(HistoriaClinica.registros_historia).options(
                    joinedload(RegistroHistoria.catalogo_diagnostico)
                )
            )
            .filter(HistoriaClinica.id_paciente == id_paciente)
            .all()
        )

    def crear_historia(self, historia_data: HistoriaClinica):
        """Crea una nueva historia clínica"""

        self.db.add(historia_data)
        self.db.commit()
        self.db.refresh(historia_data)
        return historia_data

    def existe_historia_por_paciente(self, id_paciente: int) -> bool:
        """Verifica si ya existe una historia clínica para el paciente"""
        return self.db.query(HistoriaClinica).filter(HistoriaClinica.id_paciente == id_paciente).first() is not None