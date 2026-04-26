from sqlalchemy import BigInteger, Column, ForeignKey, Integer, Text

from db.session import Base


class AtencionUrgencias(Base):
    __tablename__ = "atencion_urgencias"

    id_urgencia = Column(Integer, primary_key=True)
    id_doctor = Column(BigInteger, nullable=False)
    id_triage = Column(Integer, ForeignKey("triages.id_triage"), nullable=False)
    id_diagnostico = Column(Integer, nullable=False)
    observaciones = Column(Text, nullable=False)
    tratamiento = Column(Text, nullable=False)

    def __repr__(self):
        return f"AtencionUrgencias(id_urgencia={self.id_urgencia}, id_doctor={self.id_doctor}, id_triage={self.id_triage})"