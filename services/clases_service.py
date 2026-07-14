from repository import ClaseRepository
from exceptions import RecursoNoEncontrado,capturar_errores_db
from schemas import ClaseCreate,ClaseUpdate

class ClasesService:
    
    @capturar_errores_db
    def get_all():
        return ClaseRepository.obtener_clases()
    
    @capturar_errores_db
    def get_by_id(id:int):
    
        response = ClaseRepository.obtener_clase(id)
        if not response:
            raise RecursoNoEncontrado("Clase no encontrada")
        return response

    
    @capturar_errores_db
    def create(clase:ClaseCreate):
        id = ClaseRepository.crear_clase(clase.model_dump())
        if id:
            return ClaseRepository.obtener_clase(id)
        
    @capturar_errores_db
    def update(id:int,clase:ClaseUpdate):
        clase_request = clase.model_dump()
        clase_request["id"] = id
        response = ClaseRepository.actualizar_clase(clase_request)
        if not response:
            raise RecursoNoEncontrado("Clase no encontrada para actualizar")
        return ClaseRepository.obtener_clase(id)
    
    @capturar_errores_db
    def delete(id:int):
        response = ClaseRepository.eliminar_clase(id)
        if not response:
            raise RecursoNoEncontrado("Clase no encontrada para eliminar")

        
            