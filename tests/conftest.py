from pathlib import Path
import os
import sys
from datetime import date, time, timedelta
import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from main import app
from models.Especialidad import Especialidad
from models.Persona import Persona
from models.CatalogoDiagnostico import CatalogoDiagnostico
from models.Medicamento import Medicamento
from models.RegistroHistoria import RegistroHistoria
from models.Agenda import Agenda
from models.Cita import Cita
from models.HistoriaClinica import HistoriaClinica

from db.session import Base, BaseAdmin, get_db, get_db_admin

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configuración DB2 (admin)
SQLALCHEMY_DATABASE_URL_ADMIN = "sqlite://"
engine_admin = create_engine(
    SQLALCHEMY_DATABASE_URL_ADMIN,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocalAdmin = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_admin,
)

def override_get_db_admin():
    db = TestingSessionLocalAdmin()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    BaseAdmin.metadata.create_all(bind=engine_admin)
    app.dependency_overrides[get_db_admin] = override_get_db_admin

    yield
    Base.metadata.drop_all(bind=engine)
    BaseAdmin.metadata.drop_all(bind=engine_admin)

    app.dependency_overrides.clear()


@pytest.fixture
def create_agenda_and_cita():
    db = TestingSessionLocal()
    cita_id = 1
    paciente_id = 1
    especialidad_id = 1

    agenda = Agenda(
        id_doctor=1000 + cita_id,
        hora_inicio=time(hour=9),
        hora_fin=time(hour=10),
        fecha=date.today(),
        estado=1,
        id_especialidad=especialidad_id,
    )
    db.add(agenda)
    db.commit()
    db.refresh(agenda)

    cita = Cita(
        id_paciente=paciente_id,
        id_remision=0,
        id_agenda=agenda.id_agenda,
    )
    db.add(cita)
    db.commit()
    db.refresh(cita)

    yield agenda, cita

@pytest.fixture
def create_agenda_and_cita_vencida():
    db = TestingSessionLocal()
    cita_id = 999
    paciente_id = 99
    especialidad_id = 1

    agenda = Agenda(
        id_doctor=2000 + cita_id,
        hora_inicio=time(hour=8),
        hora_fin=time(hour=9),
        fecha=date.today() - timedelta(days=1),
        estado=1,
        id_especialidad=especialidad_id,
    )
    db.add(agenda)
    db.commit()
    db.refresh(agenda)

    cita = Cita(
        id_paciente=paciente_id,
        id_remision=0,
        id_agenda=agenda.id_agenda,
        asistio=None,
    )
    db.add(cita)
    db.commit()
    db.refresh(cita)

    yield agenda, cita

@pytest.fixture
def create_historia_and_catalogo(create_agenda_and_cita):
    db = TestingSessionLocal()
    historia = HistoriaClinica(
        id_historia=uuid.uuid4(),
        id_paciente=1,
        fecha_inicio=date.today(),
        fecha_ult_actualizacion=date.today(),
    )
    db.add(historia)
    db.commit()

    yield historia
@pytest.fixture
def create_diagnostico():
    db= TestingSessionLocal()

    # Verificar si ya existe algún registro en la tabla
    diagnostico_existente = db.query(CatalogoDiagnostico).first()

    if diagnostico_existente:
        diagnostico = diagnostico_existente
    else:
        diagnostico = CatalogoDiagnostico(
            id_diagnostico=1,
            nombre_enfermedad="Prueba",
        )
        db.add(diagnostico)
        db.commit()
        db.refresh(diagnostico)

    yield diagnostico

@pytest.fixture
def create_registro_historia( create_historia_and_catalogo):
    db = TestingSessionLocal()
    historia = create_historia_and_catalogo

    registro = RegistroHistoria(
        observaciones="observacion anterior",
        tratamiento="tratamiento anterior",
        id_historia=historia.id_historia,
        id_cita=1,
        id_diagnostico=1,
    )
    db.add(registro)
    db.commit()
    db.refresh(registro)

    yield registro

@pytest.fixture 
def create_medicamento():
    db= TestingSessionLocal()

    # Verificar si ya existe el medicamento
    medicamento_existente = db.query(Medicamento).filter(Medicamento.codigo == 1).first()
    
    if medicamento_existente:
        yield medicamento_existente
    else:
        medicamento = Medicamento(
            codigo=1,
            nombre_medicamento="Paracetamol",
            reg_invima=1,
            principio_activo="Paracetamol",
            presentacion="Tabletas"
        )
        db.add(medicamento)
        db.commit()
        db.refresh(medicamento)

        yield medicamento

@pytest.fixture()
def create_persona():
    db = TestingSessionLocalAdmin()

    p = Persona(num_documento=123456789, nombres="Juan", apellidos="Pérez")
    db.add(p)
    db.commit()
    db.refresh(p)

    yield p
@pytest.fixture()
def create_especialidad():
    db = TestingSessionLocalAdmin()

    p = Especialidad(id_especialidad=1, nombre_especialidad="Cardiología")
    db.add(p)
    db.commit()
    db.refresh(p)

    yield p

@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

        
@pytest.fixture()
def client():
    return TestClient(app)

