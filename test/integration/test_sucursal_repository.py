from repository import SucursalesRepository

def test_obtener_sucursal_por_id(entidad_sucursal):

    id_sucursal = entidad_sucursal["id_sucursal"]
    
    sucursal = SucursalesRepository.obtener_sucursal(id_sucursal)
    assert sucursal is not None
    
    assert sucursal["nombre"] == "Sucursal Test"


def test_obtener_sucursales_all(entidad_sucursal):

    id_sucursal = entidad_sucursal["id_sucursal"]
    
    sucursal = SucursalesRepository.obtener_sucursales()

    s_encontrada = next((c for c in sucursal if c["id"] == id_sucursal), None)
    
    assert s_encontrada is not None
    assert s_encontrada["nombre"] == "Sucursal Test"

