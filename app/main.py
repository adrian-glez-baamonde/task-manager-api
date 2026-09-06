from fastapi import FastAPI
from app.routers import tasks


app = FastAPI()


app.include_router(tasks.router)


@app.get("/")
async def root():
    return "¡Hola FastAPI!"