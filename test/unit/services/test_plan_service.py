from unittest.mock import patch
import pytest
from exceptions import RecursoNoEncontrado,RecursoConflictoDependencia,BaseExceptionError
from schemas import PlanCreate
from services import PlanService
from datetime import date
from dateutil.relativedelta import relativedelta


@patch("services.plan_service.PlanRepository")   
def test_get_by_id_plan_no_encontrado(mock_plan_repo):
    mock_plan_repo.obtener_plan_id.return_value = None
    
    with pytest.raises(RecursoNoEncontrado,match="Plan no encontrado"):
        PlanService.get_by_id(1)
     
@patch("services.plan_service.PlanRepository")   
def test_get_by_id_exito(mock_plan_repo):
    mock_plan_repo.obtener_plan_id.return_value = {"id" : 1}
    
    assert PlanService.get_by_id(1) == {"id" : 1}
    
@patch("services.plan_service.PlanRepository")   
def test_get_by_userid_plan_no_encontrado(mock_plan_repo):
    mock_plan_repo.obtener_plan_usuario.return_value = []
    
    with pytest.raises(RecursoNoEncontrado,match="Plan no encontrado"):
        PlanService.get_by_userid(1)
     
@patch("services.plan_service.PlanRepository")   
def test_get_by_userid_exito(mock_plan_repo):
    mock_plan_repo.obtener_plan_usuario.return_value = [{"id" : 1}]

    assert PlanService.get_by_userid(1) == [{"id" : 1}]
    
    
    
@patch("services.plan_service.PlanRepository")   
def test_get_plan_active_by_user_plan_no_encontrado(mock_plan_repo):
    mock_plan_repo.obtener_plan_vigente_por_usuario.return_value = []
    
    with pytest.raises(RecursoNoEncontrado,match="Usuario sin planes vigentes"):
        PlanService.get_plan_active_by_user(1)
     
@patch("services.plan_service.PlanRepository")   
def test_get_plan_active_by_user_exito(mock_plan_repo):
    mock_plan_repo.obtener_plan_vigente_por_usuario.return_value = [{"id" : 1}]

    assert PlanService.get_plan_active_by_user(1) == [{"id" : 1}]
    
@patch("services.plan_service.MembresiaRepository")
def test_create_membresia_no_encontrada(mock_membresia_repo):
    mock_membresia_repo.obtener_membresia.return_value = None

    plan_data = PlanCreate(
        usuario_id=1,
        membresia_id=99,
        fecha_inicio=date.today()
    )

    with pytest.raises(RecursoNoEncontrado, match="Membresia dada no encontrada"):
        PlanService.create(plan_data)
        

@patch("services.plan_service.PlanRepository")       
@patch("services.plan_service.MembresiaRepository")
def test_create_fecha_solapada(mock_membresia_repo,mock_plan_repo):
    mock_membresia_repo.obtener_membresia.return_value = {"duracion_meses":12}
    mock_plan_repo.obtener_plan_vigente_entre_fecha_por_usuario.return_value = True

    plan_data = PlanCreate(
        usuario_id=1,
        membresia_id=99,
        fecha_inicio=date.today()
    )

    with pytest.raises(RecursoConflictoDependencia, match="La fecha ingresada para el servicio choca con un plan activo."):
        PlanService.create(plan_data)


@patch("services.plan_service.PlanRepository")       
@patch("services.plan_service.MembresiaRepository")        
def test_create_base_error(mock_membresia_repo, mock_plan_repo):
    mock_membresia_repo.obtener_membresia.return_value = {"duracion_meses": 12}
    mock_plan_repo.obtener_plan_vigente_entre_fecha_por_usuario.return_value = False
    mock_plan_repo.crear_plan.return_value = None

    plan_data = PlanCreate(
        usuario_id=1,
        membresia_id=99,
        fecha_inicio=date.today()
    )
    
    with pytest.raises(BaseExceptionError,match="No se puedo crear el plan"):
        PlanService.create(plan_data)
        
           
@patch("services.plan_service.PlanRepository")       
@patch("services.plan_service.MembresiaRepository")        
def test_create_exitoso(mock_membresia_repo, mock_plan_repo):
    mock_membresia_repo.obtener_membresia.return_value = {"duracion_meses": 12}
    mock_plan_repo.obtener_plan_vigente_entre_fecha_por_usuario.return_value = False
    mock_plan_repo.crear_plan.return_value = 1
    mock_plan_repo.obtener_plan_id.return_value = {"id":1}
  
    plan_data = PlanCreate(
        usuario_id=1,
        membresia_id=99,
        fecha_inicio=date.today()
    )

    resultado = PlanService.create(plan_data)
    
    assert resultado ==  {"id":1}
    
    

@patch("services.plan_service.PlanRepository")       
@patch("services.plan_service.MembresiaRepository")        
def test_create_exitoso_called_once_with(mock_membresia_repo, mock_plan_repo):
    mock_membresia_repo.obtener_membresia.return_value = {"duracion_meses": 12}
    mock_plan_repo.obtener_plan_vigente_entre_fecha_por_usuario.return_value = False
    mock_plan_repo.crear_plan.return_value = 1
    mock_plan_repo.obtener_plan_id.return_value = {"id": 1}

    fecha_inicio = date.today()
    plan_data = PlanCreate(
        usuario_id=1,
        membresia_id=99,
        fecha_inicio=fecha_inicio
    )

    resultado = PlanService.create(plan_data)

    assert resultado == {"id": 1}

    # Verificamos CON QUÉ argumentos fue llamado crear_plan
    fecha_fin_esperada = fecha_inicio + relativedelta(months=12)
    mock_plan_repo.crear_plan.assert_called_once_with({
        "usuario_id": 1,
        "membresia_id": 99,
        "fecha_inicio": fecha_inicio,
        "estado": "activo",
        "fecha_fin": fecha_fin_esperada
    })
    

@patch("services.plan_service.PlanRepository")
def test_cancelar_plan_no_encontrado(mock_plan_repo):
    mock_plan_repo.obtener_plan_id.return_value = None
    
    with pytest.raises(RecursoNoEncontrado, match="Plan no encontrado"):
        PlanService.cancelar(1)
    


@patch("services.plan_service.PlanRepository")
def test_cancelar_exitoso(mock_plan_repo):
    fecha_inicio = date.today()
    mock_plan_repo.obtener_plan_id.return_value = {"fecha_inicio":fecha_inicio}
    mock_plan_repo.actualizar_plan.return_value = True
    
    resulado =  PlanService.cancelar(1)
    assert resulado is True
    
    fecha_fin_esperada = fecha_inicio + relativedelta(days=1)
    mock_plan_repo.actualizar_plan.assert_called_once_with(1,{
        "fecha_fin": fecha_fin_esperada,
        "estado": "cancelado"
    })


