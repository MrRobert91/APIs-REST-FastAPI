"""Tests de la API de tareas (bloque #07).

Ejecuta:  pytest
"""

from fastapi.testclient import TestClient
from main import app

cliente = TestClient(app)


# --- El test de la diapositiva «Tests con TestClient» ---

def test_crear_y_leer_tarea():
    r = cliente.post("/tareas", json={"titulo": "Test"})
    assert r.status_code == 201
    tarea_id = r.json()["id"]

    r = cliente.get(f"/tareas/{tarea_id}")
    assert r.json()["titulo"] == "Test"


# --- Tests extra: un caso por cada error y por cada endpoint ---

def test_raiz():
    r = cliente.get("/")
    assert r.status_code == 200
    assert r.json() == {"mensaje": "¡Hola, Factoría F5!"}


def test_listar_tareas():
    cliente.post("/tareas", json={"titulo": "Para listar"})
    r = cliente.get("/tareas", params={"limit": 100})
    assert r.status_code == 200
    assert any(t["titulo"] == "Para listar" for t in r.json())


def test_leer_tarea_inexistente_devuelve_404():
    r = cliente.get("/tareas/9999")
    assert r.status_code == 404
    assert r.json() == {"detail": "La tarea 9999 no existe"}


def test_id_no_numerico_devuelve_422():
    r = cliente.get("/tareas/abc")
    assert r.status_code == 422
    assert r.json()["detail"][0]["loc"] == ["path", "tarea_id"]


def test_datos_invalidos_devuelven_422_con_todos_los_errores():
    r = cliente.post("/tareas", json={"titulo": "Ok", "prioridad": 9})
    assert r.status_code == 422
    campos = [error["loc"] for error in r.json()["detail"]]
    assert ["body", "titulo"] in campos
    assert ["body", "prioridad"] in campos


def test_patch_solo_cambia_lo_enviado():
    r = cliente.post("/tareas", json={"titulo": "Repasar REST", "prioridad": 2})
    tarea_id = r.json()["id"]

    r = cliente.patch(f"/tareas/{tarea_id}", json={"completada": True})
    assert r.status_code == 200
    assert r.json()["completada"] is True
    assert r.json()["titulo"] == "Repasar REST"  # no se ha tocado


def test_borrar_tarea():
    r = cliente.post("/tareas", json={"titulo": "Para borrar"})
    tarea_id = r.json()["id"]

    r = cliente.delete(f"/tareas/{tarea_id}")
    assert r.status_code == 204

    r = cliente.get(f"/tareas/{tarea_id}")
    assert r.status_code == 404
