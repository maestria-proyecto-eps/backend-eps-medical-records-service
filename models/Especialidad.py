from sqlalchemy import Boolean, Column, Integer, String

from db.session import BaseAdmin


class Especialidad(BaseAdmin):
    __tablename__ = 'especialidades'

    id_especialidad = Column(Integer, primary_key=True)
    nombre_especialidad = Column(String(50), nullable=False)
    requiere_remision = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return (f"Especialidad(id_especialidad={self.id_especialidad}, "
                f"nombre_especialidad={self.nombre_especialidad}, "
                f"requiere_remision={self.requiere_remision})")