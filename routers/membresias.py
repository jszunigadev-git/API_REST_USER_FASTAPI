from fastapi import APIRouter
from services import MembresiaService
from schemas import Membresia

router = APIRouter(prefix="/membresias", tags=["Membresías"])

@router.get("/", response_model=list[Membresia])
def get_all():
    return MembresiaService.get_all()

@router.get("/{id}", response_model=Membresia)
def get_by_id(id:int):
    return MembresiaService.get_by_id(id)