from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from exceptions import RecursoNoEncontrado,RecursoConflictoDependencia
from datetime import datetime
import pytest


client = TestClient(app)

@pytest.fixture
def reserva_dict_valida():
    fecha_reserva = datetime.now()
    reserva_out = {
        "id" : 1,
        "estado": "confirmado",
        "clase": "yoga",
        "usuario": "Julio Diaz",
        "fecha_reserva": fecha_reserva
    }
    
    return reserva_out


@patch("routers.reserva.ReservaService")
def test_get_all_exito(reserva_service, reserva_dict_valida):
    reserva_service.get_all.return_value = [reserva_dict_valida]
    
    response = client.get("/reservas/")
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1


@patch("routers.reserva.ReservaService")
def test_reservas_by_id_sin_reserva(reserva_service):
    reserva_service.get_all_by_id.side_effect = RecursoNoEncontrado("Reserva no encontrada")
    
    response = client.get("/reservas/999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Reserva no encontrada"


@patch("routers.reserva.ReservaService")
def test_reservas_by_id_exito(reserva_service,reserva_dict_valida):
    reserva_service.get_all_by_id.return_value = reserva_dict_valida
    
    response = client.get("/reservas/1")
    
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["estado"] == "confirmado"
    
 
 
@pytest.mark.parametrize("excepcion,mensaje,status_code",[
    (RecursoNoEncontrado,"Usuario no encontrado",404),
    (RecursoConflictoDependencia,"Usuario no cuenta con plan activo, no es posible reservar",400),
    (RecursoConflictoDependencia,"No quedan cupos para la clase",400)
])
@patch("routers.reserva.ReservaService")
def test_create_reserva_error_exeption(reserva_service,excepcion,mensaje,status_code):
    reserva_service.crear_reserva.side_effect = excepcion(mensaje)
    
    request = {
         "usuario_id": 999,
        "clase_id": 999 
    }
    
    response = client.post("/reservas/",json=request)
    
    assert response.status_code == status_code
    assert response.json()["detail"] == mensaje
    

    
@patch("routers.reserva.ReservaService")
def test_create_reserva_exito(reserva_service,reserva_dict_valida):
    reserva_service.crear_reserva.return_value =  reserva_dict_valida
    
    request = {
        "usuario_id": 1,
        "clase_id": 1 
    }
   
    response = client.post("/reservas/",json=request)
    
    assert response.status_code == 201
    assert response.json()["id"] == 1
    
    
@patch("routers.reserva.ReservaService")
def test_cancelar_reserva_exito(reserva_service):
    reserva_service.cancelar_reserva.return_value = True
    
    response = client.patch("/reservas/999/cancelar")
    
    assert response.status_code == 204
    assert response.content == b""