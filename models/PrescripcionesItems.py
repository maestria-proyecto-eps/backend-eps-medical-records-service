from sqlalchemy import Column, Integer, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship

from db.session import Base


class PrescripcionesItems(Base):
    __tablename__ = 'prescripciones_items'

    id_items = Column(Integer, primary_key=True, autoincrement=True)
    cantidad = Column(Integer, nullable=False)
    dosis = Column(VARCHAR(50), nullable=False)
    duracion = Column(Integer, nullable=False)
    id_prescripcion = Column(Integer, ForeignKey('prescripciones.id_prescripcion'), nullable=False)
    id_medicamento = Column(Integer, ForeignKey('medicamentos.codigo'), nullable=False)

    prescripcion = relationship('Prescripciones', back_populates='prescripciones_items')
    medicamento = relationship('Medicamento', back_populates='prescripciones_items')

    def __repr__(self):
        return (f"PrescripcionesItems(id_items={self.id_items}, cantidad={self.cantidad}, "
                f"dosis='{self.dosis}', duracion={self.duracion}, id_prescripcion={self.id_prescripcion}, "
                f"id_medicamento={self.id_medicamento})")
