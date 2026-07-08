from fastapi import APIRouter
from services import TipoClasesService
from schemas import TipoClase

router = APIRouter(prefix="/tipo-clases", tags=["tipo de clases"])

@router.get("/", response_model=list[TipoClase])
def get_all():
    return TipoClasesService.get_all()

@router.get("/{id}", response_model=TipoClase)
def get_by_id(id:int):
    return TipoClasesService.get_by_id(id)