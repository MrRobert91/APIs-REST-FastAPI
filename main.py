"""API de tareas: el proyecto final de la masterclass «APIs REST con FastAPI».

Es el mismo código que se construye en las diapositivas, reunido en un archivo:
- Bloque #03: la app y el endpoint de bienvenida (diapositiva «Hola, mundo»).
- Bloque #05: los modelos TareaCrear, TareaActualizar y Tarea con sus reglas de Field.
- Bloque #06: el almacén en memoria y el CRUD completo.

Ejecuta:  fastapi dev main.py   y abre  http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="API de tareas")


# ---------------------------------------------------------------------------
# Modelos (bloque #05)
# ---------------------------------------------------------------------------

class TareaCrear(BaseModel):  # entrada (POST)
    titulo: str = Field(min_length=3, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    prioridad: int = Field(default=1, ge=1, le=5)


class TareaActualizar(BaseModel):  # entrada (PATCH)
    titulo: str | None = None
    descripcion: str | None = None
    prioridad: int | None = None
    completada: bool | None = None


class Tarea(TareaCrear):  # salida
    id: int
    completada: bool = False


# ---------------------------------------------------------------------------
# «Base de datos» en memoria: id → Tarea (bloque #06, paso 1)
# Al reiniciar el servidor, las tareas se pierden.
# ---------------------------------------------------------------------------

tareas: dict[int, Tarea] = {}
siguiente_id = 1


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
def raiz():
    return {"mensaje": "¡Hola, Factoría F5!"}


# Paso 2: crear y listar
@app.post("/tareas", response_model=Tarea,
          status_code=status.HTTP_201_CREATED)
def crear_tarea(datos: TareaCrear):
    global siguiente_id
    tarea = Tarea(id=siguiente_id, **datos.model_dump())
    tareas[tarea.id] = tarea
    siguiente_id += 1
    return tarea


@app.get("/tareas", response_model=list[Tarea])
def listar_tareas(skip: int = 0, limit: int = 10):
    return list(tareas.values())[skip : skip + limit]


# Paso 3: leer una tarea y devolver 404
@app.get("/tareas/{tarea_id}", response_model=Tarea)
def leer_tarea(tarea_id: int):
    if tarea_id not in tareas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La tarea {tarea_id} no existe",
        )
    return tareas[tarea_id]


# Paso 4: actualizar y borrar
@app.patch("/tareas/{tarea_id}", response_model=Tarea)
def actualizar_tarea(tarea_id: int, cambios: TareaActualizar):
    tarea = leer_tarea(tarea_id)  # 404 si no existe
    datos = cambios.model_dump(exclude_unset=True)
    actualizada = tarea.model_copy(update=datos)
    tareas[tarea_id] = actualizada
    return actualizada


@app.delete("/tareas/{tarea_id}",
            status_code=status.HTTP_204_NO_CONTENT)
def borrar_tarea(tarea_id: int):
    leer_tarea(tarea_id)
    del tareas[tarea_id]
