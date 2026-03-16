


from sqlalchemy import VARCHAR, BigInteger, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.session import Base


class registroHistoria(Base):
    __tablename__ = 'registros_historia'
    id_registro= Column(Integer, primary_key=True)
    observaciones = Column(VARCHAR(50), nullable=False)
    tratamiento = Column(VARCHAR(50), nullable=False)
    id_historia= Column(BigInteger, nullable=False)
    id_cita= Column(Integer, ForeignKey('Citas.id_cita') nullable=False)
    id_diagnostico= Column(Integer, nullable=False)

    cita = relationship('Citas', back_populates='registros_historia')