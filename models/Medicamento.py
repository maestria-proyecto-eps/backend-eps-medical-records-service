from sqlalchemy import Column, Integer, VARCHAR

from db.session import Base


class Medicamento(Base):
    __tablename__ = 'medicamentos'

    codigo = Column(Integer, primary_key=True, autoincrement=True)
    nombre_medicamento = Column(VARCHAR(50), nullable=False)
    reg_invima = Column(Integer, nullable=False)
    principio_activo = Column(VARCHAR(50), nullable=False)
    presentacion = Column(VARCHAR(50), nullable=False)

    def __repr__(self):
        return (f"Medicamento(codigo={self.codigo}, nombre_medicamento='{self.nombre_medicamento}', "
                f"reg_invima={self.reg_invima}, principio_activo='{self.principio_activo}', "
                f"presentacion='{self.presentacion}')")
