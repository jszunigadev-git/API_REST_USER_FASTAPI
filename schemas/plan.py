from pydantic import BaseModel, Field, field_validator
from typing import Literal  
from datetime import date

class PlanCreate(BaseModel):
    
    usuario_id : int
    membresia_id : int
    fecha_inicio: date = Field(default_factory=date.today)
    
    
    # Validamos que la fecha_inicio no sea menor al día de hoy
    @field_validator("fecha_inicio")
    @classmethod
    def validar_fecha_no_pasada(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("La fecha de inicio no puede ser una fecha pasada")
        return v
    
    
class PlanCancel(BaseModel):
    
    fecha_fin : date
    estado : Literal["vencido","cancelado"] = Field(
        description="El estado del plan debe ser 'vencido' o 'cancelado'"
    )


class PlanOut(BaseModel):
    id : int
    nombre_usuario : str
    email_usuario : str
    membresia : str
    fecha_inicio: date
    fecha_fin: date
    estado : str
    
    
