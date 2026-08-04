
import pytest
from unittest.mock import patch
from services import ClasesService
from exceptions import RecursoNoEncontrado,BaseExceptionError
from schemas import ClaseCreate,ClaseUpdate
from datetime import datetime



@pytest.fixture
def clase_out_dict():
    fecha = datetime(2026, 7, 29, 18, 0)
    return {
        "id" : 1,
        "tipo_clase" : "str",
        "sucursal" : "str",
        "entrenador" : "str",
        "fecha_hora": fecha,
        "capacidad" : 10,
        "duracion_minutos" : 90
    }
    
@pytest.fixture
def clase_in_dict():
    fecha = datetime(2026, 7, 29, 18, 0)
    return {
        "tipo_clase_id" : 1,
        "sucursal_id" : 1,
        "entrenador_id" : 1,
        "fecha_hora": fecha,
        "capacidad" : 10,
        "duracion_minutos" : 90
    }
    
@pytest.fixture
def clase_update_dict():
    fecha = datetime(2026, 7, 29, 18, 0)
    return {
        "tipo_clase_id" : 1,
        "sucursal_id" : 1,
        "entrenador_id" : 1,
        "fecha_hora": fecha,
        "capacidad" : 10,
        "duracion_minutos" : 90
    }  

@patch("services.clases_service.ClaseRepository")
def test_clases_get_by_id_sin_clase(mock_clase_repository):
    mock_clase_repository.obtener_clase.return_value = None
    
    with pytest.raises(RecursoNoEncontrado, match="Clase no encontrada"):
        ClasesService.get_by_id(1)
        
@patch("services.clases_service.ClaseRepository")
def test_clases_get_by_id_exito(mock_clase_repository):
    mock_clase_repository.obtener_clase.return_value = {"id":1}
    
    assert ClasesService.get_by_id(1) == {"id":1}
 
   
@patch("services.clases_service.ClaseRepository")
def test_create_return_none(mock_clase_repository, clase_in_dict):
    mock_clase_repository.crear_clase.return_value = None

    clase_date = ClaseCreate(**clase_in_dict)
    
    with pytest.raises(BaseExceptionError, match="No fue posible crear la clase"):
        ClasesService.create(clase_date)
    
  
@patch("services.clases_service.ClaseRepository")
def test_create_exito(mock_clase_repository, clase_in_dict, clase_out_dict):
    mock_clase_repository.crear_clase.return_value = 1
    mock_clase_repository.obtener_clase.return_value = clase_out_dict
    
    clase_date = ClaseCreate(**clase_in_dict)
    
    resultado = ClasesService.create(clase_date)
    
    assert resultado == clase_out_dict
    
    mock_clase_repository.crear_clase.assert_called_once_with(clase_date.model_dump())
    mock_clase_repository.obtener_clase.assert_called_once_with(1)
    

@patch("services.clases_service.ClaseRepository")
def test_update_clase_no_encontrada(mock_clase_repository, clase_update_dict):
    mock_clase_repository.actualizar_clase.return_value = None

    clase_date = ClaseUpdate(**clase_update_dict)
    
    with pytest.raises(RecursoNoEncontrado, match="Clase no encontrada para actualizar"):
        ClasesService.update(1,clase_date)


@patch("services.clases_service.ClaseRepository")
def test_update_exito(mock_clase_repository, clase_update_dict, clase_out_dict):
    mock_clase_repository.actualizar_clase.return_value = True
    mock_clase_repository.obtener_clase.return_value = clase_out_dict
    
    clase_date = ClaseUpdate(**clase_update_dict)
    
    resultado = ClasesService.update(1,clase_date)
    
    assert resultado == clase_out_dict
    
    clase_request_esperado = clase_date.model_dump()
    clase_request_esperado["id"] = 1
    mock_clase_repository.actualizar_clase.assert_called_once_with(clase_request_esperado)
    mock_clase_repository.obtener_clase.assert_called_once_with(1)


@patch("services.clases_service.ClaseRepository")
def test_delete_error(mock_clase_repository):
    mock_clase_repository.eliminar_clase.return_value = False
    
    with pytest.raises(RecursoNoEncontrado, match="Clase no encontrada para eliminar"):
        ClasesService.delete(1)
        

@patch("services.clases_service.ClaseRepository")
def test_delete_exito(mock_clase_repository):
    mock_clase_repository.eliminar_clase.return_value = True
    
    resultado = ClasesService.delete(1)
    
    assert resultado is None
