from repository import PlanRepository, MembresiaRepository
from exceptions import RecursoNoEncontrado,capturar_errores_db , RecursoConflictoDependencia , BaseExceptionError
from schemas import PlanCreate, PlanCancel
from dateutil.relativedelta import relativedelta

class PlanService:
    
    @capturar_errores_db
    def get_all():
        return PlanRepository.obtener_planes()
    
    
    @capturar_errores_db
    def get_by_id(plan_id:int):
        response = PlanRepository.obtener_plan_id(plan_id)
        if not response:
            raise RecursoNoEncontrado("Plan no encontrado")
        return response
    
    @capturar_errores_db
    def get_by_userid(user_id:int):
        response = PlanRepository.obtener_plan_usuario(user_id)
        if not response:
            raise RecursoNoEncontrado("Plan no encontrado")
        return response
    
    @capturar_errores_db
    def get_plan_active_by_user(user_id:int):
        planes_activos = PlanRepository.obtener_plan_vigente_por_usuario(user_id)
        if not planes_activos:
            raise RecursoNoEncontrado("Usuario sin planes vigentes")
        return planes_activos
    
    
    @capturar_errores_db
    def create(plan:PlanCreate):
        
        plan_dict = plan.model_dump()
        usuario_id = plan_dict["usuario_id"]
        plan_dict["estado"] = "activo"
        membresia_id = plan_dict["membresia_id"]
        
        membresia = MembresiaRepository.obtener_membresia(membresia_id)
        if not membresia:
            raise RecursoNoEncontrado("Membresia dada no encontrada en la base de datos")
        
        meses_duracion = membresia["duracion_meses"]
        
        # Calcular la fecha de fin
        fecha_inicio = plan_dict["fecha_inicio"] 
        fecha_fin = fecha_inicio + relativedelta(months=meses_duracion)
        plan_dict["fecha_fin"] = fecha_fin
        
        verificar_bloque = PlanRepository.obtener_plan_vigente_entre_fecha_por_usuario(usuario_id,fecha_inicio,fecha_fin)
        
        if verificar_bloque:
            raise RecursoConflictoDependencia("La fecha ingresada para el servicio choca con un plan activo.")
        
        id_plan = PlanRepository.crear_plan(plan_dict)
        if not id_plan:
            raise BaseExceptionError("No se puedo crear el plan") 
        return PlanRepository.obtener_plan_id(id_plan)
          
    @capturar_errores_db
    def cancelar(id_plan:int):
       plan = PlanRepository.obtener_plan_id(id_plan)
       if not plan:
           raise RecursoNoEncontrado("Plan no encontrado")

       fecha_fin_plan = plan["fecha_inicio"] + relativedelta(days=1)
       estado_plan = "cancelado"
       plan_cancelado = PlanCancel(fecha_fin=fecha_fin_plan, estado=estado_plan)
       
       return PlanRepository.actualizar_plan(id_plan,plan_cancelado.model_dump())
