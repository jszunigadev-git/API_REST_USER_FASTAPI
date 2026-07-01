#errors.py
class BaseExceptionError(Exception):
    status_code = 500
    
class RecursoNoEncontrado(BaseExceptionError):
    status_code = 404

class RecursoDuplicado(BaseExceptionError):
    status_code = 409

class RecursoConflictoDependencia(BaseExceptionError):
    status_code = 400

class DatabaseServiceError(BaseExceptionError):
    status_code = 500