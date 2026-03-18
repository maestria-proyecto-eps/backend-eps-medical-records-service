from sqlalchemy import BigInteger, Column, Date, Integer, SmallInteger, Time
from sqlalchemy.orm import relationship

from db.session import Base


class Agenda(Base):
    __tablename__ = "agenda"
    id_agenda = Column(Integer, primary_key=True)
    id_doctor = Column(BigInteger, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    fecha = Column(Date, nullable=False)
    estado = Column(SmallInteger, nullable=False)
    id_especialidad = Column(Integer, nullable=False)
    hora_fin = Column(Time, nullable=False)

    cita = relationship("Cita", back_populates="agenda")


    def __repr__(self):
        return f"Agenda(id={self.id_agenda}, id_doctor={self.id_doctor}, hora_inicio='{self.hora_inicio}', fecha='{self.fecha}', estado={self.estado}, id_especialidad={self.id_especialidad}, hora_fin='{self.hora_fin}')"