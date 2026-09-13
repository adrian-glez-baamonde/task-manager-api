from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_create_task_success():
    response = client.post("/tasks", json={"description": "Estudiar programación"})     # Simulamos una petición POST /tasks con un body válido
    assert response.status_code == 200                                                  # Comprobamos que la petición fue exitosa

    data = response.json()                                                              # Convertimos el cuerpo de la respuesta (JSON) a un diccionario de Python
    assert data["description"] == "Estudiar programación"                               # Comprobamos que los campos tienen los valores esperados
    assert data["status"] == "todo"

    assert "id" in data                                                                 # Comprobamos que estos campos existen en la respuesta (sin exigir un valor concreto)
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_missing_description():
    response = client.post("/tasks", json={})
    assert response.status_code == 422


def test_create_task_with_category():
    response_category = client.post("/categories", json={"name": "Trabajo"})
    category = response_category.json()

    response_task = client.post("/tasks", json={"description": "Estudiar programación", "category_id": category["id"]})
    assert response_task.status_code == 200
    data = response_task.json()

    assert data["description"] == "Estudiar programación"
    assert data["status"] == "todo"
    assert data["category_id"] == category["id"]

    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_all_tasks():
    response_create = client.post("/tasks", json={"description": "Tarea de prueba"})    
    created_task = response_create.json()
    
    response = client.get("/tasks")
    assert response.status_code == 200  

    data = response.json()
    assert any(task["id"] == created_task["id"] for task in data) 


def test_get_tasks_filtered_by_status():
    response_task1 = client.post("/tasks", json={"description": "Tarea todo"})
    task1 = response_task1.json()

    response_task2 = client.post("/tasks", json={"description": "Tarea todo 2"})
    task2 = response_task2.json()
    client.patch(f"/tasks/{task2['id']}", json={"status": "done"})

    response = client.get("/tasks?status_filter=todo")
    assert response.status_code == 200
    data = response.json()

    assert any(task["id"] == task1["id"] for task in data)

    assert not any(task["id"] == task2["id"] for task in data)


def test_get_tasks_by_id_success():
    response_create = client.post("/tasks", json={"description": "Tarea de prueba"})
    created_task = response_create.json()

    response = client.get(f"/tasks/{created_task['id']}")
    assert response.status_code == 200 

    data = response.json()
    assert data["id"] == created_task["id"]


def test_get_tasks_by_id_not_found():
    response = client.get("/tasks/999999")
    assert response.status_code == 404


def test_update_tasks_description():
    response_create = client.post("/tasks", json={"description": "Tarea de prueba"})
    created_task = response_create.json()

    response = client.patch(f"/tasks/{created_task['id']}", json={"description": "Descripción actualizada"})       # Hacemos PATCH mandando solo description

    assert response.status_code == 200

    data = response.json()

    assert data["description"] == "Descripción actualizada"                                                         # Comprobamos que description cambió
    assert data["status"] == "todo"                                                                                 # Comprobamos que status NO cambió (sigue siendo el valor original)


def test_update_tasks_status():
    response_create = client.post("/tasks", json={"description": "Tarea de prueba"})
    created_task = response_create.json()

    response = client.patch(f"/tasks/{created_task['id']}", json={"status": "done"})       

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "done"  
    assert data["description"] == "Tarea de prueba"                                                         


def test_delete_tasks_success():
    response_create = client.post("/tasks", json={"description": "Tarea de prueba"})
    created_task = response_create.json()

    response = client.delete(f"/tasks/{created_task['id']}")
    assert response.status_code == 200 

    response = client.get(f"/tasks/{created_task['id']}")                               # Comprobamos que la tarea ya no existe
    assert response.status_code == 404


def test_delete_tasks_not_found():
    response = client.delete("/tasks/999999")
    assert response.status_code == 404