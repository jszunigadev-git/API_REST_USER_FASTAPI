from unittest.mock import patch
import pytest
from exceptions import RecursoNoEncontrado, RecursoConflictoDependencia, BaseExceptionError
from schemas import ReservaCreate
from services import ReservaService
from datetime import datetime, timedelta


    
@patch("services.reserva_service.ReservaRepository")
def test_get_all_reservas_no_encontrada(mock_reserva_service):
    mock_reserva_service.obtener_reserva_by_id.return_value = None
    
    with pytest.raises(RecursoNoEncontrado, match="Reserva no encontrada"):
        ReservaService.get_all_by_id(1)
        
@patch("services.reserva_service.ReservaRepository")
def test_get_all_reservas_exito(mock_reserva_service):
    mock_reserva_service.obtener_reserva_by_id.return_value = {"id":1}
    
    resultado = ReservaService.get_all_by_id(1)
    
    assert resultado == {"id":1}
    mock_reserva_service.obtener_reserva_by_id.assert_called_once_with(1)
    
        

@patch("services.reserva_service.UsuarioService")
def test_crear_reserva_usuario_no_encontrado(mock_usuario_service):
    mock_usuario_service.get_by_id.return_value = None
    
    reserva_data = ReservaCreate(usuario_id=1, clase_id=1)
    
    with pytest.raises(RecursoNoEncontrado, match="Usuario no encontrado"):
        ReservaService.crear_reserva(reserva_data)
        
@patch("services.reserva_service.UsuarioService")
def test_crear_reserva_sin_plan_vigente(mock_usuario_service):
    mock_usuario_service.get_by_id.return_value = {"id": 1}  # usuario SÍ existe
    mock_usuario_service.is_active_user.return_value = False  # pero sin plan vigente
    
    reserva_data = ReservaCreate(usuario_id=1, clase_id=1)
    
    with pytest.raises(RecursoConflictoDependencia, match="Usuario no cuenta con plan activo"):
        ReservaService.crear_reserva(reserva_data)
  
@patch("services.reserva_service.ClasesService")      
@patch("services.reserva_service.UsuarioService")
def test_crear_reserva_clase_no_encontrada(mock_usuario_service,mock_clases_service):
    mock_usuario_service.get_by_id.return_value = {"id": 1}
    mock_usuario_service.is_active_user.return_value = True 
    mock_clases_service.get_by_id.return_value = None
    
    reserva_data = ReservaCreate(usuario_id=1, clase_id=1)
    
    with pytest.raises(RecursoNoEncontrado, match="Clase no encontrada"):
        ReservaService.crear_reserva(reserva_data)
        
@patch("services.reserva_service.ClasesService")      
@patch("services.reserva_service.UsuarioService")
def test_crear_reserva_fecha_pasada(mock_usuario_service,mock_clases_service):
    mock_usuario_service.get_by_id.return_value = {"id": 1}
    mock_usuario_service.is_active_user.return_value = True
    
    fecha_pasada = datetime.now() - timedelta(days=1)
    mock_clases_service.get_by_id.return_value =  {"id": 1,"fecha_hora":fecha_pasada}
    
    reserva_data = ReservaCreate(usuario_id=1, clase_id=1)
    
    with pytest.raises(RecursoConflictoDependencia, match="la fecha de la clase ya paso, no es posible reservar"):
        ReservaService.crear_reserva(reserva_data)

@patch("services.reserva_service.ReservaRepository")          
@patch("services.reserva_service.ClasesService")      
@patch("services.reserva_service.UsuarioService")
def test_crear_reserva_con_reserva_previa(mock_usuario_service,mock_clases_service,mock_reserva_repo):
    mock_usuario_service.get_by_id.return_value = {"id": 1}
    mock_usuario_service.is_active_user.return_value = True
    
    fecha_reserva = datetime.now() + timedelta(days=1)
    mock_clases_service.get_by_id.return_value =  {"id": 1,"fecha_hora":fecha_reserva}
    mock_reserva_repo.reserva_usuario_clase.return_value = True
    
    reserva_data = ReservaCreate(usuario_id=1, clase_id=1)
    
    with pytest.raises(RecursoConflictoDependencia, match="Usuario ya reservo esta clase, no es posible volver a reservar"):
        ReservaService.crear_reserva(reserva_data)
        

@patch("services.reserva_service.ReservaRepository")          
@patch("services.reserva_service.ClasesService")      
@patch("services.reserva_service.UsuarioService")
def test_crear_reserva_sin_cupos(mock_usuario_service,mock_clases_service,mock_reserva_repo):
    mock_usuario_service.get_by_id.return_value = {"id": 1}
    mock_usuario_service.is_active_user.return_value = True
    
    fecha_reserva = datetime.now() + timedelta(days=1)
    mock_clases_service.get_by_id.return_value =  {"id": 1,"fecha_hora":fecha_reserva}
    mock_reserva_repo.reserva_usuario_clase.return_value = False
    mock_reserva_repo.crear_reserva_con_lock.return_value = None
    
    reserva_data = ReservaCreate(usuario_id=1, clase_id=1)
    
    with pytest.raises(RecursoConflictoDependencia, match="No quedan cupos para la clase"):
        ReservaService.crear_reserva(reserva_data)

   
@patch("services.reserva_service.ReservaRepository")          
@patch("services.reserva_service.ClasesService")      
@patch("services.reserva_service.UsuarioService")
def test_crear_reserva_error_base(mock_usuario_service,mock_clases_service,mock_reserva_repo):
    mock_usuario_service.get_by_id.return_value = {"id": 1}
    mock_usuario_service.is_active_user.return_value = True
    
    fecha_reserva = datetime.now() + timedelta(days=1)
    mock_clases_service.get_by_id.return_value =  {"id": 1,"fecha_hora":fecha_reserva}
    mock_reserva_repo.reserva_usuario_clase.return_value = False
    mock_reserva_repo.crear_reserva_con_lock.return_value = 1
    mock_reserva_repo.obtener_reserva_by_id.return_value = None
    
    
    reserva_data = ReservaCreate(usuario_id=1, clase_id=1)
    
    with pytest.raises(BaseExceptionError, match="La reserva se creó pero no pudo recuperarse"):
        ReservaService.crear_reserva(reserva_data)
        
   
@patch("services.reserva_service.ReservaRepository")          
@patch("services.reserva_service.ClasesService")      
@patch("services.reserva_service.UsuarioService")
def test_crear_reserva_exito(mock_usuario_service,mock_clases_service,mock_reserva_repo):
    mock_usuario_service.get_by_id.return_value = {"id": 1}
    mock_usuario_service.is_active_user.return_value = True
    
    fecha_reserva = datetime.now() + timedelta(days=1)
    mock_clases_service.get_by_id.return_value =  {"id": 1,"fecha_hora":fecha_reserva}
    mock_reserva_repo.reserva_usuario_clase.return_value = False
    mock_reserva_repo.crear_reserva_con_lock.return_value = 1
    mock_reserva_repo.obtener_reserva_by_id.return_value = {"id": 1}
    
    
    reserva_data = ReservaCreate(usuario_id=1, clase_id=1)
    
    assert ReservaService.crear_reserva(reserva_data) == {"id": 1}
    
    
@patch("services.reserva_service.ReservaRepository")
def test_cancelar_reserva_no_encontrada(mock_reserva_repo):
    mock_reserva_repo.obtener_reserva_by_id.return_value = None
    
    with pytest.raises(RecursoNoEncontrado, match="Reserva no encontrada"):
        ReservaService.cancelar_reserva(1)
        

@patch("services.reserva_service.ReservaRepository")
def test_cancelar_reserva_ya_cancelada(mock_reserva_repo):
    mock_reserva_repo.obtener_reserva_by_id.return_value = {"id": 1,"estado":"cancelada"}
    
    with pytest.raises(RecursoConflictoDependencia, match="Reserva ya se encuentra cancelada."):
        ReservaService.cancelar_reserva(1)
        
@patch("services.reserva_service.ReservaRepository")
def test_cancelar_reserva_fecha_pasada(mock_reserva_repo):
    fecha_pasada = datetime.now() - timedelta(days=1)
    mock_reserva_repo.obtener_reserva_by_id.return_value = {"id": 1,"estado":"confirmada","fecha_hora_clase":fecha_pasada}
    
    with pytest.raises(RecursoConflictoDependencia, match="la fecha de la clase ya paso, no es posible cancelar"):
        ReservaService.cancelar_reserva(1)
        
@patch("services.reserva_service.ReservaRepository")
def test_cancelar_reserva_error(mock_reserva_repo):
    fecha_clase = datetime.now() + timedelta(days=1)
    mock_reserva_repo.obtener_reserva_by_id.return_value = {"id": 1,"estado":"confirmada","fecha_hora_clase":fecha_clase}
    mock_reserva_repo.cancelar_reserva_lock.return_value = False
    
    with pytest.raises(RecursoConflictoDependencia, match="No es posible cancelar la reserva"):
        ReservaService.cancelar_reserva(1)
        
@patch("services.reserva_service.ReservaRepository")
def test_cancelar_reserva_exito(mock_reserva_repo):
    fecha_clase = datetime.now() + timedelta(days=1)
    mock_reserva_repo.obtener_reserva_by_id.return_value = {"id": 1,"estado":"confirmada","fecha_hora_clase":fecha_clase}
    mock_reserva_repo.cancelar_reserva_lock.return_value = True
    
    assert ReservaService.cancelar_reserva(1) is True