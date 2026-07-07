from pydantic import BaseModel

class EntrenadorBase(BaseModel):
    nombre : str
    email: str
    telefono: str
    
class Entrenador(EntrenadorBase):
    id : int
    