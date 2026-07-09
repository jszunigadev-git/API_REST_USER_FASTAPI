from fastapi import APIRouter
from schemas import ClaseCreate,ClaseUpdate, ClaseOut
from services import ClasesService

router = APIRouter(prefix="/clases", tags=["Clases"])


@router.get("/",response_model=list[ClaseOut])
def get_all():
    return ClasesService.get_all()

@router.get("/{id}",response_model=ClaseOut)
def get_by_id(id:int):
    return ClasesService.get_by_id(id)

@router.post("/",response_model=ClaseOut, status_code=201)
def post(clase:ClaseCreate):
    return ClasesService.create(clase)

@router.put("/{id}",response_model=ClaseOut)
def put(id:int,clase:ClaseUpdate):
    return ClasesService.update(id,clase)

@router.delete("/{id}",status_code=204)
def delete(id:int):
    return ClasesService.delete(id)