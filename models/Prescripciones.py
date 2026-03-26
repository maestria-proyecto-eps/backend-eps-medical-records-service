from sqlalchemy import Column, Integer, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

from db.session import Base


class Prescripciones(Base):
    __tablename__ = 'prescripciones'

    id_prescripcion = Column(Integer, primary_key=True, autoincrement=True)
    id_atencion = Column(SmallInteger, nullable=False)
    tipo = Column(SmallInteger, nullable=False)  # Tipo de atención: hospitalización, urgencias, etc.

    prescripciones_items = relationship('PrescripcionesItems', back_populates='prescripcion')

    def __repr__(self):
        return (f"Prescripciones(id_prescripcion={self.id_prescripcion}, "
                f"id_atencion={self.id_atencion}, tipo={self.tipo})")
