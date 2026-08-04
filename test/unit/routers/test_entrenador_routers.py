import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from exceptions import RecursoNoEncontrado, BaseExceptionError

client = TestClient(app)


@pytest.fixture
def entrenador_base():
    return {
        "nombre" : "Entrenador Nombre",
        "email": "entrenador@mail.com",
        "telefono": "+569 89999999" 
    }
    
@pytest.fixture
def entrenador_out():
    return {
        "id" : 1,
        "nombre" : "Entrenador Nombre",
        "email": "entrenador@mail.com",
        "telefono": "+569 89999999" 
    }

@patch("routers.entrenador.TrainerService")
def test_trainer_get_all_sin_trainer(mock_trainer_service):
    mock_trainer_service.get_all.return_value = []
    
    response = client.get("/entrenador/")
    
    assert response.status_code == 200
    assert response.json() == []
    
@patch("routers.entrenador.TrainerService")
def test_trainer_get_all_exito(mock_trainer_service,entrenador_out):
    mock_trainer_service.get_all.return_value = [entrenador_out]
    
    response = client.get("/entrenador/")
    
    assert response.status_code == 200
    assert response.json()[0]["id"] == entrenador_out["id"]
    assert response.json()[0]["nombre"] == entrenador_out["nombre"]


@patch("routers.entrenador.TrainerService")
def test_trainer_get_id_sin_entrenador(mock_trainer_service):
    mock_trainer_service.get_by_id.side_effect = RecursoNoEncontrado("Entrenador no encontrado")
    
    response = client.get("/entrenador/1")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Entrenador no encontrado"
    
@patch("routers.entrenador.TrainerService")
def test_trainer_get_id_exito(mock_trainer_service,entrenador_out):
    mock_trainer_service.get_by_id.return_value = entrenador_out
    
    response = client.get("/entrenador/1")
    
    assert response.status_code == 200
    assert response.json()["id"] == entrenador_out["id"]
    assert response.json()["nombre"] == entrenador_out["nombre"]
    

@patch("routers.entrenador.TrainerService")
def test_trainer_post_error_creacion(mock_trainer_service, entrenador_base):
    mock_trainer_service.create.side_effect = BaseExceptionError("No fue posible crear al entrenador")
    
    
    response = client.post("/entrenador/",json=entrenador_base)
    
    assert response.status_code == 500
    assert response.json()["detail"] == "No fue posible crear al entrenador"
    

@patch("routers.entrenador.TrainerService")
def test_trainer_post_exito(mock_trainer_service, entrenador_base, entrenador_out):
    mock_trainer_service.create.return_value = entrenador_out
    
    
    response = client.post("/entrenador/",json=entrenador_base)
    
    assert response.status_code == 201
    assert response.json()["id"] == 1
    

@patch("routers.entrenador.TrainerService")
def test_trainer_put_error_update(mock_trainer_service, entrenador_base):
    mock_trainer_service.update.side_effect = RecursoNoEncontrado("Entrenador no encontrado")
    
    
    response = client.put("/entrenador/1",json=entrenador_base)
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Entrenador no encontrado"
    

@patch("routers.entrenador.TrainerService")
def test_trainer_put_exito(mock_trainer_service, entrenador_base, entrenador_out):
    mock_trainer_service.update.return_value = entrenador_out
    
    
    response = client.put("/entrenador/1",json=entrenador_base)
    
    assert response.status_code == 200
    assert response.json()["id"] == 1

@patch("routers.entrenador.TrainerService")
def test_trainer_delete_trainer_no_encontrado(mock_trainer_service):
    mock_trainer_service.delete.side_effect = RecursoNoEncontrado("Entrenador no encontrado")
    
    
    response = client.delete("/entrenador/1")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Entrenador no encontrado"


@patch("routers.entrenador.TrainerService")
def test_trainer_delete_exito(mock_trainer_service):
    mock_trainer_service.delete.return_value = None
    
    
    response = client.delete("/entrenador/1")
    
    assert response.status_code == 204
    assert response.content == b""
     
@patch("routers.entrenador.TrainerService")
def test_tariner_get_all_clases(mock_trainer_service):
    mock_trainer_service.get_clases_by_entrenador.return_value = []
    
    response = client.get("/entrenador/1/clases")
    
    assert response.status_code == 200
    assert response.json() == []
         
