import json
import os


TASKS_FILE = "tasks.json"


def ensure_file_exists():                                  # Comprobar si el archivo JSON existe si no, lo crea con una lista vacía
    if not os.path.exists(TASKS_FILE):                     # Si no existe, lo creamos en modo escritura ("w")
        with open(TASKS_FILE, "w") as file:                # Guardamos una lista vacía como contenido inicial, para que el archivo ya tenga una estructura JSON válida desde el principio       
            json.dump([], file)


def read_tasks():                                          # Lee el archivo JSON (asegurándose antes de que existe) y devuelve la lista de tareas   
    ensure_file_exists()                                   # Llamamos primero a esta función por seguridad: si es la primera vez que se ejecuta el programa, el archivo aún no existiría y read_tasks fallaría
    with open(TASKS_FILE, "r") as file:                    # Abrimos en modo lectura ("r"); usamos "with" para que el archivo se cierre automáticamente al salir del bloque, incluso si hay un error
        tasks = json.load(file)                            # json.load() convierte el contenido del archivo (texto JSON) en estructuras nativas de Python (aquí, una lista de diccionarios)
    return tasks


def save_tasks(tasks):                                     # Recibe la lista completa de tareas y la escribe en el archivo JSON. Necesita recibir la lista de tareas
    with open(TASKS_FILE, "w") as file:                    # Abrimos en modo escritura ("w"): esto sobrescribe todo el contenido anterior del archivo, por eso siempre le pasamos la lista COMPLETA de tareas, no solo la tarea que cambió
        json.dump(tasks, file)                             # json.dump(datos, archivo) hace lo contrario a json.load(): convierte estructuras de Python a texto JSON y lo escribe en el archivo


def generate_next_id(tasks):                               # Recibe la lista de tareas y devuelve el siguiente id disponible
    if not tasks:                                          # Si la lista está vacía, no hay ningún id existente todavía, así que empezamos desde 1
        return 1

    ids = [task["id"] for task in tasks]                   # Con esta list comprehension, recorremos cada tarea (diccionario) de la lista y extraemos solo su campo "id", generando una lista de ids

    max_id = max(ids)

    return max_id + 1
