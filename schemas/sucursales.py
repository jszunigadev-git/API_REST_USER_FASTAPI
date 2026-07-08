from pydantic import BaseModel

class Sucursales(BaseModel):
    id : int
    nombre : str
    