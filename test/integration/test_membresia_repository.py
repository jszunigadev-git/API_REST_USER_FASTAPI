
from repository import MembresiaRepository

def test_obtener_membresia_por_id(entidad_membresia):

    id_membresia = entidad_membresia["id_membresia"]
    
    membresia = MembresiaRepository.obtener_membresia(id_membresia)
    assert membresia is not None
    
    assert membresia["nombre"] == "membresia Test"


def test_obtener_membresias_all(entidad_membresia):

    id_membresia = entidad_membresia["id_membresia"]
    
    membresias = MembresiaRepository.obtener_membresias()

    m_encontrada = next((c for c in membresias if c["id"] == id_membresia), None)
    
    assert m_encontrada is not None
    assert m_encontrada["nombre"] == "membresia Test"
