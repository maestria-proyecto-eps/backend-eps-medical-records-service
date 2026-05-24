from sqlalchemy import BigInteger, Column, Integer, ForeignKey, TIMESTAMP
from datetime import datetime

from db.session import Base


class AdminMed(Base):
    __tablename__ = "administracion_medicamentos"

    id_admin_med = Column(Integer, primary_key=True)
    id_enfermera = Column(BigInteger, nullable=False)
    fecha_admin = Column(TIMESTAMP, default=datetime.now)
    id_hospitalizacion = Column(Integer, ForeignKey("hospitalizaciones.id_hospitalizacion"),nullable=False)




