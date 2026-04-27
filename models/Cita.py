from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.session import Base

class Cita(Base):
    __tablename__ = 'citas'
    id_cita = Column(Integer, primary_key=True)
    id_paciente = Column(BigInteger, nullable=False)
    id_remision = Column(Integer, nullable=False)
    id_agenda = Column(Integer, ForeignKey("agenda.id_agenda"), nullable=False)
    asistio = Column(Boolean, nullable=True)

    agenda = relationship("Agenda", back_populates="cita")
    registro_historia = relationship("RegistroHistoria", uselist=False, back_populates="cita")

    @property
    def id_especialidad(self):
        return self.agenda.id_especialidad if self.agenda else None

    def __repr__(self):
        return f"Cita(id_cita={self.id_cita}, id_paciente={self.id_paciente}, id_remision={self.id_remision}, id_agenda={self.id_agenda}, asistio={self.asistio})"
    