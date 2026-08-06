from repository import UsuarioRepository

def test_crear_y_obtener_usuario():
      
    user_dict = {
        "nombre": "Usuario Test",
        "email": "usuariotest@mail.com",
        "telefono": "+569 89655644",
    }
    
    usuario = UsuarioRepository.crear_usuario(user_dict)
    
    assert usuario is not None
    
    id_usuario = usuario["id"]
    
    try:
        clase = UsuarioRepository.obtener_usuario(id_usuario)
        assert clase["nombre"] == "Usuario Test"
        assert clase["email"] == "usuariotest@mail.com"
        assert clase["telefono"] == "+569 89655644"
    finally:
        UsuarioRepository.eliminar_usuario(id_usuario)
    
    
def test_crear_y_obtener_usuario_filtrado():
      
    user_dict_1 = {
        "nombre": "Usuario Test",
        "email": "usuariotest@mail.com",
        "telefono": "+569 89655644",
    }
    
    user_dict_2 = {
        "nombre": "Usuario filtrado Test",
        "email": "usuariofiltradotest@mail.com",
        "telefono": "+569 99999999",
    }
    
    usuario_1 = UsuarioRepository.crear_usuario(user_dict_1)
    usuario_2 = UsuarioRepository.crear_usuario(user_dict_2)
    

    usuario_filtrado = UsuarioRepository.obtener_usuarios("filtrado")
    encontrado = next((u for u in usuario_filtrado if u["id"] == usuario_2["id"]),None)
    try:
        assert encontrado is not None
        assert encontrado["nombre"] == "Usuario filtrado Test"
        assert encontrado["email"] == "usuariofiltradotest@mail.com"
        assert encontrado["telefono"] == "+569 99999999"
    finally:
        UsuarioRepository.eliminar_usuario(usuario_1["id"])
        UsuarioRepository.eliminar_usuario(usuario_2["id"] )


def test_obtener_usuarios_sin_filtros():
    user_dict = {
        "nombre": "Usuario Test",
        "email": "usuariotest@mail.com",
        "telefono": "+569 89655644",
    }
    
    usuario = UsuarioRepository.crear_usuario(user_dict)
    id_usuario = usuario["id"]
    
    try:
        usuarios = UsuarioRepository.obtener_usuarios()
        encontrado = next((u for u in usuarios if u["id"] == id_usuario), None)
        assert encontrado is not None
        assert encontrado["nombre"] == "Usuario Test"
    finally:
        UsuarioRepository.eliminar_usuario(id_usuario)

def test_actualizar_usuario():
    
    user_dict = {
        "nombre": "Usuario Test",
        "email": "usuariotest@mail.com",
        "telefono": "+569 89655644",
    }
    
    usuario = UsuarioRepository.crear_usuario(user_dict)
    
    assert usuario is not None
    
    id_usuario = usuario["id"]
    
    user_update_dict = {
        "id" : id_usuario,
        "nombre": "Usuario Test update",
        "email": "usuariotestupdate@mail.com",
        "telefono": "+569 89655644",
    }
    try:
        usuario_update = UsuarioRepository.actualizar_usuario(user_update_dict)
        
        assert usuario_update is True
        
        usuario = UsuarioRepository.obtener_usuario(id_usuario)
        assert usuario["nombre"] == "Usuario Test update"
        assert usuario["email"] == "usuariotestupdate@mail.com"
    finally:
        UsuarioRepository.eliminar_usuario(id_usuario)


def test_actualizar_patch_usuario_dict_vacio():
    
    user_dict = {
        "nombre": "Usuario Test",
        "email": "usuariotest@mail.com",
        "telefono": "+569 89655644",
    }
    
    usuario = UsuarioRepository.crear_usuario(user_dict)
    
    assert usuario is not None
    
    id_usuario = usuario["id"]
    
    user_patch_dict = {}
    
    try:
        usuario_patch = UsuarioRepository.actualizar_patch_usuario(id_usuario,user_patch_dict)
        
        assert usuario_patch["nombre"] == "Usuario Test"
        assert usuario_patch["email"] == "usuariotest@mail.com"
    finally:
        UsuarioRepository.eliminar_usuario(id_usuario)

def test_actualizar_patch_usuario_parcial():
    
    user_dict = {
        "nombre": "Usuario Test",
        "email": "usuariotest@mail.com",
        "telefono": None
    }
    
    usuario = UsuarioRepository.crear_usuario(user_dict)
    
    assert usuario is not None
    
    id_usuario = usuario["id"]
    
    user_update_dict = {
        "email": "usuariopatch@mail.com",
        "telefono": "+569 89655644",
    }
    try:
        usuario_patch = UsuarioRepository.actualizar_patch_usuario(id_usuario,user_update_dict)
        

        assert usuario_patch["nombre"] == "Usuario Test"
        assert usuario_patch["email"] == "usuariopatch@mail.com"
        assert usuario_patch["telefono"] == "+569 89655644"
    finally:
        UsuarioRepository.eliminar_usuario(id_usuario)

def test_eliminar_usuario():
    
    user_dict = {
        "nombre": "Usuario Test",
        "email": "usuariotest@mail.com",
        "telefono": "+569 89655644",
    }
    
    usuario = UsuarioRepository.crear_usuario(user_dict)
    
    assert usuario is not None
    id_usuario = usuario["id"]
    
    usuario_delete = UsuarioRepository.eliminar_usuario(id_usuario)
    assert usuario_delete is True
    
