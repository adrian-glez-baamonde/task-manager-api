# Task Manager API

API REST para gestión de tareas construida con FastAPI, como proyecto de práctica 
para consolidar conocimientos de backend en Python.

Basado conceptualmente en el proyecto [Task Tracker de roadmap.sh](https://roadmap.sh/projects/task-tracker), 
adaptado de una CLI a una API REST con FastAPI.

## Funcionalidades

- Crear, listar, ver, actualizar y borrar tareas.
- Filtrar tareas por estado (`todo`, `in-progress`, `done`).
- Organizar tareas en categorías (crear y listar categorías, asignar categoría a una tarea).
- Persistencia en base de datos SQLite mediante SQLAlchemy.
- Documentación interactiva automática con Swagger UI.

## Tecnologías

- Python 3.14
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- pytest

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/adrian-glez-baamonde/task-manager-api.git
   cd task-manager-api
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate      # Windows
   source venv/bin/activate     # Linux/Mac
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Arranca el servidor:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Abre la documentación interactiva en tu navegador:
   ```
   http://127.0.0.1:8000/docs
   ```

## Tests

El proyecto incluye tests automáticos con `pytest`, cubriendo los casos de éxito 
y de error de todos los endpoints.

Para ejecutarlos:
```bash
pytest
```

## Endpoints

### Tareas

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/tasks` | Crear una tarea nueva (admite `category_id` opcional) |
| GET | `/tasks` | Listar todas las tareas (admite `?status_filter=` para filtrar por estado) |
| GET | `/tasks/{task_id}` | Ver una tarea concreta |
| PATCH | `/tasks/{task_id}` | Actualizar una tarea (parcial, incluye reasignar `category_id`) |
| DELETE | `/tasks/{task_id}` | Borrar una tarea |

### Categorías

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/categories` | Crear una categoría nueva |
| GET | `/categories` | Listar todas las categorías |

## Nota sobre los comentarios

Este proyecto contuvo inicialmente comentarios más detallados y abundantes de lo 
que sería habitual en código profesional. Es intencional: es uno de mis primeros 
proyectos aprendiendo Python/FastAPI, y comenté extensamente cada línea para 
consolidar mi comprensión mientras lo desarrollaba. A medida que he ido afianzando 
los conceptos, he retirado los comentarios que ya no aportaban información nueva, 
por lo que su densidad ha ido bajando conforme avanzaba el proyecto. En proyectos 
futuros de mi portfolio verás un nivel de comentarios más ajustado a las buenas 
prácticas habituales.