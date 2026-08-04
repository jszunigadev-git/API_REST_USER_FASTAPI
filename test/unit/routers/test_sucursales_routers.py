import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from exceptions import RecursoNoEncontrado

client = TestClient(app)
 
@pytest.fixture
def sucursal_out():
    return {
        'id' : 1,
        'nombre' : "str"
    }

@patch("routers.sucursales.SucursalService")
def test_sucursales_get_all_sin_sucursales(mock_sucursal_service):
    mock_sucursal_service.get_all.return_value = []
    
    response = client.get("/sucursales/")
    
    assert response.status_code == 200
    assert response.json() == []
    
@patch("routers.sucursales.SucursalService")
def test_sucursales_get_all_exito(mock_sucursal_service,sucursal_out):
    mock_sucursal_service.get_all.return_value = [sucursal_out]
    
    response = client.get("/sucursales/")
    
    assert response.status_code == 200
    assert response.json()[0]["id"] == sucursal_out["id"]
    assert response.json()[0]["nombre"] == sucursal_out["nombre"]


@patch("routers.sucursales.SucursalService")
def test_sucursales_get_id_sin_sucursal(mock_sucursal_service):
    mock_sucursal_service.get_by_id.side_effect = RecursoNoEncontrado("Sucursal no encontrada")
    
    response = client.get("/sucursales/1")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Sucursal no encontrada"
    
@patch("routers.sucursales.SucursalService")
def test_sucursales_get_id_exito(mock_sucursal_service,sucursal_out):
    mock_sucursal_service.get_by_id.return_value = sucursal_out
    
    response = client.get("/sucursales/1")
    
    assert response.status_code == 200
    assert response.json()["id"] == sucursal_out["id"]
    assert response.json()["nombre"] == sucursal_out["nombre"]
    

@patch("routers.sucursales.SucursalService")
def test_sucursal_get_all_clases(mock_sucursal_service):
    mock_sucursal_service.get_clases_by_sucursal.return_value = []
    
    response = client.get("/sucursales/1/clases")
    
    assert response.status_code == 200
    assert response.json() == []
