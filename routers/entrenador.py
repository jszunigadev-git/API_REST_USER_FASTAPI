from fastapi import APIRouter
from schemas import EntrenadorBase , Entrenador, ClaseOut
from services import TrainerService


router = APIRouter(prefix="/entrenador", tags=["Entrenador"])

@router.get("/",response_model=list[Entrenador])
def get_trainers():
    return TrainerService.get_all()

@router.get("/{id}")
def get_trainer(id:int):
    return TrainerService.get_by_id(id)

@router.post("/",response_model=Entrenador,status_code=201)
def create_trainer(trainer:EntrenadorBase):
    return TrainerService.create(trainer)

@router.put("/{id}",response_model=Entrenador)
def update_trainer(id:int,trainer:EntrenadorBase):
    return TrainerService.update(id,trainer)


@router.delete("/{id}",status_code=204)
def delete_trainer(id:int):
    return TrainerService.delete(id)

@router.get("/{id}/clases",response_model=list[ClaseOut])
def get_clases_trainer(id:int):
    return TrainerService.get_clases_by_entrenador(id)