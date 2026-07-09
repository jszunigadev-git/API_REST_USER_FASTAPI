from fastapi import APIRouter
from services import SucursalService
from schemas import Sucursales,ClaseOut

router = APIRouter(prefix="/sucursales", tags=["Sucursales"])

@router.get("/",response_model=list[Sucursales])
def get_all():
    return SucursalService.get_all()

@router.get("/{id}",response_model=Sucursales)
def get_by_id(id:int):
    return SucursalService.get_by_id(id)

@router.get("/{id}/clases",response_model=list[ClaseOut])
def get_clases(id:int):
    return SucursalService.get_clases_by_sucursal(id)