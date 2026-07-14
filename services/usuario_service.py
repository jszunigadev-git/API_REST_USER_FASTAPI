
from repository import UsuarioRepository,PlanRepository
from schemas import UsuarioBase, UsuarioPatch , Usuario
from exceptions import RecursoNoEncontrado,capturar_errores_db

class UsuarioService:
    @staticmethod
    @capturar_errores_db
    def get_all(nombre: str | None = None):
        """Puede recibir el parametro '?nombre=n' en la URL para buscar por Nombre de usuario"""
        usuarios = UsuarioRepository.obtener_usuarios(nombre)
        if not usuarios and nombre != None:
            raise RecursoNoEncontrado("Usuario no encontrado")
        return usuarios


    @staticmethod
    @capturar_errores_db
    def get_by_id(id: int):
        usuario = UsuarioRepository.obtener_usuario(id)
        if not usuario:
            raise RecursoNoEncontrado("Usuario no encontrado")
        return usuario


    @staticmethod
    @capturar_errores_db
    def create(data: UsuarioBase):
        id_record = UsuarioRepository.crear_usuario(data.model_dump())
        if id_record:
            nuevo_usuario = Usuario(id=id_record["id"],**data.model_dump()).model_dump()
            return nuevo_usuario
        return None


    @staticmethod
    @capturar_errores_db
    def delete(id: int):
        eliminado = UsuarioRepository.eliminar_usuario(id)
        if not eliminado:
            raise RecursoNoEncontrado("Usuario no encontrado")


    @staticmethod
    @capturar_errores_db
    def update(id: int, data: UsuarioBase):
        usuario_update = Usuario(id=id,**data.model_dump()).model_dump()
        if not UsuarioRepository.actualizar_usuario(usuario_update):
            raise RecursoNoEncontrado("Usuario no encontrado")
        return usuario_update

    @staticmethod
    @capturar_errores_db
    def patch(id: int, data: UsuarioPatch):
        usuario_patch = data.model_dump(exclude_unset=True)   
        actualizar_patch = UsuarioRepository.actualizar_patch_usuario(id, usuario_patch)
        if not actualizar_patch:
            raise RecursoNoEncontrado("Usuario no encontrado")
        return actualizar_patch
    
    @capturar_errores_db
    def is_active_user(id:int):
        """Devuelve bool si el usuario indicado cuenta con planes activos"""
        planes_activos = PlanRepository.obtener_plan_vigente_por_usuario(id)
        if not planes_activos:
            return False
        return True
