from pydantic import BaseModel

class TipoClase(BaseModel):
    id : int
    nombre : str