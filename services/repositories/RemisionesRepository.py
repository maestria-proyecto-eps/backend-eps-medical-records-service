from datetime import date
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

    def get_all_referrals(self, id_especialidad: int = None, id_paciente: int = None, vigente: bool = None):
        query = self.db.query(Remisiones)

        if id_especialidad is not None:
            query = query.filter(Remisiones.id_especialidad == id_especialidad)

        if id_paciente is not None:
            query = query.filter(Remisiones.id_paciente == id_paciente)

        if vigente is True:
            query = query.filter(Remisiones.expiracion >= date.today())
        elif vigente is False:
            query = query.filter(Remisiones.expiracion < date.today())

        return query.order_by(Remisiones.id_remision.asc()).all()

    def get_referrals_by_patient_id(self, patient_id: int):
        return (
            self.db.query(Remisiones)
            .filter(Remisiones.id_paciente == patient_id)
            .order_by(Remisiones.id_remision.asc())
            .all()
        )