
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from exceptions import RecursoNoEncontrado

client = TestClient(app)
 
@pytest.fixture
def tipo_clases_out():
    return {
        'id' : 1,
        'nombre' : "str"
    }

@patch("routers.tipo_clases.TipoClasesService")
def test_tipo_clases_get_all_sin_tipos(mock_tipo_clases_service):
    mock_tipo_clases_service.get_all.return_value = []
    
    response = client.get("/tipo-clases/")
    
    assert response.status_code == 200
    assert response.json() == []
    
@patch("routers.tipo_clases.TipoClasesService")
def test_tipo_clases_get_all_exito(mock_tipo_clases_service,tipo_clases_out):
    mock_tipo_clases_service.get_all.return_value = [tipo_clases_out]
    
    response = client.get("/tipo-clases/")
    
    assert response.status_code == 200
    assert response.json()[0]["id"] == tipo_clases_out["id"]
    assert response.json()[0]["nombre"] == tipo_clases_out["nombre"]


@patch("routers.tipo_clases.TipoClasesService")
def test_tipo_clases_get_id_sin_tipo(mock_tipo_clases_service):
    mock_tipo_clases_service.get_by_id.side_effect = RecursoNoEncontrado("Tipo de clase no encontrada")
    
    response = client.get("/tipo-clases/1")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Tipo de clase no encontrada"
    
@patch("routers.tipo_clases.TipoClasesService")
def test_tipo_clases_get_id_exito(mock_tipo_clases_service,tipo_clases_out):
    mock_tipo_clases_service.get_by_id.return_value = tipo_clases_out
    
    response = client.get("/tipo-clases/1")
    
    assert response.status_code == 200
    assert response.json()["id"] == tipo_clases_out["id"]
    assert response.json()["nombre"] == tipo_clases_out["nombre"]
    

@patch("routers.tipo_clases.TipoClasesService")
def test_tipo_clases_get_all_clases(mock_tipo_clases_service):
    mock_tipo_clases_service.get_clases_by_tipo_clase.return_value = []
    
    response = client.get("/tipo-clases/1/clases")
    
    assert response.status_code == 200
    assert response.json() == []
    
    
