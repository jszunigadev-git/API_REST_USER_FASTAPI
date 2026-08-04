from unittest.mock import patch
import pytest
from exceptions import RecursoNoEncontrado
from services import SucursalService

@patch("services.sucursal_service.SucursalesRepository")
def test_get_sucursal_no_encontrada(mock_sucursal_mepository):
    mock_sucursal_mepository.obtener_sucursal.return_value = None
    
    with pytest.raises(RecursoNoEncontrado, match="Sucursal no encontrada"):
        SucursalService.get_by_id(1)
        
@patch("services.sucursal_service.SucursalesRepository")
def test_get_by_id_exito(mock_sucursal_mepository):
    mock_sucursal_mepository.obtener_sucursal.return_value = {"id":1}
    
    resultado = SucursalService.get_by_id(1)
    
    assert resultado == {"id":1}
    mock_sucursal_mepository.obtener_sucursal.assert_called_once_with(1)