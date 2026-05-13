import pytest
from models.Cita import Cita
from services.CitaService import CitatService
from services.repositories.CitaRepository import CitaRepository
from services.repositories.RegistroRepository import RegistroRepository
from services.repositories.HistoriaRepository import HistoriaRepository
from services.repositories.CatalogoDiagnosticoRepository import CatalogoDiagnosticoRepository
from services.repositories.MedicamentoRepository import MedicamentoRepository
from services.repositories.PrescripcionesRepository import PrescripcionesRepository
from services.repositories.PrescripcionesItemsRepository import PrescripcionesItemsRepository
from services.repositories.RemisionesRepository import RemisionesRepository
from services.repositories.EspecialidadRepository import EspecialidadRepository
from services.repositories.PersonaRepository import PersonaRepository


def test_get_consultation_context_cita_no_existe(client):
    response = client.get("/api/appoinment/99999/consultation-context")

    assert response.status_code == 404
    body = response.json()
    assert body["hasError"] is True
    assert body["message"] == "La cita no existe"
    assert body["data"] is None


def test_get_consultation_context_exitoso(client,create_agenda_and_cita):
    agenda, cita = create_agenda_and_cita

    response = client.get(f"/api/appoinment/{cita.id_cita}/consultation-context")
    print(response.json())
    assert response.status_code == 200
    body = response.json()
    assert body["hasError"] is False
    assert body["message"] == "Cita obtenida exitosamente"
    assert body["data"]["id_cita"] == cita.id_cita
    assert body["data"]["id_paciente"] == cita.id_paciente
    assert body["data"]["id_especialidad"] == agenda.id_especialidad


def test_get_consultation_context_conflict_registro_existente(client, create_registro_historia):
    registro = create_registro_historia



    response = client.get(f"/api/appoinment/{registro.id_cita}/consultation-context")

    assert response.status_code == 409
    body = response.json()
    assert body["hasError"] is True
    assert body["message"] == "La cita ya tiene un registro asociado"
    assert body["data"] is None


def test_create_consultation_cita_no_existe(client):
    registro_data = {
        "obervacion": "Paciente presenta síntomas de gripe",
        "tratamiento": "Reposo y medicamentos",
        "id_diagnostico": 1,
        "tipo_preinscripcion": 1,
        "medicamentos": [
            {
                "codigo": 1,
                "dosis": "500mg",
                "duracion": 7,
                "cantidad": 14
            }
        ]
    }
    
    response = client.post("/api/appoinment/99999/consultation", json=registro_data)

    assert response.status_code == 404
    body = response.json()
    assert body["hasError"] is True
    assert body["message"] == "La cita no existe"
    assert body["data"] is None


def test_create_consultation_exitoso(client, create_agenda_and_cita, create_medicamento, create_diagnostico, db_session):
    agenda, cita = create_agenda_and_cita
    medicamento= create_medicamento
    diagnostico = create_diagnostico
    registro_data = {
        "obervacion": "Paciente presenta síntomas de gripe",
        "tratamiento": "Reposo y medicamentos",
        "id_diagnostico": 1,
        "tipo_preinscripcion": 1,
        "medicamentos": [
            {
                "codigo": 1,
                "dosis": "500mg",
                "duracion": 7,
                "cantidad": 14
            }
        ]
    }

    response = client.post(f"/api/appoinment/{cita.id_cita}/consultation", json=registro_data)
    assert response.status_code == 201
    body = response.json()
    assert body["hasError"] is False
    assert body["message"] == "Registro de historia creado exitosamente"
    assert body["data"] is not None
    assert body["data"]["id_cita"] == cita.id_cita

    cita_actualizada = db_session.query(Cita).filter(Cita.id_cita == cita.id_cita).first()
    assert cita_actualizada is not None
    assert cita_actualizada.asistio is True


def test_create_consultation_conflict_registro_existente(client, create_registro_historia):
    registro = create_registro_historia
    registro_data = {
        "obervacion": "Paciente presenta síntomas de gripe",
        "tratamiento": "Reposo y medicamentos",
        "id_diagnostico": 1,
        "tipo_preinscripcion": 1,
        "medicamentos": [
            {
                "codigo": 1,
                "dosis": "500mg",
                "duracion": 7,
                "cantidad": 14
            }
        ]
    }

    response = client.post(f"/api/appoinment/{registro.id_cita}/consultation", json=registro_data)

    assert response.status_code == 409
    body = response.json()
    assert body["hasError"] is True
    assert body["message"] == "La cita ya tiene un registro asociado"
    assert body["data"] is None

def test_create_remision_cita_no_existe(client):
    registro_data = {
        "id_registro":1,
        "id_especialidad": 1,
        "fecha_expiracion": "2030-01-01"
    }
    
    response = client.post("/api/appoinment/99999/remision", json=registro_data)

    assert response.status_code == 404
    body = response.json()
    assert body["hasError"] is True
    assert body["message"] == "La cita no existe"
    assert body["data"] is None

def test_create_remision_especialidad_no_existe(client,create_agenda_and_cita):
    agenda, cita = create_agenda_and_cita
    registro_data = {
        "id_registro": 1,
        "id_especialidad": 99999,
        "fecha_expiracion": "2030-01-01"
    }
    
    response = client.post("/api/appoinment/1/remision", json=registro_data)

    assert response.status_code == 422
    body = response.json()
    assert body["hasError"] is True
    assert body["message"] == "La especialidad no existe"
    assert body["data"] is None
def test_create_remision_fecha_invalida(client,create_agenda_and_cita,create_especialidad):
    agenda, cita = create_agenda_and_cita
    registro_data = {
        "id_registro": 1,
        "id_especialidad": 1,
        "fecha_expiracion": "2020-01-01"
    }
    
    response = client.post("/api/appoinment/1/remision", json=registro_data)

    assert response.status_code == 422
    body = response.json()
    assert body["hasError"] is True
    assert body["message"] == "La fecha de expiración debe ser una fecha futura"
    assert body["data"] is None

def test_create_remision_registro_invalido(client,create_agenda_and_cita):
    agenda, cita = create_agenda_and_cita   
    registro_data = {
        "id_registro": 99999,
        "id_especialidad": 1,
        "fecha_expiracion": "2030-01-01"
    }
    
    response = client.post("/api/appoinment/1/remision", json=registro_data)

    assert response.status_code == 403
    body = response.json()
    assert body["hasError"] is True
    assert body["message"] == "El id_registro no pertenece a la cita"
    assert body["data"] is None
def test_create_remision_valido(client,create_agenda_and_cita):
    agenda, cita = create_agenda_and_cita   
    registro_data = {
        "id_registro": 1,
        "id_especialidad": 1,
        "fecha_expiracion": "2030-01-01"
    }
    
    response = client.post("/api/appoinment/1/remision", json=registro_data)

    assert response.status_code == 201
    body = response.json()
    assert body["hasError"] is False
    assert body["message"] == "Remisión creada exitosamente"
    assert body["data"] is not None    

def test_procesar_inasistencias_marca_cita_vencida(create_agenda_and_cita_vencida, db_session):
    agenda, cita = create_agenda_and_cita_vencida

    service = CitatService(
        CitaRepository(db_session),
        RegistroRepository(db_session),
        HistoriaRepository(db_session),
        CatalogoDiagnosticoRepository(db_session),
        MedicamentoRepository(db_session),
        PrescripcionesRepository(db_session),
        PrescripcionesItemsRepository(db_session),
        RemisionesRepository(db_session),
        EspecialidadRepository(db_session),
        PersonaRepository(db_session),
    )

    response = service.procesar_inasistencias()

    cita_actualizada = db_session.query(Cita).filter(Cita.id_cita == cita.id_cita).first()

    assert response.hasError is False
    assert response.data["citas_procesadas"] >= 1
    assert cita_actualizada is not None
    assert cita_actualizada.asistio is False
