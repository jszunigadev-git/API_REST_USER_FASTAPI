import pytest
from repository import trainerRepository

@pytest.fixture
def entrenador_dict():
    return {
        "nombre": "Entreandor Test",
        "email": "entreandortest@mail.com",
        "telefono": "+569 89655644",
    }
    
def test_crear_y_obtener_entreandor(entrenador_dict):
      
    entrenador = trainerRepository.crear_entrenador(entrenador_dict)
    
    assert entrenador is not None
    
    id_entrenador = entrenador["id"]
    
    try:
        entrenador_encontrado = trainerRepository.obtener_entrenador(id_entrenador)
        
        assert isinstance(entrenador_encontrado, dict)
        assert entrenador_encontrado["nombre"] == "Entreandor Test"
        assert entrenador_encontrado["email"] == "entreandortest@mail.com"
        assert entrenador_encontrado["telefono"] == "+569 89655644"
    finally:
        trainerRepository.eliminar_entrenador(id_entrenador)
    


def test_actualizar_entrenador(entrenador_dict):
    
    entrenador = trainerRepository.crear_entrenador(entrenador_dict)
    
    assert entrenador is not None
    
    id_entrenador = entrenador["id"]
    
    trainer_update_dict = {
        "id" : id_entrenador,
        "nombre": "Entreandor Test update",
        "email": "entrenador@mail.com",
        "telefono": "+569 89655633",
    }
    try:
        trainer_update = trainerRepository.actualizar_entrenador(trainer_update_dict)
        
        assert trainer_update is True
        
        resultado = trainerRepository.obtener_entrenador(id_entrenador)
        assert resultado["nombre"] == "Entreandor Test update"
        assert resultado["email"] == "entrenador@mail.com"
    finally:
        trainerRepository.eliminar_entrenador(id_entrenador)


def test_eliminar_entrenador(entrenador_dict):
    
    entrenador = trainerRepository.crear_entrenador(entrenador_dict)
    
    assert entrenador is not None
    
    id_entrenador = entrenador["id"]
    
    entrenador_delete = trainerRepository.eliminar_entrenador(id_entrenador)
    assert entrenador_delete is True
    
