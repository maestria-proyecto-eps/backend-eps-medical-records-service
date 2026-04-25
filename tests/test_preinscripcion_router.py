import pytest
from tests.conftest import TestingSessionLocal
from models.Cita import Cita
from datetime import date, timedelta, time
from services.PreinscripcionesService import PreinscripcionesService
from services.repositories.PrescripcionesRepository import PrescripcionesRepository
from services.repositories.MedicamentoRepository import MedicamentoRepository
from models.Agenda import Agenda
from models.Medicamento import Medicamento


def test_add_preinscripcion_exitoso(client, create_agenda_and_cita, create_medicamento):
    """Test para crear una preinscripción exitosamente"""
    agenda, cita = create_agenda_and_cita
    medicamento = create_medicamento
    
    preinscripcion_data = {
        "id_atencion": cita.id_cita,
        "tipo": 1,
        "prescripciones_items": [
            {
                "id_medicamento": medicamento.codigo,
                "cantidad": 10,
                "dosis": "500mg",
                "duracion": "7 días"
            }
        ]
    }
    
    response = client.post("/api/prescriptions/", json=preinscripcion_data)
    
    assert response.status_code == 200
    body = response.json()
    assert body["hasError"] is False
    assert body["message"] == "Preinscripción creada exitosamente"
    assert body["data"]["id_atencion"] == cita.id_cita
    assert body["data"]["tipo"] == 1
    assert len(body["data"]["prescripciones_items"]) == 1


def test_add_preinscripcion_tipo_invalido(client, create_agenda_and_cita, create_medicamento):
    """Test para validar tipo inválido"""
    agenda, cita = create_agenda_and_cita
    medicamento = create_medicamento
    
    preinscripcion_data = {
        "id_atencion": cita.id_cita,
        "tipo": 5,  # Tipo inválido
        "prescripciones_items": [
            {
                "id_medicamento": medicamento.codigo,
                "cantidad": 10,
                "dosis": "500mg",
                "duracion": "7 días"
            }
        ]
    }
    
    response = client.post("/api/prescriptions/", json=preinscripcion_data)
    
    assert response.status_code == 400
    body = response.json()
    assert body["hasError"] is True
    assert "tipo" in body["message"].lower()


def test_add_preinscripcion_id_atencion_invalido(client, create_medicamento):
    """Test para validar id_atencion negativo"""
    medicamento = create_medicamento
    
    preinscripcion_data = {
        "id_atencion": -1,  # ID inválido
        "tipo": 1,
        "prescripciones_items": [
            {
                "id_medicamento": medicamento.codigo,
                "cantidad": 10,
                "dosis": "500mg",
                "duracion": "7 días"
            }
        ]
    }
    
    response = client.post("/api/prescriptions/", json=preinscripcion_data)
    
    assert response.status_code == 400
    body = response.json()
    assert body["hasError"] is True
    assert "id_atencion" in body["message"].lower()


def test_add_preinscripcion_cantidad_invalida(client, create_agenda_and_cita, create_medicamento):
    """Test para validar cantidad negativa en items"""
    agenda, cita = create_agenda_and_cita
    medicamento = create_medicamento
    
    preinscripcion_data = {
        "id_atencion": cita.id_cita,
        "tipo": 1,
        "prescripciones_items": [
            {
                "id_medicamento": medicamento.codigo,
                "cantidad": -5,  # Cantidad inválida
                "dosis": "500mg",
                "duracion": "7 días"
            }
        ]
    }
    
    response = client.post("/api/prescriptions/", json=preinscripcion_data)
    
    assert response.status_code == 400
    body = response.json()
    assert body["hasError"] is True
    assert "cantidad" in body["message"].lower()


def test_add_preinscripcion_dosis_vacia(client, create_agenda_and_cita, create_medicamento):
    """Test para validar dosis vacía"""
    agenda, cita = create_agenda_and_cita
    medicamento = create_medicamento
    
    preinscripcion_data = {
        "id_atencion": cita.id_cita,
        "tipo": 1,
        "prescripciones_items": [
            {
                "id_medicamento": medicamento.codigo,
                "cantidad": 10,
                "dosis": "",  # Dosis vacía
                "duracion": "7 días"
            }
        ]
    }
    
    response = client.post("/api/prescriptions/", json=preinscripcion_data)
    
    assert response.status_code == 400
    body = response.json()
    assert body["hasError"] is True
    assert "dosis" in body["message"].lower()


def test_add_preinscripcion_duracion_vacia(client, create_agenda_and_cita, create_medicamento):
    """Test para validar duración vacía"""
    agenda, cita = create_agenda_and_cita
    medicamento = create_medicamento
    
    preinscripcion_data = {
        "id_atencion": cita.id_cita,
        "tipo": 1,
        "prescripciones_items": [
            {
                "id_medicamento": medicamento.codigo,
                "cantidad": 10,
                "dosis": "500mg",
                "duracion": ""  # Duración vacía
            }
        ]
    }
    
    response = client.post("/api/prescriptions/", json=preinscripcion_data)
    
    assert response.status_code == 400
    body = response.json()
    assert body["hasError"] is True
    assert "duracion" in body["message"].lower()


def test_add_preinscripcion_medicamento_no_existe(client, create_agenda_and_cita):
    """Test para validar que el medicamento existe"""
    agenda, cita = create_agenda_and_cita
    
    preinscripcion_data = {
        "id_atencion": cita.id_cita,
        "tipo": 1,
        "prescripciones_items": [
            {
                "id_medicamento": 99999,  # Medicamento que no existe
                "cantidad": 10,
                "dosis": "500mg",
                "duracion": "7 días"
            }
        ]
    }
    
    response = client.post("/api/prescriptions/", json=preinscripcion_data)
    
    assert response.status_code == 400
    body = response.json()
    assert body["hasError"] is True
    assert "medicamento" in body["message"].lower()


def test_get_preinscripciones_exitoso(client, create_agenda_and_cita, create_medicamento):
    """Test para obtener preinscripciones exitosamente"""
    # Primero creamos una preinscripción
    agenda, cita = create_agenda_and_cita
    medicamento = create_medicamento
    
    preinscripcion_data = {
        "id_atencion": cita.id_cita,
        "tipo": 1,
        "prescripciones_items": [
            {
                "id_medicamento": medicamento.codigo,
                "cantidad": 10,
                "dosis": "500mg",
                "duracion": "7 días"
            }
        ]
    }
    
    client.post("/api/prescriptions/", json=preinscripcion_data)
    
    # Ahora consultamos las preinscripciones
    response = client.get("/api/prescriptions/")
    
    assert response.status_code == 200
    body = response.json()
    assert body["hasError"] is False
    assert body["message"] == "Datos obtenidos exitosamente"
    assert "data" in body
    assert "data" in body["data"]
    assert len(body["data"]["data"]) > 0


def test_get_preinscripciones_por_id(client, create_agenda_and_cita, create_medicamento):
    """Test para obtener preinscripciones por id"""
    agenda, cita = create_agenda_and_cita
    medicamento = create_medicamento
    
    preinscripcion_data = {
        "id_atencion": cita.id_cita,
        "tipo": 1,
        "prescripciones_items": [
            {
                "id_medicamento": medicamento.codigo,
                "cantidad": 10,
                "dosis": "500mg",
                "duracion": "7 días"
            }
        ]
    }
    
    create_response = client.post("/api/prescriptions/", json=preinscripcion_data)
    id_preinscripcion = create_response.json()["data"]["id_preinscripcion"]
    
    # Consultamos por id específico
    response = client.get(f"/api/prescriptions/?idPreinscripcion={id_preinscripcion}")
    
    assert response.status_code == 200
    body = response.json()
    assert body["hasError"] is False
    assert len(body["data"]["data"]) == 1
    assert body["data"]["data"][0]["id_preinscripcion"] == id_preinscripcion


def test_get_preinscripciones_por_id_invalido(client):
    """Test para validar id de preinscripción negativo"""
    response = client.get("/api/prescriptions/?idPreinscripcion=-1")
    
    assert response.status_code == 400
    body = response.json()
    assert body["hasError"] is True
    assert "preinscripción" in body["message"].lower()


def test_get_preinscripciones_por_id_atencion_invalido(client):
    """Test para validar id de atención negativo"""
    response = client.get("/api/prescriptions/?idAtencion=-5")
    
    assert response.status_code == 400
    body = response.json()
    assert body["hasError"] is True
    assert "atención" in body["message"].lower()


def test_get_preinscripciones_tipo_invalido(client):
    """Test para validar tipo inválido en consulta"""
    response = client.get("/api/prescriptions/?tipo=10")
    
    assert response.status_code == 400
    body = response.json()
    assert body["hasError"] is True
    assert "tipo" in body["message"].lower()


def test_get_preinscripciones_vacio(client):
    """Test para obtener preinscripciones cuando no hay datos"""
    response = client.get("/api/prescriptions/?idPreinscripcion=99999")
    
    assert response.status_code == 200
    body = response.json()
    assert body["hasError"] is False
    assert body["data"]["data"] == []
    assert body["data"]["page"] == 1
    assert body["data"]["pages"] == 0