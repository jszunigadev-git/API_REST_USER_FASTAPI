from repository import MembresiaRepository
from exceptions import RecursoNoEncontrado,capturar_errores_db

class MembresiaService:
    
    @capturar_errores_db
    def get_all():
        return MembresiaRepository.obtener_membresias()
    
    @capturar_errores_db
    def get_by_id(id:int):
        response =  MembresiaRepository.obtener_membresia(id)
        if not response:
            raise RecursoNoEncontrado("Membresia no encontrada")
        return response