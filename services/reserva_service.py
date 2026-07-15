from repository import  ReservaRepository
from services import UsuarioService, ClasesService
from exceptions import capturar_errores_db , RecursoNoEncontrado, RecursoConflictoDependencia, BaseExceptionError
from datetime import datetime
from schemas import ReservaCreate


class ReservaService:
    
    @capturar_errores_db
    def get_all():
        return ReservaRepository.obtener_reservas()
    
    
    @capturar_errores_db
    def get_all_by_id(id:int):
        reserva = ReservaRepository.obtener_reserva_by_id(id)
        if not reserva:
            raise RecursoNoEncontrado("Reserva no encontrada")
        return reserva
    
    
    @capturar_errores_db
    def get_all_by_user_id(id:int):
        return  ReservaRepository.obtener_reservas_by_usuario(id)
 
    @capturar_errores_db
    def crear_reserva(reserva:ReservaCreate)->dict|None:
        
        #Buscar usuario, Usuario existe
        usuario = UsuarioService.get_by_id(reserva.usuario_id)
        if not usuario:
            raise RecursoNoEncontrado("Usuario no encontrado")
        
        # Verificar plan vigente
        plan_vigente = UsuarioService.is_active_user(reserva.usuario_id)
        if not plan_vigente:
            raise RecursoConflictoDependencia("Usuario no cuenta con plan activo, no es posible reservar")
        
        # 3. Buscar clase
        clase = ClasesService.get_by_id( reserva.clase_id)
        if not clase:
            raise RecursoNoEncontrado("Clase no encontrada")
        
        # 4. Verificar fecha de la clase futura
        if clase["fecha_hora"] < datetime.now():
            raise RecursoConflictoDependencia("la fecha de la clase ya paso, no es posible reservar")
        
        # 5. Verificar que no exista una reserva previa. # ✓ Usuario no reservó esa clase
        reserva_previa = ReservaRepository.reserva_usuario_clase(reserva.usuario_id,  reserva.clase_id)
        if reserva_previa:
            raise RecursoConflictoDependencia("Usuario ya reservo esta clase, no es posible volver a reservar")
            
        # 6. Verificar capacidad, Crear la reserva y Disminuir cupos
        id_reserva  = ReservaRepository.crear_reserva_con_lock(reserva.usuario_id,  reserva.clase_id)
        if not id_reserva:
            raise RecursoConflictoDependencia("No quedan cupos para la clase")
        
        # 7. Retornar la reserva creada.
        reserva = ReservaRepository.obtener_reserva_by_id(id_reserva)
        if not reserva:
            raise BaseExceptionError("La reserva se creó pero no pudo recuperarse")
        return reserva
                
                
    @capturar_errores_db
    def cancelar_reserva(reserva_id:int)->bool:
        
        reserva = ReservaRepository.obtener_reserva_by_id(reserva_id)
        if not reserva:
            raise RecursoNoEncontrado("Reserva no encontrada")
        
        if reserva["estado"] == "cancelada":
            raise RecursoConflictoDependencia("Reserva ya se encuentra cancelada.")
        
        if reserva["fecha_hora_clase"] < datetime.now():
            raise RecursoConflictoDependencia("la fecha de la clase ya paso, no es posible cancelar")
        
        reserva_cancelada  = ReservaRepository.cancelar_reserva_lock(reserva_id)
        if not reserva_cancelada:
            raise RecursoConflictoDependencia("No es posible cancelar la reserva")
        
        return reserva_cancelada

