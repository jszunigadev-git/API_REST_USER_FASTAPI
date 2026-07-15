#main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers import *
from exceptions import BaseExceptionError

app = FastAPI()


@app.exception_handler(BaseExceptionError)
def domain_exception_handler(request: Request, exc: BaseExceptionError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc) or "Error en la operación"}
    )


app.include_router(router_user)
app.include_router(router_trainer)
app.include_router(router_sucursal)
app.include_router(router_membresias)
app.include_router(router_tipo_clase)
app.include_router(router_clase)
app.include_router(router_plan)
app.include_router(rouert_reserva)
