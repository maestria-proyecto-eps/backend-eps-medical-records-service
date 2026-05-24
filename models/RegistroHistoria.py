from sqlalchemy import VARCHAR, Column, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import relationship

from db.session import Base


class RegistroHistoria(Base):
    __tablename__ = 'registros_historia'
    id_registro= Column(Integer, primary_key=True)
    observaciones = Column(VARCHAR(50), nullable=False)
    tratamiento = Column(VARCHAR(50), nullable=False)
    id_historia = Column(Uuid, ForeignKey('historias_clinicas.id_historia'), nullable=False)
    id_cita = Column(Integer, ForeignKey('citas.id_cita'), nullable=False)
    id_diagnostico = Column(Integer, ForeignKey('catalogo_diagnosticos.id_diagnostico'), nullable=True)

    cita = relationship('Cita', uselist=False, back_populates='registro_historia')
    historia_clinica = relationship('HistoriaClinica', back_populates='registros_historia')
    catalogo_diagnostico = relationship('CatalogoDiagnostico',uselist=False, back_populates='registros_historia')
    remisiones = relationship('Remisiones', back_populates='registro_historia')

    @property
    def nombre_enfermedad(self):
        return self.catalogo_diagnostico.nombre_enfermedad if self.catalogo_diagnostico else "Sin diagnóstico"

    def __repr__(self):
        return f"registroHistoria(id_registro={self.id_registro}, observaciones='{self.observaciones}', tratamiento='{self.tratamiento}', id_historia={self.id_historia}, id_cita={self.id_cita}, id_diagnostico={self.id_diagnostico})"