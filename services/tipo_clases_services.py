from database import TipoClasesRepository
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