from sqlalchemy import Column, Integer, ForeignKey
from db.session import Base


class AdminMedItems(Base):
    __tablename__ = "administracion_med_items"

    id_admin_items = Column(Integer, primary_key=True)
    id_prescripcion_item =  Column(Integer)
    id_admin_med = Column(Integer, ForeignKey("administracion_medicamentos.id_admin_med"),nullable=False)