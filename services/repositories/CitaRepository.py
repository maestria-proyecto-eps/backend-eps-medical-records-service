from datetime import datetime
from sqlalchemy.orm import Session, joinedload

from models.Cita import Cita
from models.Agenda import Agenda

class CitaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_cita_by_id(self, cita_id):
        return self.db.query(Cita).options(joinedload(Cita.agenda)).filter(Cita.id_cita == cita_id).first()
    
    def get_citas_vencidas_sin_asistencia(self):
        ahora = datetime.now()

        citas_pendientes = (
            self.db.query(Cita)
            .join(Agenda, Cita.id_agenda == Agenda.id_agenda)
            .options(joinedload(Cita.agenda))
            .filter(Cita.asistio.is_(None))
            .all()
        )

        return [
            cita
            for cita in citas_pendientes
            if cita.agenda is not None
            and datetime.combine(cita.agenda.fecha, cita.agenda.hora_fin) < ahora
        ]