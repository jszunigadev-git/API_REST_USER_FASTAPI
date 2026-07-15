from fastapi import APIRouter
from services import ReservaService
from schemas import ReservaCreate, ReservaOut

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.get("/",response_model=list[ReservaOut])
def get_reservas():
    return ReservaService.get_all()


@router.get("/{id}",response_model=ReservaOut)
def get_reservas_by_id(id:int):
    return ReservaService.get_all_by_id(id)

@router.post("/",response_model=ReservaOut,status_code=201)
def create_reservas(reserva:ReservaCreate):
    return ReservaService.crear_reserva(reserva)

@router.patch("/{id}/cancelar",status_code=204)
def cancelar_reserva(id : int):
    return ReservaService.cancelar_reserva(id)