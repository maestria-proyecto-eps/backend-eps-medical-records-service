from sqlalchemy import Column, Integer, ForeignKey
from db.session import Base


class AdminMedItems(Base):
    __tablename__ = "ADMINISTRACIONMED_ITEMS"

    id_admin_items = Column(Integer, primary_key=True)
    id_prescripcion_items =  Column(Integer)
    id_admin_med = Column(Integer, ForeignKey("administracion_medicamentos.id_admin_med"),nullable=False)
    id_items = Column(Integer, ForeignKey("prescripciones_items.id_items"), nullable=False)