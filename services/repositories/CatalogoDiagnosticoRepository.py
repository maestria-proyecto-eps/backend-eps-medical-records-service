from sqlalchemy import func
from sqlalchemy.orm import Session

from models.CatalogoDiagnostico import CatalogoDiagnostico


class CatalogoDiagnosticoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_catalogo_by_filters(self, id_diagnostico:int=None, nombre:str=None):
        query = self.db.query(CatalogoDiagnostico)
        if id_diagnostico is not None:
            query = query.filter(CatalogoDiagnostico.id_diagnostico == id_diagnostico)
        if nombre is not None:
            query = query.filter(func.lower(CatalogoDiagnostico.nombre_enfermedad).like(nombre.lower()+"%"))
        query = (
            query
            .limit(20)
        )
        return self.db.execute(query).scalars().all()

    def existe_diagnostico_por_id(self, id_diagnostico: int) -> bool:
        """Valida si existe un diagnóstico con el id especificado"""
        return self.db.query(CatalogoDiagnostico).filter(CatalogoDiagnostico.id_diagnostico == id_diagnostico).first() is not None