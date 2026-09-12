from fastapi import FastAPI
from app.routers import tasks, categories
from app.database import engine, Base
from app.models import Task, Category


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(tasks.router)
app.include_router(categories.router)


@app.get("/")
async def root():
    return "¡Hola FastAPI!"