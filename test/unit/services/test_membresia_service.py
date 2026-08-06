from unittest.mock import patch
import pytest
from exceptions import RecursoNoEncontrado
from services import MembresiaService

@patch("services.membresia_service.MembresiaRepository")
def test_get_membresia_no_encontrada(mock_membresia_mepository):
    mock_membresia_mepository.obtener_membresia.return_value = None
    
    with pytest.raises(RecursoNoEncontrado, match="Membresia no encontrada"):
        MembresiaService.get_by_id(1)
        
@patch("services.membresia_service.MembresiaRepository")
def test_get_by_id_exito(mock_membresia_mepository):
    mock_membresia_mepository.obtener_membresia.return_value = {"id":1}
    
    resultado = MembresiaService.get_by_id(1)
    
    assert resultado == {"id":1}
    mock_membresia_mepository.obtener_membresia.assert_called_once_with(1)