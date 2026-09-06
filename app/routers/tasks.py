from fastapi import APIRouter
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