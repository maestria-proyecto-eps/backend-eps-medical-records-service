from sqlalchemy import Column, Integer, Date, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from db.session import Base


class Remisiones(Base):
    __tablename__ = 'remisiones'

    id_remision = Column(Integer, primary_key=True, autoincrement=True)
    fecha_expiracion = Column(Date, nullable=False)
    id_paciente = Column(BigInteger, nullable=False)
    id_registro = Column(Integer, ForeignKey('registros_historia.id_registro'), nullable=False)
    id_especialidad = Column(Integer, nullable=False)

    registro_historia = relationship('RegistroHistoria', back_populates='remisiones')

    def __repr__(self):
        return (f"Remisiones(id_remision={self.id_remision}, "
                f"fecha_expiracion={self.fecha_expiracion}, id_paciente={self.id_paciente}, "
                f"id_registro={self.id_registro}, id_especialidad={self.id_especialidad})")
