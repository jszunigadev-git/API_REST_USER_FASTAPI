import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from datetime import datetime
from exceptions import RecursoNoEncontrado, BaseExceptionError

client = TestClient(app)

fecha = "2026-07-29T18:00:00"

@pytest.fixture
def clase_in():
    return {
    'tipo_clase_id' : 1,
    'sucursal_id' : 1,
    'entrenador_id' : 1,
    'fecha_hora': fecha,
    'capacidad' : 10,
    'duracion_minutos' : 60
    }
       
    
@pytest.fixture
def clase_out():
    return {
    'id' : 1,
    'tipo_clase' : 'str',
    'sucursal' : 'str',
    'entrenador' : 'str',
    'fecha_hora': fecha,
    'capacidad' : 10,
    'duracion_minutos' : 60
    }

@patch("routers.clases.ClasesService")
def test_clases_get_all_sin_clases(mock_clases_service):
    mock_clases_service.get_all.return_value = []
    
    response = client.get("/clases/")
    
    assert response.status_code == 200
    assert response.json() == []
    
@patch("routers.clases.ClasesService")
def test_clases_get_all_exito(mock_clases_service,clase_out):
    mock_clases_service.get_all.return_value = [clase_out]
    
    response = client.get("/clases/")
    
    assert response.status_code == 200
    assert response.json()[0]["id"] == clase_out["id"]
    assert response.json()[0]["capacidad"] == clase_out["capacidad"]


@patch("routers.clases.ClasesService")
def test_clases_get_id_sin_clases(mock_clases_service):
    mock_clases_service.get_by_id.side_effect = RecursoNoEncontrado("Clase no encontrada")
    
    response = client.get("/clases/1")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Clase no encontrada"
    
@patch("routers.clases.ClasesService")
def test_clases_get_id_exito(mock_clases_service,clase_out):
    mock_clases_service.get_by_id.return_value = clase_out
    
    response = client.get("/clases/1")
    
    assert response.status_code == 200
    assert response.json()["id"] == clase_out["id"]
    assert response.json()["capacidad"] == clase_out["capacidad"]
    

@patch("routers.clases.ClasesService")
def test_clases_post_error_creacion(mock_clases_service, clase_in):
    mock_clases_service.create.side_effect = BaseExceptionError("No fue posible crear la clase")
    
    
    response = client.post("/clases/",json=clase_in)
    
    assert response.status_code == 500
    assert response.json()["detail"] == "No fue posible crear la clase"
    

@patch("routers.clases.ClasesService")
def test_clases_post_exito(mock_clases_service, clase_in, clase_out):
    mock_clases_service.create.return_value = clase_out
    
    
    response = client.post("/clases/",json=clase_in)
    
    assert response.status_code == 201
    assert response.json()["id"] == 1
    

@patch("routers.clases.ClasesService")
def test_clases_put_error_update(mock_clases_service, clase_in, clase_out):
    mock_clases_service.update.side_effect = RecursoNoEncontrado("Clase no encontrada para actualizar")
    
    
    response = client.put("/clases/1",json=clase_in)
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Clase no encontrada para actualizar"
    

@patch("routers.clases.ClasesService")
def test_clases_put_exito(mock_clases_service, clase_in, clase_out):
    mock_clases_service.update.return_value = clase_out
    
    
    response = client.put("/clases/1",json=clase_in)
    
    assert response.status_code == 200
    assert response.json()["id"] == 1

@patch("routers.clases.ClasesService")
def test_clases_delete_clase_no_encontrada(mock_clases_service):
    mock_clases_service.delete.side_effect = RecursoNoEncontrado("Clase no encontrada para eliminar")
    
    
    response = client.delete("/clases/1")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Clase no encontrada para eliminar"


@patch("routers.clases.ClasesService")
def test_clases_delete_exito(mock_clases_service):
    mock_clases_service.delete.return_value = None
    
    
    response = client.delete("/clases/1")
    
    assert response.status_code == 204
    assert response.content == b""
     