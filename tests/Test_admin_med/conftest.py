"""
tests/Test_admin_med/conftest.py
"""
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from db.session import get_db, get_db_admin, get_db_audit, get_db_admin_audit
from core.auth_utils import get_current_user_id
from core.dependencias import get_usuario_actual

# Importar modelos para que Base registre las tablas
from models.user import USUARIOS, ROLES  # noqa: F401

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
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def override_get_db_admin():
    db = TestingSessionLocalAdmin()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def override_get_db_audit():
    # get_db_audit ejecuta SET LOCAL en Postgres — no compatible con SQLite.
    # En tests simplemente usamos una sesión SQLite sin auditoría.
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
# Mock de usuario
# ---------------------------------------------------------------------------
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
    """
    Registra overrides de BD y auth para toda la sesión de tests.
    NO usar clear_dependency_overrides con autouse=True — eso borra los
    overrides de auth y restaura HTTPBearer → 401 en todos los tests.
    """
    from db.session import Base, BaseAdmin
    Base.metadata.create_all(bind=engine)
    BaseAdmin.metadata.create_all(bind=engine_admin)

    # BD
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_db_admin] = override_get_db_admin
    app.dependency_overrides[get_db_audit] = override_get_db_audit
    app.dependency_overrides[get_db_admin_audit] = override_get_db_admin_audit

    # Auth: cortar HTTPBearer en la raíz
    app.dependency_overrides[get_current_user_id] = lambda: 1
    app.dependency_overrides[get_usuario_actual] = lambda: make_mock_usuario("Administrador")

    yield

    Base.metadata.drop_all(bind=engine)
    BaseAdmin.metadata.drop_all(bind=engine_admin)
    app.dependency_overrides.clear()

# ---------------------------------------------------------------------------
# Fixtures de tests
# ---------------------------------------------------------------------------
@pytest.fixture()
def client():
    """
    Fixture de client — NO usar TestClient(app) a nivel de módulo en los
    tests, ya que se instancia antes de que los overrides estén activos.
    Usar este fixture en su lugar.
    """
    return TestClient(app)