
from unittest.mock import patch
import pytest
from exceptions import RecursoNoEncontrado
from services import TipoClasesService

@patch("services.tipo_clases_services.TipoClasesRepository")
def test_get_tipo_clase_no_encontrada(mock_tipo_clases_repository):
    mock_tipo_clases_repository.obtener_tipo_clase.return_value = None
    
    with pytest.raises(RecursoNoEncontrado, match="Tipo de clase no encontrada"):
        TipoClasesService.get_by_id(1)
        
@patch("services.tipo_clases_services.TipoClasesRepository")
def test_get_by_id_exito(mock_tipo_clases_repository):
    mock_tipo_clases_repository.obtener_tipo_clase.return_value = {"id":1}
    
    resultado = TipoClasesService.get_by_id(1)
    
    assert resultado == {"id":1}
    mock_tipo_clases_repository.obtener_tipo_clase.assert_called_once_with(1)