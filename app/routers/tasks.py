from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Task


router = APIRouter()


@router.post("/tasks", response_model=TaskResponse)                                     # response_model valida y da forma a la respuesta según TaskResponse
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):                 # db se obtiene automáticamente vía Depends(get_db) en cada petición
    new_task = Task(                                                                    # Creamos una instancia del modelo SQLAlchemy (no un diccionario)
        description=task.description,
        status="todo",
        category_id=task.category_id
    )                                                                                   # id, created_at y updated_at los genera la base de datos sola

    db.add(new_task)                                                                    # Marcamos el objeto para ser guardado
    db.commit()                                                                         # Confirmamos el cambio en la base de datos
    db.refresh(new_task)                                                                # Recargamos el objeto para obtener el id y fechas ya generados

    return new_task


@router.get("/tasks", response_model=list[TaskResponse])                                # list[TaskResponse] indica que la respuesta es una lista de tareas
async def show_tasks(status_filter: str | None = None, db: Session = Depends(get_db)):
    if status_filter is not None:
        tasks = db.query(Task).filter(Task.status == status_filter).all()               # SQL WHERE status = ...; el filtrado lo hace la base de datos
    else:
        tasks = db.query(Task).all()                                                    # Trae todas las filas de la tabla tasks

    return tasks


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()                            # .first() devuelve la tarea o None si no existe

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No existe ninguna tarea con id {task_id}")

    return task


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_update: TaskUpdate, task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No existe ninguna tarea con id {task_id}")

    if task_update.description is not None:
        task.description = task_update.description                                      # Asignación directa sobre el objeto, sin diccionarios

    if task_update.status is not None:
        task.status = task_update.status

    if task_update.category_id is not None:
        task.category_id = task_update.category_id

    db.commit()                                                                         # updated_at se actualiza solo gracias a onupdate en el modelo
    db.refresh(task)

    return task


@router.delete("/tasks/{task_id}", response_model=TaskResponse)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,                      
            detail=f"No existe ninguna tarea con id {task_id}")

    db.delete(task)                                                                     # SQLAlchemy traduce esto a un DELETE SQL sobre esa fila
    db.commit()

    return task