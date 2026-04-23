def test_get_referrals_exitoso(client, create_remision):
    response = client.get("/api/referrals")

    assert response.status_code == 200
    body = response.json()
    assert body["hasError"] is False
    assert body["message"] == "Remisiones obtenidas exitosamente"
    assert isinstance(body["data"], list)
    assert len(body["data"]) >= 1


def test_get_referrals_by_patient_id_exitoso(client, create_remision):
    response = client.get("/api/referrals/patients/123456789")

    assert response.status_code == 200
    body = response.json()
    assert body["hasError"] is False
    assert body["message"] == "Remisiones del paciente obtenidas exitosamente"
    assert isinstance(body["data"], list)
    assert len(body["data"]) >= 1
    assert body["data"][0]["id_paciente"] == 123456789