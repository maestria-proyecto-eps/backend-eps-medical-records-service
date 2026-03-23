from sqlalchemy.orm import Session

from models.RegistroHistoria import RegistroHistoria


class RegistroRepository:
    def __init__(self, db: Session):
        self.db = db

    def exists_by_id_cita(self, id_cita: int) -> bool:
        return self.db.query(self.db.query(RegistroHistoria).filter(RegistroHistoria.id_cita == id_cita).exists()).scalar()

    def exists_by_id_registro_and_id_cita(self, id_registro: int, id_cita: int) -> bool:
        return self.db.query(self.db.query(RegistroHistoria).filter(RegistroHistoria.id_registro == id_registro, RegistroHistoria.id_cita == id_cita).exists()).scalar()

    def get_by_id(self, id_registro: int):
        return self.db.query(RegistroHistoria).filter(RegistroHistoria.id_registro == id_registro).first()

    def crear_registro(self, registro_data: dict):
        """Crea un nuevo registro de historia (sin commit, para usar en transacciones)"""
        nuevo_registro = RegistroHistoria(**registro_data)
        self.db.add(nuevo_registro)
        # No hacer commit aquí, se hace en la transacción
        return nuevo_registro
