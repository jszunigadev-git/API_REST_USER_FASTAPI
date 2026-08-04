
from unittest.mock import patch
import pytest
from exceptions import RecursoNoEncontrado,BaseExceptionError
from services import TrainerService
from schemas import EntrenadorBase, Entrenador


@pytest.fixture
def entrenador_base():
    return {
        "nombre" : "Entrenador Nombre",
        "email": "entrenador@mail.com",
        "telefono": "+569 89999999" 
    }


    
@patch("services.entrenador_service.trainerRepository")
def test_get_entrenador_no_encontrado(mock_trainer_repository):
    mock_trainer_repository.obtener_entrenador.return_value = None
    
    with pytest.raises(RecursoNoEncontrado, match="Entrenador no encontrado"):
        TrainerService.get_by_id(1)
        
@patch("services.entrenador_service.trainerRepository")
def test_get_by_id_exito(mock_trainer_repository):
    mock_trainer_repository.obtener_entrenador.return_value = {"id":1}
    
    resultado = TrainerService.get_by_id(1)
    
    assert resultado == {"id":1}
    mock_trainer_repository.obtener_entrenador.assert_called_once_with(1)
    
    

@patch("services.entrenador_service.trainerRepository")
def test_create_error(mock_trainer_repository, entrenador_base):
    mock_trainer_repository.crear_entrenador.return_value = None
    
    entrenador_data = EntrenadorBase(**entrenador_base)
    with pytest.raises(BaseExceptionError, match="No fue posible crear al entrenador"):
        TrainerService.create(entrenador_data)
    

@patch("services.entrenador_service.trainerRepository")
def test_create_entrenador_exito(mock_trainer_repository, entrenador_base):
    mock_trainer_repository.crear_entrenador.return_value = {"id":1}
    
    entrenador_data = EntrenadorBase(**entrenador_base)

    resultado = TrainerService.create(entrenador_data)
    
    entrenador_request_esperado = entrenador_data.model_dump()
    entrenador_request_esperado["id"] = 1
    
    entrenador_esperado = Entrenador(**entrenador_request_esperado)
    
    assert resultado == entrenador_esperado
    
    mock_trainer_repository.crear_entrenador.assert_called_once_with(entrenador_data.model_dump())
    
    
    
@patch("services.entrenador_service.trainerRepository")
def test_update_error(mock_trainer_repository, entrenador_base):
    mock_trainer_repository.actualizar_entrenador.return_value = False
    
    entrenador_data = EntrenadorBase(**entrenador_base)
    with pytest.raises(RecursoNoEncontrado, match="Entrenador no encontrado"):
        TrainerService.update(1,entrenador_data)   


@patch("services.entrenador_service.trainerRepository")
def test_update_entrenador_exito(mock_trainer_repository, entrenador_base):
    mock_trainer_repository.actualizar_entrenador.return_value = True
    
    entrenador_data = EntrenadorBase(**entrenador_base)

    resultado = TrainerService.update(1,entrenador_data)
    
    entrenador_update = entrenador_data.model_dump()
    entrenador_update["id"] = 1

    assert resultado == entrenador_update

    mock_trainer_repository.actualizar_entrenador.assert_called_once_with(entrenador_update)
    


@patch("services.entrenador_service.trainerRepository")
def test_delete_error(mock_trainer_repository):
    mock_trainer_repository.eliminar_entrenador.return_value = None
    
    with pytest.raises(RecursoNoEncontrado, match="Entrenador no encontrado"):
        TrainerService.delete(1)
        
@patch("services.entrenador_service.trainerRepository")
def test_delete_exito(mock_trainer_repository):
    mock_trainer_repository.eliminar_entrenador.return_value = True
    
    resultado = TrainerService.delete(1)
    
    assert resultado is None
    mock_trainer_repository.eliminar_entrenador.assert_called_once_with(1)    
