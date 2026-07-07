from database import trainerRepository
from schemas import EntrenadorBase,Entrenador
from exceptions import RecursoNoEncontrado,capturar_errores_db

class TrainerService:
    
    @capturar_errores_db
    def get_all():
        return trainerRepository.obtener_entrenadores()
    
    @capturar_errores_db
    def get_by_id(id:int)->dict:
        entrenador = trainerRepository.obtener_entrenador(id)
        if not entrenador:
            raise RecursoNoEncontrado("Entrenador no encontrado")
        return entrenador
        
    @capturar_errores_db
    def create(trainer:EntrenadorBase):
        
        id_trainer = trainerRepository.crear_entrenador(trainer.model_dump())
        nuevo_trainer = Entrenador(id=id_trainer["id"],**trainer.model_dump())
        return nuevo_trainer
    
    @capturar_errores_db
    def update(id:int,trainer:EntrenadorBase):
        entrenador_update = Entrenador(id=id,**trainer.model_dump()).model_dump()
        update_record = trainerRepository.actualizar_entrenador(entrenador_update)
        if not update_record:
            raise RecursoNoEncontrado("Entrenador no encontrado")
        return entrenador_update
    
    @capturar_errores_db
    def delete(id:int):
        delete_record = trainerRepository.eliminar_entrenador(id)
        if not delete_record:
            raise RecursoNoEncontrado("Entrenador no encontrado")
        