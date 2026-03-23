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


def test_create_consultation_exitoso(client, create_agenda_and_cita,create_medicamento, create_diagnostico):
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
