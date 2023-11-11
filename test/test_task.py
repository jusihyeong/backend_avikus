import unittest

from fastapi.testclient import TestClient

from src.app import app
from src.models.schemas.avikus import Task

client = TestClient(app)


class MyTestCase(unittest.TestCase):
    def test_create_task(self):
        response = client.post("/create", json={"name": "John", "content": "something"})
        task = Task(**response.json().get("data"))

        assert response.status_code == 201
        assert task.name == "John"

    def test_get_task(self):
        response = client.post("/create", json={"name": "John", "content": "something"})
        createTask = Task(**response.json().get("data"))
        assert response.status_code == 201
        assert createTask.name == "John"

        response = client.get("/read/" + str(createTask.id))
        getTask = Task(**response.json().get("data"))

        assert response.status_code == 200
        assert createTask.id == getTask.id
        assert createTask.name == getTask.name

    def test_update_task(self):
        response = client.post("/create", json={"name": "John", "content": "something"})
        createTask = Task(**response.json().get("data"))
        assert response.status_code == 201
        assert createTask.name == "John"

        response = client.put("/update/" + str(createTask.id), json={"name": "Sam"})

        updateTask = Task(**response.json().get("data"))

        assert response.status_code == 201
        assert createTask.id == updateTask.id
        assert updateTask.name == "Sam"

    def test_delete_task(self):
        response = client.post("/create", json={"name": "John", "content": "something"})
        createTask = Task(**response.json().get("data"))
        assert response.status_code == 201
        assert createTask.name == "John"
        response = client.delete("/delete/" + str(createTask.id))

        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()
