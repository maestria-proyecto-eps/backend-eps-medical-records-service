def test_get_medicalHistory_valido(client,create_historia_and_catalogo):

    response = client.get("/api/pattient/1/medical-history")

    assert response.status_code == 200
    body = response.json()
    assert body["hasError"] is False
    assert body["message"] == "Historias clínicas obtenidas exitosamente"
    assert body["data"] is not None

def test_get_medicalHistory_invalido(client):

    response = client.get(f"/api/pattient/999/medical-history")

    assert response.status_code == 404
    body = response.json()
    assert body["hasError"] is True
    assert body["message"] == "No hay historia clínica para el paciente"
    assert body["data"] is None
    