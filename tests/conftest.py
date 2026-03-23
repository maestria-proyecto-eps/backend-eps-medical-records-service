from pathlib import Path
import os
import sys
from datetime import date, time
import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from main import app
from models.CatalogoDiagnostico import CatalogoDiagnostico
from models.Medicamento import Medicamento
from models.RegistroHistoria import RegistroHistoria
from models.Agenda import Agenda
from models.Cita import Cita
from models.HistoriaClinica import HistoriaClinica

from db.session import Base, get_db

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


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(bind=engine)
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
def client():
    return TestClient(app)
