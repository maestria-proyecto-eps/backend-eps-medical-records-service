from datetime import date

from sqlalchemy import BigInteger, Column, Integer, SmallInteger, Time


class Agenda:
    _table_name = "agenda"
    id_agenda = Column(Integer, primary_key=True)
    id_doctor = Column(BigInteger, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    fecha = Column(date, nullable=False)
    estado = Column(SmallInteger, nullable=False)
    id_especialidad = Column(Integer, nullable=False)
    hora_fin = Column(Time, nullable=False)

    

    def __str__(self):
        return f"Agenda(id={self.id_agenda}, id_doctor={self.id_doctor}, hora_inicio='{self.hora_inicio}', fecha='{self.fecha}', estado={self.estado}, id_especialidad={self.id_especialidad}, hora_fin='{self.hora_fin}')"