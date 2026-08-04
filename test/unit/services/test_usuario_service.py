
from unittest.mock import patch
import pytest
from exceptions import RecursoNoEncontrado,BaseExceptionError
from services import UsuarioService
from schemas import UsuarioBase, UsuarioPatch , Usuario



@pytest.fixture
def usuario_base():
    return {
        "nombre" : "Nombre Usuario",
        "email": "usuario@mail.com",
        "telefono": "+569 89999999" 
    }

@pytest.fixture
def usuario():
    return {
        "id" : 1,
        "nombre" : "Nombre Usuario",
        "email": "usuario@mail.com",
        "telefono": "+569 89999999" 
    }

    
@patch("services.usuario_service.UsuarioRepository")
def test_get_usuario_id_no_encontrado(mock_usuario_repository):
    mock_usuario_repository.obtener_usuario.return_value = None
    
    with pytest.raises(RecursoNoEncontrado, match="Usuario no encontrado"):
        UsuarioService.get_by_id(1)
        
@patch("services.usuario_service.UsuarioRepository")
def test_get_usuario_id_exito(mock_usuario_repository):
    mock_usuario_repository.obtener_usuario.return_value = {"id":1}
    
    resultado = UsuarioService.get_by_id(1)
    
    assert resultado == {"id":1}
    mock_usuario_repository.obtener_usuario.assert_called_once_with(1)
    

@patch("services.usuario_service.UsuarioRepository")
def test_get_all_usuario_no_encontrado(mock_usuario_repository):
    mock_usuario_repository.obtener_usuarios.return_value = None
    
    with pytest.raises(RecursoNoEncontrado, match="Usuario no encontrado"):
        UsuarioService.get_all("Test")
        

@patch("services.usuario_service.UsuarioRepository")
def test_get_all_exito(mock_usuario_repository):
    mock_usuario_repository.obtener_usuarios.return_value = None
    
    resultado = UsuarioService.get_all(None)
    
    assert resultado == None
    mock_usuario_repository.obtener_usuarios.assert_called_once_with(None)
    


@patch("services.usuario_service.UsuarioRepository")
def test_create_usuario_no_creado(mock_usuario_repository,usuario_base):
    mock_usuario_repository.crear_usuario.return_value = None
    
    usuario_data = UsuarioBase(**usuario_base)
    with pytest.raises(BaseExceptionError, match="Error al crear usuario"):
        UsuarioService.create(usuario_data)
        
@patch("services.usuario_service.UsuarioRepository")
def test_create_usuario_exito(mock_usuario_repository,usuario_base):
    mock_usuario_repository.crear_usuario.return_value = {"id" : 1}
    
    usuario_data = UsuarioBase(**usuario_base)
    resultado = UsuarioService.create(usuario_data)
    
    usuario_base["id"] = 1

    assert resultado == usuario_base
    mock_usuario_repository.crear_usuario.assert_called_once_with(usuario_data.model_dump())


@patch("services.usuario_service.UsuarioRepository")
def test_delete_error(mock_usuario_repository):
    mock_usuario_repository.eliminar_usuario.return_value = None
    
    with pytest.raises(RecursoNoEncontrado, match="Usuario no encontrado"):
        UsuarioService.delete(1)
        
@patch("services.usuario_service.UsuarioRepository")
def test_delete_exito(mock_usuario_repository):
    mock_usuario_repository.eliminar_usuario.return_value = True
    
    resultado = UsuarioService.delete(1)
    
    assert resultado is None
    mock_usuario_repository.eliminar_usuario.assert_called_once_with(1)    


@patch("services.usuario_service.UsuarioRepository")
def test_update_usuario_no_encontrado(mock_usuario_repository, usuario_base):
    mock_usuario_repository.actualizar_usuario.return_value = False
    
    usuario_data = UsuarioBase(**usuario_base)
    with pytest.raises(RecursoNoEncontrado, match="Usuario no encontrado"):
        UsuarioService.update(1,usuario_data)   


@patch("services.usuario_service.UsuarioRepository")
def test_update_usuario_exito(mock_usuario_repository, usuario_base):
    mock_usuario_repository.actualizar_usuario.return_value = True
    
    usuario_data = UsuarioBase(**usuario_base)

    resultado = UsuarioService.update(1,usuario_data)
    
    usuario_update = usuario_data.model_dump()
    usuario_update["id"] = 1

    assert resultado == usuario_update
    mock_usuario_repository.actualizar_usuario.assert_called_once_with(usuario_update)



@patch("services.usuario_service.UsuarioRepository")
def test_patch_usuario_no_encontrado(mock_usuario_repository, usuario_base):
    mock_usuario_repository.actualizar_patch_usuario.return_value = None
    
    usuario_data = UsuarioPatch(**usuario_base)
    with pytest.raises(RecursoNoEncontrado, match="Usuario no encontrado"):
        UsuarioService.patch(1,usuario_data)
        

@patch("services.usuario_service.UsuarioRepository")
def test_patch_usuario_exito(mock_usuario_repository, usuario_base,usuario):
    
    usuario_data = UsuarioPatch(**usuario_base)
   
    mock_usuario_repository.actualizar_patch_usuario.return_value = usuario
    
    resultado = UsuarioService.patch(1,usuario_data)
    
    assert resultado == usuario
    mock_usuario_repository.actualizar_patch_usuario.assert_called_once_with(1,usuario_base)
