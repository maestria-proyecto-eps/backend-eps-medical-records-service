from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from models.Medicamento import Medicamento


class MedicamentoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_medicamento_by_filters(self, nombre: str = None):
        query = self.db.query(Medicamento)

        if nombre is not None:
            query = query.filter(or_(func.lower(Medicamento.nombre_medicamento).like(nombre.lower() + "%"),func.lower(Medicamento.principio_activo).like(nombre.lower() + "%")))

        query = query.limit(20)
        return self.db.execute(query).scalars().all()

    def existe_medicamento_por_codigo(self, codigo: int) -> bool:
        """Valida si existe un medicamento con el código especificado"""
        return self.db.query(Medicamento).filter(Medicamento.codigo == codigo).first() is not None
