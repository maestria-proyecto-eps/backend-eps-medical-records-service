from sqlalchemy import BigInteger, Column, Date, Integer
from sqlalchemy.orm import relationship

from db.session import Base


class HistoriaClinica(Base):
    __tablename__ = 'historias_clinicas'

    id_historia = Column(BigInteger, primary_key=True)
    id_paciente = Column(BigInteger, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_ult_actualizacion = Column(Date, nullable=False)

    registros_historia = relationship('RegistroHistoria', backref='historia_clinica')

    def __repr__(self):
        return (f"HistoriaClinica(id_historia={self.id_historia}, id_paciente={self.id_paciente}, "
                f"fecha_inicio={self.fecha_inicio}, fecha_ult_actualizacion={self.fecha_ult_actualizacion})")