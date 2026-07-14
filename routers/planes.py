from fastapi import APIRouter
from schemas import PlanCreate,  PlanOut
from services import PlanService

router = APIRouter(prefix="/planes", tags=["Planes"])


@router.get("/",response_model=list[PlanOut])
def get_all():
    return PlanService.get_all()

@router.get("/{id}",response_model=PlanOut)
def get_by_id(id:int):
    return PlanService.get_by_id(id)

@router.post("/",response_model=PlanOut, status_code=201)
def post(plan:PlanCreate):
    return PlanService.create(plan)

@router.patch("/{id}/cancelar",status_code=204)
def cancelar_plan(id:int):
    return PlanService.cancelar(id)

