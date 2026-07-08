from pydantic import BaseModel

class Membresia(BaseModel):
    id : int
    nombre : str
    precio : int
    duracion_meses : int