from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from app.schemas import TaskCreate
from app.storage import read_tasks, save_tasks, generate_next_id


router = APIRouter()                                        


@router.post("/tasks")                                       
async def create_task(task: TaskCreate):                     
    tasks = read_tasks()                                      # Leemos todas las tareas existentes desde el archivo JSON
    new_id = generate_next_id(tasks)                          # Calculamos el siguiente id disponible a partir de las tareas ya existentes

    new_task = {                                              # Construimos la tarea nueva completa como diccionario, ya que storage.py trabaja con diccionarios, no con objetos Pydantic
        "id": new_id,                                         # Usamos el id recién generado
        "description": task.description,                      # La descripción viene del body validado (TaskCreate)
        "status": "todo",                                     # Toda tarea nueva empieza con este estado fijo, no lo decide el usuario
        "created_at": datetime.now().isoformat(),             # Convertimos a string ISO porque un objeto datetime no es serializable directamente a JSON
        "updated_at": datetime.now().isoformat()              # Al crearla, se considera "actualizada" en este mismo instante
    }

    tasks.append(new_task)                                    # Añadimos la tarea nueva a la lista completa de tareas
    save_tasks(tasks)                                         # Guardamos la lista entera (sobrescribiendo el archivo) con la tarea nueva ya incluida
    return new_task                                           # Devolvemos la tarea creada; FastAPI la convierte automáticamente a JSON en la respuesta


@router.get("/tasks")
async def show_tasks(status: str | None = None):                                # "status" es un query parameter opcional; si no se manda, vale None
    tasks = read_tasks()

    if status is not None:                                                      # Si el usuario pidió filtrar por un status concreto
        filtered_tasks = [task for task in tasks if task["status"] == status]   # List Comprehension solo con las tareas cuyo status coincide con el pedido
        return filtered_tasks        
    else:                                                                       # Si no se pidió ningún filtro, devolvemos la lista completa de tareas
        return tasks


@router.get("/tasks/{task_id}")
async def get_task(task_id: int):
    tasks = read_tasks()

    for task in tasks:                                              # Recorremos la lista buscando la tarea con el id pedido
        if task["id"] == task_id:                                   # Si encontramos una tarea cuyo id coincide con task_id, la devolvemos
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,                      # Si el bucle termina sin encontrar ninguna coincidencia, lanzamos un error
        detail=f"No existe ninguna tarea con id {task_id}")


