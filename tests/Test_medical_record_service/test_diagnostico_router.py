def test_get_diagnosticos_valido(client,create_diagnostico):
    diagnostico = create_diagnostico

    response = client.get("/api/diagnosticos/search?id=1")

    assert response.status_code == 200
    body = response.json()
    assert body["hasError"] is False
    assert body["message"] == "Diagnóstico obtenido exitosamente"
    assert body["data"] is not None

def test_get_diagnosticos_invalido(client):

    response = client.get(f"/api/diagnosticos/search?nombre=q")

    assert response.status_code == 400
    body = response.json()
    assert body["hasError"] is True
    assert body["message"] == "El nombre debe tener al menos 2 caracteres"
    assert body["data"] is None
    
    