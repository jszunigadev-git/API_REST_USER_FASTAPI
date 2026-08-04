import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from exceptions import RecursoNoEncontrado

client = TestClient(app)
 
@pytest.fixture
def membresia_out():
    return {
        'id' : 1,
        'nombre' : "str",
        'precio' : 35000,
        'duracion_meses' : 1
    }

@patch("routers.membresias.MembresiaService")
def test_membresia_get_all_sin_membresias(mock_membresia_service):
    mock_membresia_service.get_all.return_value = []
    
    response = client.get("/membresias/")
    
    assert response.status_code == 200
    assert response.json() == []
    
@patch("routers.membresias.MembresiaService")
def test_membresia_get_all_exito(mock_membresia_service,membresia_out):
    mock_membresia_service.get_all.return_value = [membresia_out]
    
    response = client.get("/membresias/")
    
    assert response.status_code == 200
    assert response.json()[0]["id"] == membresia_out["id"]
    assert response.json()[0]["duracion_meses"] == membresia_out["duracion_meses"]


@patch("routers.membresias.MembresiaService")
def test_membresia_get_id_sin_membresia(mock_membresia_service):
    mock_membresia_service.get_by_id.side_effect = RecursoNoEncontrado("Membresia no encontrada")
    
    response = client.get("/membresias/1")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Membresia no encontrada"
    
@patch("routers.membresias.MembresiaService")
def test_membresia_get_id_exito(mock_membresia_service,membresia_out):
    mock_membresia_service.get_by_id.return_value = membresia_out
    
    response = client.get("/membresias/1")
    
    assert response.status_code == 200
    assert response.json()["id"] == membresia_out["id"]
    assert response.json()["duracion_meses"] == membresia_out["duracion_meses"]
    
