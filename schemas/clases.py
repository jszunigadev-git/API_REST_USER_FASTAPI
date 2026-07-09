from pydantic import BaseModel
from datetime import datetime

class ClaseCreate(BaseModel):
    
    tipo_clase_id : int
    sucursal_id : int
    entrenador_id : int
    fecha_hora: datetime
    capacidad : int
    duracion_minutos : int
    
    
class ClaseUpdate(BaseModel):
    tipo_clase_id : int
    sucursal_id : int
    entrenador_id : int
    fecha_hora: datetime
    capacidad : int
    duracion_minutos : int


class ClaseOut(BaseModel):
    id : int
    tipo_clase : str
    sucursal : str
    entrenador : str
    fecha_hora: datetime
    capacidad : int
    duracion_minutos : int