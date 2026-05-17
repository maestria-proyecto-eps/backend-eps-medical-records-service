"""
tests/Test_medical_record_service/conftest.py
"""
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
from jose import jwt

from main import app
from db.session import Base, BaseAdmin, get_db, get_db_admin, get_db_audit, get_db_admin_audit
from core.auth_utils import get_current_user_id
from core.dependencias import get_usuario_actual

from models.user import USUARIOS, ROLES          # noqa: F401
from models.Especialidad import Especialidad
from models.Persona import Persona
from models.CatalogoDiagnostico import CatalogoDiagnostico
from models.Medicamento import Medicamento
from models.RegistroHistoria import RegistroHistoria
from models.Agenda import Agenda
from models.Cita import Cita
from models.HistoriaClinica import HistoriaClinica
from models.Remisiones import Remisiones

# ---------------------------------------------------------------------------
# Engines SQLite en memoria
# ---------------------------------------------------------------------------
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

engine_admin = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocalAdmin = sessionmaker(autocommit=False, autoflush=False, bind=engine_admin)

# ---------------------------------------------------------------------------
# Overrides de BD
# ---------------------------------------------------------------------------
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_db_admin():
    db = TestingSessionLocalAdmin()
    try:
        yield db
    finally:
        db.close()

def override_get_db_audit():
    # get_db_audit ejecuta SET LOCAL en Postgres — no compatible con SQLite.
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def override_get_db_admin_audit():
    db = TestingSessionLocalAdmin()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# ---------------------------------------------------------------------------
# Mock de usuario y JWT para tests
# ---------------------------------------------------------------------------
# IMPORTANTE: Los tests de /patients/me y /doctors/me pasan tokens JWT reales.
# Esos endpoints usan get_current_patient_user / get_current_doctor_user que
# decodifican el token con settings.JWT_SECRET. Para que funcionen en tests,
# el token debe firmarse con el mismo secret.
# Como no tenemos acceso a settings.JWT_SECRET aquí, los tests que dependen
# de tokens reales necesitan que get_current_user_id NO esté overrideado
# para esos endpoints. La solución es usar HTTPBearer(auto_error=False) o
# pasar el token con el secret correcto. Por ahora se usa "dummy-secret"
# consistentemente — si el secret de producción es diferente, esos tests
# fallarán con 401/404 hasta que se alinee el secret.

TEST_JWT_SECRET = "dummy-secret"
TEST_JWT_ALG = "HS256"

def make_mock_usuario(rol_nombre: str) -> USUARIOS:
    rol = ROLES(id_rol=1, nombre_rol=rol_nombre)
    user = USUARIOS(
        id_usuario=1,
        num_documento=999999999,
        password="x",
        id_rol=1,
        estado=True,
        intentos_login=0,
    )
    user.rol = rol
    return user

# ---------------------------------------------------------------------------
# Setup de sesión (scope=session, autouse)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    BaseAdmin.metadata.create_all(bind=engine_admin)

    # BD — las 4 funciones de sesión
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_db_admin] = override_get_db_admin
    app.dependency_overrides[get_db_audit] = override_get_db_audit
    app.dependency_overrides[get_db_admin_audit] = override_get_db_admin_audit

    # Auth: cortar HTTPBearer → devolver user_id=1 sin validar token
    app.dependency_overrides[get_current_user_id] = lambda: 1
    # get_usuario_actual → usuario mock con rol Administrador
    # (pasa RequireRole de cualquier rol, incluido Médico, Paciente, Enfermero)
    app.dependency_overrides[get_usuario_actual] = lambda: make_mock_usuario("Administrador")

    yield

    Base.metadata.drop_all(bind=engine)
    BaseAdmin.metadata.drop_all(bind=engine_admin)
    app.dependency_overrides.clear()

# ---------------------------------------------------------------------------
# Fixture de cliente
# ---------------------------------------------------------------------------
@pytest.fixture()
def client():
    return TestClient(app)

# ---------------------------------------------------------------------------
# Fixture de sesión directa
# ---------------------------------------------------------------------------
@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------------------------
# Fixtures de datos
# ---------------------------------------------------------------------------
@pytest.fixture
def create_agenda_and_cita():
    db = TestingSessionLocal()
    agenda = Agenda(
        id_doctor=1001,
        hora_inicio=time(hour=9),
        hora_fin=time(hour=10),
        fecha=date.today(),
        estado=1,
        id_especialidad=1,
    )
    db.add(agenda)
    db.commit()
    db.refresh(agenda)

    cita = Cita(
        id_paciente=1,
        id_remision=0,
        id_agenda=agenda.id_agenda,
    )
    db.add(cita)
    db.commit()
    db.refresh(cita)
    db.close()
    yield agenda, cita

@pytest.fixture
def create_agenda_and_cita_vencida():
    db = TestingSessionLocal()
    agenda = Agenda(
        id_doctor=2999,
        hora_inicio=time(hour=8),
        hora_fin=time(hour=9),
        fecha=date.today() - timedelta(days=1),
        estado=1,
        id_especialidad=1,
    )
    db.add(agenda)
    db.commit()
    db.refresh(agenda)

    cita = Cita(
        id_paciente=99,
        id_remision=0,
        id_agenda=agenda.id_agenda,
        asistio=None,
    )
    db.add(cita)
    db.commit()
    db.refresh(cita)
    db.close()
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
    db.refresh(historia)
    db.close()
    yield historia

@pytest.fixture
def create_diagnostico():
    db = TestingSessionLocal()
    diagnostico_existente = db.query(CatalogoDiagnostico).first()
    if diagnostico_existente:
        db.close()
        yield diagnostico_existente
    else:
        diagnostico = CatalogoDiagnostico(
            id_diagnostico=1,
            nombre_enfermedad="Prueba",
        )
        db.add(diagnostico)
        db.commit()
        db.refresh(diagnostico)
        db.close()
        yield diagnostico

@pytest.fixture
def create_registro_historia(create_historia_and_catalogo):
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
    db.close()
    yield registro

@pytest.fixture
def create_medicamento():
    db = TestingSessionLocal()
    medicamento_existente = db.query(Medicamento).filter(Medicamento.codigo == 1).first()
    if medicamento_existente:
        db.close()
        yield medicamento_existente
    else:
        medicamento = Medicamento(
            codigo=1,
            nombre_medicamento="Paracetamol",
            reg_invima=1,
            principio_activo="Paracetamol",
            presentacion="Tabletas",
        )
        db.add(medicamento)
        db.commit()
        db.refresh(medicamento)
        db.close()
        yield medicamento

@pytest.fixture()
def create_persona():
    db = TestingSessionLocalAdmin()
    p = Persona(num_documento=123456789, nombres="Juan", apellidos="Pérez")
    db.add(p)
    db.commit()
    db.refresh(p)
    db.close()
    yield p

@pytest.fixture()
def create_especialidad():
    db = TestingSessionLocalAdmin()
    existente = db.query(Especialidad).filter(Especialidad.id_especialidad == 1).first()
    if existente:
        db.close()
        yield existente
    else:
        p = Especialidad(id_especialidad=1, nombre_especialidad="Cardiología", requiere_remision=False)
        db.add(p)
        db.commit()
        db.refresh(p)
        db.close()
        yield p

@pytest.fixture
def create_remision():
    db = TestingSessionLocal()
    remision = Remisiones(
        expiracion=date.today() + timedelta(days=10),
        id_paciente=123456789,
        id_registro=1,
        id_especialidad=1,
    )
    db.add(remision)
    db.commit()
    db.refresh(remision)
    db.close()
    yield remision

# ---------------------------------------------------------------------------
# Tokens JWT para tests que los requieren explícitamente
# (/patients/me, /doctors/me usan get_current_patient_user que decodifica
# el token con settings.JWT_SECRET — si el secret de producción difiere
# de TEST_JWT_SECRET, esos endpoints devolverán 401. Alinear el secret
# en .env de CI con TEST_JWT_SECRET = "dummy-secret" para que pasen.)
# ---------------------------------------------------------------------------
@pytest.fixture
def paciente_token():
    payload = {
        "id_usuario": 44,
        "num_documento": 1018442903,
        "id_role": 3,
        "role": "Paciente",
    }
    return jwt.encode(payload, TEST_JWT_SECRET, algorithm=TEST_JWT_ALG)

@pytest.fixture
def doctor_token():
    payload = {
        "id_usuario": 55,
        "num_documento": 9999999999,
        "id_role": 2,
        "role": "Doctor",
    }
    return jwt.encode(payload, TEST_JWT_SECRET, algorithm=TEST_JWT_ALG)