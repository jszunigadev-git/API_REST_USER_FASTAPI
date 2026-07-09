from functools import wraps
import psycopg2
from .errors import RecursoDuplicado,RecursoConflictoDependencia,DatabaseServiceError

def capturar_errores_db(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except psycopg2.errors.UniqueViolation:
            raise RecursoDuplicado("Error, Existen datos duplicados")
        except  psycopg2.errors.ForeignKeyViolation as e:
            detalle = e.diag.message_detail if e.diag.message_detail else "Uno de los identificadores de referencia no existe o está asociado a otro registro."
            raise RecursoConflictoDependencia(f"Error de dependencias: {detalle}")
        except psycopg2.DatabaseError as e:
            detalle = e.diag.message_primary if e.diag.message_primary else "Error en la operación"
            raise DatabaseServiceError(detalle)
    return wrapper
