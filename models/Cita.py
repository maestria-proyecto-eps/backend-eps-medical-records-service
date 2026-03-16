from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.session import Base


class Cita(Base):
    __tablename__ = 'citas'
    id_cita = Column(Integer, primary_key=True)
    id_paciente = Column(Integer, nullable=False)
    id_remision = Column(Integer, nullable=False)
    id_agenta = Column(Integer, ForeignKey('agenda.id_agenda'), nullable=False)

    agenda = relationship('agenda', back_populates='citas')

    @property
    def id_especialidad(self):
        return self.agenda.id_especialidad if self.agenda else None

    def __repr__(self):
        return f"Cita(id_cita={self.id_cita}, id_paciente={self.id_paciente}, id_remision={self.id_remision}, id_agenta={self.id_agenta})"