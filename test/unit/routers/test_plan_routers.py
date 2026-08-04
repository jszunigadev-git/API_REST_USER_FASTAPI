from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from exceptions import RecursoNoEncontrado,RecursoConflictoDependencia
import pytest

client = TestClient(app)

@pytest.fixture
def plan_dict_valido():
    return {
        "id": 1,
        "nombre_usuario": "Juan Pérez",
        "email_usuario": "juan@test.com",
        "membresia": "Mensual",
        "fecha_inicio": "2026-09-01",
        "fecha_fin": "2026-09-30",
        "estado": "activo"
    }


@patch("routers.planes.PlanService")
def test_get_all_exito(mock_plan_service, plan_dict_valido):
    mock_plan_service.get_all.return_value = [plan_dict_valido]
    
    response = client.get("/planes/")
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1

    

@patch("routers.planes.PlanService") 
def test_get_by_id_no_encontrado(mock_plan_service):
    mock_plan_service.get_by_id.side_effect = RecursoNoEncontrado("Plan no encontrado") 

    response = client.get("/planes/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Plan no encontrado"
    
    
@patch("routers.planes.PlanService")
def test_get_by_id_exito(mock_plan_service, plan_dict_valido):
    mock_plan_service.get_by_id.return_value = plan_dict_valido

    response = client.get("/planes/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["estado"] == "activo"
    

@patch("routers.planes.PlanService")
def test_post_crear_plan_exitoso(mock_plan_service, plan_dict_valido):
    mock_plan_service.create.return_value = plan_dict_valido

    body = {
        "usuario_id": 1,
        "membresia_id": 2,
        "fecha_inicio": "2026-09-01"
    }

    response = client.post("/planes/", json=body)

    assert response.status_code == 201
    assert response.json()["id"] == 1
    
    

def test_post_crear_plan_fecha_pasada_falla_validacion():
    body = {
        "usuario_id": 1,
        "membresia_id": 2,
        "fecha_inicio": "2020-01-01"
    }

    response = client.post("/planes/", json=body)

    assert response.status_code == 422
    
    
@patch("routers.planes.PlanService")
def test_post_crear_plan_fecha_solapada(mock_plan_service):
    mock_plan_service.create.side_effect = RecursoConflictoDependencia(
        "La fecha ingresada para el servicio choca con un plan activo."
    )

    body = {
        "usuario_id": 1,
        "membresia_id": 2,
        "fecha_inicio": "2026-09-01"
    }

    response = client.post("/planes/", json=body)

    assert response.status_code == 400
    assert response.json()["detail"] == "La fecha ingresada para el servicio choca con un plan activo."
    
    
@patch("routers.planes.PlanService")
def test_patch_cancelar_plan_exitoso(mock_plan_service):
    mock_plan_service.cancelar.return_value = True

    response = client.patch("/planes/1/cancelar")

    assert response.status_code == 204
    assert response.content == b""  # 204 no debe traer body