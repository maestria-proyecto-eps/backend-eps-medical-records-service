from sqlalchemy import VARCHAR, BigInteger, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.session import Base


class RegistroHistoria(Base):
    __tablename__ = 'registros_historia'
    id_registro= Column(Integer, primary_key=True)
    observaciones = Column(VARCHAR(50), nullable=False)
    tratamiento = Column(VARCHAR(50), nullable=False)
    id_historia = Column(BigInteger, ForeignKey('historias_clinicas.id_historia'), nullable=False)
    id_cita = Column(Integer, ForeignKey('citas.id_cita'), nullable=False)
    id_diagnostico = Column(Integer, ForeignKey('catalogo_diagnosticos.id_diagnostico'), nullable=False)

    cita = relationship('Cita', uselist=False, back_populates='registro_historia')
    historia_clinica = relationship('HistoriaClinica', uselist=False, backref='registros_historia')
    catalogo_diagnostico = relationship('CatalogoDiagnostico', uselist=False, backref='registros_historia')

    def __repr__(self):
        return f"registroHistoria(id_registro={self.id_registro}, observaciones='{self.observaciones}', tratamiento='{self.tratamiento}', id_historia={self.id_historia}, id_cita={self.id_cita}, id_diagnostico={self.id_diagnostico})"