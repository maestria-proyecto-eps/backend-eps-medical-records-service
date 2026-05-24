from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, Text

from db.session import Base


class AtencionHospitalizacion(Base):
    __tablename__ = "atencion_hospitalizaciones"

    id_atencionh = Column(Integer, primary_key=True)
    id_doctor = Column(BigInteger, nullable=False)
    id_diagnostico = Column(Integer, nullable=False)
    id_hospitalizacion = Column(Integer, ForeignKey("hospitalizaciones.id_hospitalizacion"), nullable=False)
    fecha_atencionh = Column(DateTime, nullable=False)
    observaciones = Column(Text, nullable=False)
    tratamiento = Column(Text, nullable=False)

    def __repr__(self):
        return f"AtencionHospitalizacion(id_atencionh={self.id_atencionh}, id_doctor={self.id_doctor}, id_hospitalizacion={self.id_hospitalizacion})"