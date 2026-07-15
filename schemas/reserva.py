from pydantic import BaseModel
from datetime import datetime

class ReservaCreate(BaseModel):
    usuario_id: int
    clase_id: int

    
class ReservaOut(BaseModel):
    id : int
    estado: str
    clase: str
    usuario: str
    fecha_reserva: datetime