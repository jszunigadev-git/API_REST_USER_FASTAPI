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
        except  psycopg2.errors.ForeignKeyViolation:
            raise RecursoConflictoDependencia("No se pudo eliminar, tiene dependencias")
        except psycopg2.DatabaseError:
            raise DatabaseServiceError()
    return wrapper
