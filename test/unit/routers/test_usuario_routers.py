import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from exceptions import RecursoNoEncontrado, BaseExceptionError

client = TestClient(app)

@pytest.fixture
def usuario_base():
    return {
        "nombre" : "Usuario Nombre",
        "email": "usuario@mail.com",
        "telefono": "+569 89999999" 
    }
    
@pytest.fixture
def usuario_out():
    return {
        "id" : 1,
        "nombre" : "Usuario Nombre",
        "email": "usuario@mail.com",
        "telefono": "+569 89999999" 
    }

@patch("routers.usuario.UsuarioService")
def test_usuario_get_all_sin_usarios(mock_usuario_service):
    mock_usuario_service.get_all.return_value = []
    
    response = client.get("/usuarios/")
    
    assert response.status_code == 200
    assert response.json() == []
    
@patch("routers.usuario.UsuarioService")
def test_usuario_get_all_exito(mock_usuario_service, usuario_out):
    mock_usuario_service.get_all.return_value = [usuario_out]
    
    response = client.get("/usuarios/")
    
    assert response.status_code == 200
    assert response.json()[0]["id"] == usuario_out["id"]
    assert response.json()[0]["nombre"] == usuario_out["nombre"]


@patch("routers.usuario.UsuarioService")
def test_usuario_get_id_sin_usuario(mock_usuario_service):
    mock_usuario_service.get_by_id.side_effect = RecursoNoEncontrado("Usuario no encontrado")
    
    response = client.get("/usuarios/1")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"
    
@patch("routers.usuario.UsuarioService")
def test_usuario_get_id_exito(mock_usuario_service, usuario_out):
    mock_usuario_service.get_by_id.return_value = usuario_out
    
    response = client.get("/usuarios/1")
    
    assert response.status_code == 200
    assert response.json()["id"] == usuario_out["id"]
    assert response.json()["nombre"] == usuario_out["nombre"]
    

@patch("routers.usuario.UsuarioService")
def test_usuario_post_error_creacion(mock_usuario_service, usuario_base):
    mock_usuario_service.create.side_effect = BaseExceptionError("Error al crear usuario")
    
    
    response = client.post("/usuarios/",json=usuario_base)
    
    assert response.status_code == 500
    assert response.json()["detail"] == "Error al crear usuario"
    

@patch("routers.usuario.UsuarioService")
def test_usuario_post_exito(mock_usuario_service, usuario_base, usuario_out):
    mock_usuario_service.create.return_value = usuario_out
    
    
    response = client.post("/usuarios/",json=usuario_base)
    
    assert response.status_code == 201
    assert response.json()["id"] == 1
    

@patch("routers.usuario.UsuarioService")
def test_usuario_put_error_update(mock_usuario_service, usuario_base):
    mock_usuario_service.update.side_effect = RecursoNoEncontrado("Usuario no encontrado")
    

    response = client.put("/usuarios/1",json=usuario_base)
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"
    

@patch("routers.usuario.UsuarioService")
def test_usuario_put_exito(mock_usuario_service, usuario_base, usuario_out):
    mock_usuario_service.update.return_value = usuario_out
    
    
    response = client.put("/usuarios/1",json=usuario_base)
    
    assert response.status_code == 200
    assert response.json()["id"] == 1

@patch("routers.usuario.UsuarioService")
def test_usuario_delete_usuario_no_encontrado(mock_usuario_service):
    mock_usuario_service.delete.side_effect = RecursoNoEncontrado("Usuario no encontrado")
    
    
    response = client.delete("/usuarios/1")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"


@patch("routers.usuario.UsuarioService")
def test_usuario_delete_exito(mock_usuario_service):
    mock_usuario_service.delete.return_value = None
    
    
    response = client.delete("/usuarios/1")
    
    assert response.status_code == 204
    assert response.content == b""


@patch("routers.usuario.UsuarioService")
def test_usuario_patch_usuario_no_encontrado(mock_usuario_service, usuario_base):
    mock_usuario_service.patch.side_effect = RecursoNoEncontrado("Usuario no encontrado")
    

    response = client.patch("/usuarios/1",json=usuario_base)
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"
    

@patch("routers.usuario.UsuarioService")
def test_usuario_patch_exito(mock_usuario_service, usuario_base, usuario_out):
    mock_usuario_service.patch.return_value = usuario_out
    
    response = client.patch("/usuarios/1",json=usuario_base)
    
    assert response.status_code == 200
    assert response.json()["id"] == 1


@patch("routers.usuario.PlanService")
def test_usuario_get_all_planes(mock_plan_service):
    mock_plan_service.get_by_userid.return_value = []
    
    response = client.get("/usuarios/1/planes")
    
    assert response.status_code == 200
    assert response.json() == []


@patch("routers.usuario.ReservaService")
def test_usuario_get_all_reservas(mock_reserva_service):
    mock_reserva_service.get_all_by_user_id.return_value = []
    
    response = client.get("/usuarios/1/reservas")
    
    assert response.status_code == 200
    assert response.json() == []
        
