from database import TipoClasesRepository, ClaseRepository
from exceptions import RecursoNoEncontrado,capturar_errores_db

class TipoClasesService:
    
    @capturar_errores_db
    def get_all():
        return TipoClasesRepository.obtener_tipo_clases()
    
    @capturar_errores_db
    def get_by_id(id:int):
        response =  TipoClasesRepository.obtener_tipo_clase(id)
        if not response:
            raise RecursoNoEncontrado("Tipo de clase no encontrada")
        return response
    
    @capturar_errores_db
    def get_clases_by_tipo_clase(id:int):
        return ClaseRepository.obtener_clase_por_tipo_clase(id)