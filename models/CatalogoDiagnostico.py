from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship

from db.session import Base


class CatalogoDiagnostico(Base):
    __tablename__ = 'catalogo_diagnosticos'

    id_diagnostico = Column(Integer, primary_key=True)
    nombre_enfermedad = Column(VARCHAR(50), nullable=False)

    registros_historia = relationship('RegistroHistoria', back_populates='catalogo_diagnostico')

    def __repr__(self):
        return (f"CatalogoDiagnostico(id_diagnostico={self.id_diagnostico}, "
                f"nombre_enfermedad='{self.nombre_enfermedad}')")