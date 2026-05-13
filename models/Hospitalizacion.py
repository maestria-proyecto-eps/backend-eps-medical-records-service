from sqlalchemy import Column, DateTime, ForeignKey, Integer, SmallInteger

from db.session import Base


class Hospitalizacion(Base):
    __tablename__ = "hospitalizaciones"

    id_hospitalizacion = Column(Integer, primary_key=True)
    id_urgencia = Column(Integer, ForeignKey("atencion_urgencias.id_urgencia"), nullable=False)
    num_cama = Column(Integer, nullable=False)
    ingreso = Column(DateTime, nullable=False)
    salida = Column(DateTime, nullable=True)
    estado = Column(SmallInteger, nullable=False)

    def __repr__(self):
        return f"Hospitalizacion(id_hospitalizacion={self.id_hospitalizacion}, id_urgencia={self.id_urgencia}, num_cama={self.num_cama})"