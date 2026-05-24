from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, SmallInteger, String, Text

from db.session import Base


class Triage(Base):
    __tablename__ = "triages"

    id_triage = Column(Integer, primary_key=True)
    id_paciente = Column(BigInteger, nullable=False)
    id_enfermero = Column(Integer, nullable=False)
    motivo = Column(String(100), nullable=False)
    nivel = Column(SmallInteger, nullable=False)
    antecedentes = Column(String(200), nullable=True)
    fechat = Column(DateTime, nullable=False)
    estado = Column(SmallInteger, nullable=False)
    alergias = Column(String(100), nullable=True)
    hallazgos = Column(Text, nullable=True)
    medicamentos = Column(String(300), nullable=True)
    pulso = Column(String(50), nullable=True)
    presion_arterial = Column(String(50), nullable=True)
    frecuencia_cardiaca = Column(String(50), nullable=True)
    frecuencia_respiratoria = Column(String(50), nullable=True)
    temperatura = Column(String(50), nullable=True)
    saturacion_oxigeno = Column(String(50), nullable=True)
    escala_dolor = Column(SmallInteger, nullable=True)
    riesgo_vital = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"Triage(id_triage={self.id_triage}, id_paciente={self.id_paciente}, nivel={self.nivel}, estado={self.estado})"