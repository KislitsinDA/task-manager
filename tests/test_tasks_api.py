
from __future__ import annotations

from http import HTTPStatus

def test_create_task(client):
    payload = {"title": "Write tests", "description": "Cover all endpoints"}
    r = client.post("/tasks", json=payload)
    assert r.status_code == HTTPStatus.CREATED
    data = r.json()
    assert data["id"]
    assert data["title"] == "Write tests"
    assert data["description"] == "Cover all endpoints"
    assert data["status"] == "created"


def test_create_validation(client):
    r = client.post("/tasks", json={"title": ""})
    assert r.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_task(client):
    created = client.post("/tasks", json={"title": "T1"}).json()
    r = client.get(f"/tasks/{created['id']}")
    assert r.status_code == HTTPStatus.OK
    assert r.json()["title"] == "T1"


def test_list_tasks(client):
    client.post("/tasks", json={"title": "A"})
    client.post("/tasks", json={"title": "B"})
    r = client.get("/tasks")
    assert r.status_code == HTTPStatus.OK
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_update_task(client):
    created = client.post("/tasks", json={"title": "Old"}).json()
    r = client.patch(f"/tasks/{created['id']}", json={"title": "New", "status": "in_progress"})
    assert r.status_code == HTTPStatus.OK
    data = r.json()
    assert data["title"] == "New"
    assert data["status"] == "in_progress"


def test_update_not_found(client):
    r = client.patch("/tasks/00000000-0000-0000-0000-000000000000", json={"title": "X"})
    assert r.status_code == HTTPStatus.NOT_FOUND


def test_delete_task(client):
    created = client.post("/tasks", json={"title": "To delete"}).json()
    r = client.delete(f"/tasks/{created['id']}")
    assert r.status_code == HTTPStatus.NO_CONTENT
    r2 = client.get(f"/tasks/{created['id']}")
    assert r2.status_code == HTTPStatus.NOT_FOUND
