from fastapi import APIRouter
from services import TipoClasesService
from schemas import TipoClase, ClaseOut

router = APIRouter(prefix="/tipo-clases", tags=["tipo de clases"])

@router.get("/", response_model=list[TipoClase])
def get_all():
    return TipoClasesService.get_all()

@router.get("/{id}", response_model=TipoClase)
def get_by_id(id:int):
    return TipoClasesService.get_by_id(id)

@router.get("/{id}/clases",response_model=list[ClaseOut])
def get_clases_by_id(id:int):
    return TipoClasesService.get_clases_by_tipo_clase(id)