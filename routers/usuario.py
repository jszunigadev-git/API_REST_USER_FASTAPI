from fastapi import APIRouter,Query,Path,Body
from schemas import UsuarioBase,Usuario,UsuarioPatch,PlanOut
from services import UsuarioService,PlanService


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# GET  /usuarios
@router.get("/",response_model=list[Usuario]) # response_model (controlar la respuesta final)
def get_users(nombre:str|None = Query(None)): # Query (enviar un valor opcional para filtar datos)
    return UsuarioService.get_all(nombre=nombre)

# GET  /usuarios/{id}
@router.get("/{id}",response_model=Usuario)
def get_user(id:int = Path(..., gt=0)): # Path (puedo validar los datos de entrada, ejemplo controlar ids negativos)
    return UsuarioService.get_by_id(id)


# POST /usuarios
@router.post("/", status_code=201,response_model=Usuario) # status_code seteado a 201 para el exito de un insert
def create_user(usuario:UsuarioBase):
    return   UsuarioService.create(usuario)
        

# DELETE /usuarios/{id}
@router.delete("/{id}", status_code=204) # status_code seteado a 204 para el exito de un delete
def del_user(id:int = Path(..., gt=0) ):
    return  UsuarioService.delete(id)

# PUT /usuarios/{id}
@router.put("/{id}",response_model=Usuario)
def put_user(id:int = Path(..., gt=0) ,usuario:UsuarioBase = Body(...)):
    return  UsuarioService.update(id,usuario)

#Intentar crear PATCH /usuarios/{id} - usuario.model_dump(exclude_unset=True) - class UsuarioPatch(BaseModel):
#UsuarioPatch
@router.patch("/usuarios/{id}",response_model=Usuario)
def patch_user(id:int =Path(...,gt=0), usuario:UsuarioPatch = Body(...)):
    return UsuarioService.patch(id,usuario)


# GET/usuarios
@router.get("/{id}/planes",response_model=list[PlanOut]) 
def get_plan_user(id:int):
    return PlanService.get_plan_active_by_user(id)