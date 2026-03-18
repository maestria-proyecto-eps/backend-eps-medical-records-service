from sqlalchemy import VARCHAR, BigInteger, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.session import Base


class RegistroHistoria(Base):
    __tablename__ = 'registros_historia'
    id_registro= Column(Integer, primary_key=True)
    observaciones = Column(VARCHAR(50), nullable=False)
    tratamiento = Column(VARCHAR(50), nullable=False)
    id_historia= Column(BigInteger, nullable=False)
    id_cita= Column(Integer, ForeignKey('citas.id_cita'), nullable=False)
    id_diagnostico= Column(Integer, nullable=False)

    cita = relationship('Cita',uselist=False, back_populates='registro_historia')

    def __repr__(self):
        return f"registroHistoria(id_registro={self.id_registro}, observaciones='{self.observaciones}', tratamiento='{self.tratamiento}', id_historia={self.id_historia}, id_cita={self.id_cita}, id_diagnostico={self.id_diagnostico})"