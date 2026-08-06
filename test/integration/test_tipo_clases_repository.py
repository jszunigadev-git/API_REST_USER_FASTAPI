
from repository import TipoClasesRepository


def test_obtener_tipo_clase_por_id(entidad_tipo_clase):

    id_tipo_clase = entidad_tipo_clase["tipo_clase_id"]
    
    tipo_clase = TipoClasesRepository.obtener_tipo_clase(id_tipo_clase)
    assert tipo_clase is not None
    
    assert tipo_clase["nombre"] == "Tipo Clase Test"


def test_obtener_tipo_clase_all(entidad_tipo_clase):

    id_tipo_clase = entidad_tipo_clase["tipo_clase_id"]
    
    tipo_clases = TipoClasesRepository.obtener_tipo_clases()

    encontrada = next((c for c in tipo_clases if c["id"] == id_tipo_clase), None)
    
    assert encontrada is not None
    assert encontrada["nombre"] == "Tipo Clase Test"

