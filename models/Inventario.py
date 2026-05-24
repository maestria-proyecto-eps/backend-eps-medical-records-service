from sqlalchemy import Column, Date, Integer, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship

from db.session import Base


class Inventario(Base):
    __tablename__ = 'inventario'

    id_inventario = Column(Integer, primary_key=True, autoincrement=True)
    lote = Column(VARCHAR(50), nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    precio_in = Column(Integer, nullable=False)
    codigo = Column(Integer, ForeignKey('medicamentos.codigo'), nullable=False)

    medicamento = relationship('Medicamento', back_populates='inventario_items')

    def __repr__(self):
        return (f"Inventario(id_inventario={self.id_inventario}, lote='{self.lote}', "
                f"cantidad={self.cantidad}, fecha_vencimiento={self.fecha_vencimiento}, "
                f"precio_in={self.precio_in}, codigo={self.codigo})")
