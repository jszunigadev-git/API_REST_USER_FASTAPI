from pydantic import BaseModel , Field


class UsuarioBase(BaseModel): #pydantic valida los datos
    nombre:str = Field(...,min_length=3,max_length=50)
    email:str  = Field(...,min_length=5)
    telefono: str|None = None

class Usuario(UsuarioBase):
    id:int


class UsuarioPatch(BaseModel):
    nombre:str|None = Field(None,min_length=3,max_length=50)
    email:str|None = Field(None,min_length=5)
    telefono: str|None = None
    
    

