from fastapi import FastAPI
from app.routers import tasks
from app.database import engine, Base
from app.models import Task


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(tasks.router)


@app.get("/")
async def root():
    return "¡Hola FastAPI!"