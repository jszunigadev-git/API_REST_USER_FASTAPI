from repository import SucursalesRepository, ClaseRepository
from exceptions import RecursoNoEncontrado,capturar_errores_db

class SucursalService:
    
    @capturar_errores_db
    def get_all():
        return SucursalesRepository.obtener_sucursales()
    
    @capturar_errores_db
    def get_by_id(id:int):
        response =  SucursalesRepository.obtener_sucursal(id)
        if not response:
            raise RecursoNoEncontrado("Sucursal no encontrada")
        return response
    
    @capturar_errores_db
    def get_clases_by_sucursal(id:int):
        return ClaseRepository.obtener_clase_por_sucursal(id)