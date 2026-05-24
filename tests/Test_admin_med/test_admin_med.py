import pytest
from unittest.mock import MagicMock
from datetime import datetime
from main import app
from db.session import get_db, get_db_audit
from models.PrescripcionesItems import PrescripcionesItems

# IMPORTANTE: NO instanciar TestClient(app) a nivel de módulo.
# Hacerlo antes de que setup_test_db registre los overrides hace que el
# cliente capture el estado sin auth bypasseado → 401 en todos los tests.
# Usar el fixture `client` definido en conftest.py.

class MockObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

@pytest.fixture
def db_mock():
    mock = MagicMock()
    def side_effect_flush(*args, **kwargs):
        for call in mock.add.call_args_list:
            obj = call[0][0]
            if hasattr(obj, 'id_admin_med') and not obj.id_admin_med:
                obj.id_admin_med = 100
    mock.flush.side_effect = side_effect_flush
    return mock

def test_post_admin_med_multiple_items_success(client, db_mock):
    # Override get_db_audit (el router AdminMedicamentos usa get_db_audit, no get_db)
    app.dependency_overrides[get_db_audit] = lambda: db_mock

    item1 = MagicMock(spec=PrescripcionesItems); item1.id_items = 50
    item2 = MagicMock(spec=PrescripcionesItems); item2.id_items = 60

    chain = db_mock.query.return_value.join.return_value.filter.return_value
    chain.filter.return_value = chain
    chain.first.side_effect = [item1, item2]

    payload = {
        "id_enfermera": 2021100,
        "id_hospitalizacion": 1,
        "admin_med_items": [50, 60]
    }

    response = client.post("/api/administracion_medicamentos", json=payload)

    assert response.status_code == 200
    assert response.json()["hasError"] is False
    assert db_mock.commit.called

    # Restaurar el override original al terminar el test
    from tests.Test_admin_med.conftest import override_get_db_audit
    app.dependency_overrides[get_db_audit] = override_get_db_audit

def test_get_admin_med_success_and_grouping(client, db_mock):
    app.dependency_overrides[get_db_audit] = lambda: db_mock

    admin_data = MockObject(
        id_admin_med=100,
        id_enfermera=2021100,
        id_hospitalizacion=1,
        fecha_admin=datetime(2026, 5, 13, 10, 0, 0)
    )

    adm_item1 = MockObject(id_admin_items=1)
    presc1 = MockObject(id_items=50)
    med1 = MockObject(codigo=1010, nombre_medicamento="Ibuprofeno")

    adm_item2 = MockObject(id_admin_items=2)
    presc2 = MockObject(id_items=60)
    med2 = MockObject(codigo=2020, nombre_medicamento="Amoxicilina")

    query_mock = db_mock.query.return_value
    j1 = MagicMock(); query_mock.join.return_value = j1
    j2 = MagicMock(); j1.join.return_value = j2
    j3 = MagicMock(); j2.join.return_value = j3

    f_mock = MagicMock()
    j3.filter.return_value = f_mock
    f_mock.filter.return_value = f_mock

    f_mock.all.return_value = [
        (admin_data, adm_item1, presc1, med1),
        (admin_data, adm_item2, presc2, med2)
    ]

    response = client.get("/api/administracion_medicamentos/1")

    assert response.status_code == 200
    res_json = response.json()
    assert res_json["hasError"] is False
    assert len(res_json["Data"]) == 1
    assert len(res_json["Data"][0]["items_administrados"]) == 2
    assert res_json["Data"][0]["items_administrados"][0]["medicamento"]["nombre_medicamento"] == "Ibuprofeno"

    from tests.Test_admin_med.conftest import override_get_db_audit
    app.dependency_overrides[get_db_audit] = override_get_db_audit

def test_get_admin_med_with_filters(client, db_mock):
    app.dependency_overrides[get_db_audit] = lambda: db_mock

    f_mock = db_mock.query.return_value.join.return_value.join.return_value.join.return_value.filter.return_value
    f_mock.filter.return_value = f_mock
    f_mock.all.return_value = []

    response = client.get("/api/administracion_medicamentos/1?id_enfermera=2021100")

    assert response.status_code == 200
    assert f_mock.filter.call_count >= 1

    from tests.Test_admin_med.conftest import override_get_db_audit
    app.dependency_overrides[get_db_audit] = override_get_db_audit

def test_get_admin_med_not_found_or_empty(client, db_mock):
    """Prueba el comportamiento cuando no hay registros."""
    app.dependency_overrides[get_db_audit] = lambda: db_mock

    f_mock = db_mock.query.return_value.join.return_value.join.return_value.join.return_value.filter.return_value
    f_mock.filter.return_value = f_mock
    f_mock.all.return_value = []

    response = client.get("/api/administracion_medicamentos/999")

    assert response.status_code == 200
    assert response.json()["Data"] == []

    from tests.Test_admin_med.conftest import override_get_db_audit
    app.dependency_overrides[get_db_audit] = override_get_db_audit

def test_get_admin_med_error_500(client, db_mock):
    app.dependency_overrides[get_db_audit] = lambda: db_mock

    db_mock.query.return_value.join.return_value.join.return_value.join.return_value.filter.return_value.all.side_effect = Exception("Falla crítica")

    response = client.get("/api/administracion_medicamentos/1")

    assert response.status_code == 500
    assert "Error al obtener los registros" in response.json()["detail"]

    from tests.Test_admin_med.conftest import override_get_db_audit
    app.dependency_overrides[get_db_audit] = override_get_db_audit