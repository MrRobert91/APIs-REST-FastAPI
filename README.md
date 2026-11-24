# APIs REST con FastAPI

API de tareas de la masterclass **«APIs REST con FastAPI»** de Factoría F5: la misma API que se construye paso a paso en las diapositivas, completa y lista para ejecutar con Docker o con Python.

📄 Diapositivas: [`docs/masterclass-apis-rest-fastapi.pdf`](docs/masterclass-apis-rest-fastapi.pdf)

## Endpoints

| Método | Ruta | Acción | Respuesta |
|---|---|---|---|
| GET | `/` | Bienvenida | 200 |
| GET | `/tareas?skip=0&limit=10` | Listar las tareas | 200 + lista |
| POST | `/tareas` | Crear una tarea | 201 + tarea |
| GET | `/tareas/{tarea_id}` | Ver una tarea | 200 o 404 |
| PATCH | `/tareas/{tarea_id}` | Modificar algunos campos | 200 o 404 |
| DELETE | `/tareas/{tarea_id}` | Borrar una tarea | 204 o 404 |

Reglas de validación al crear: `titulo` de 3 a 100 caracteres, `descripcion` opcional de hasta 500, `prioridad` entre 1 y 5 (por defecto 1). Si no se cumplen, la API responde **422** con todos los errores.

> Las tareas se guardan **en memoria**: al reiniciar el servidor (o el contenedor) se pierden. Es a propósito, para centrarnos en la API.

## Opción 1: con Docker

Necesitas [Docker](https://docs.docker.com/get-docker/).

```bash
docker compose up --build
```

O sin Compose:

```bash
docker build -t api-tareas .
docker run --rm -p 8000:8000 api-tareas
```

Abre http://localhost:8000/docs para ver y probar la API.

Para ejecutar los tests dentro del contenedor (con él en marcha):

```bash
docker compose exec api python -m pytest
```

## Opción 2: con Python

Necesitas **Python 3.10 o superior**.

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

pip install -r requirements.txt
fastapi dev main.py              # modo desarrollo, con recarga automática
```

Abre http://127.0.0.1:8000/docs.

Tests:

```bash
pytest
```

## Probar con curl

Con la API en marcha, en otra terminal:

```bash
bash probar.sh
```

Crea una tarea, la lista, la marca como completada, la borra y comprueba que después da 404. En Windows con PowerShell las comillas del JSON pueden dar problemas: usa `/docs`, Git Bash o un cliente como Postman o Bruno.

## Archivos

| Archivo | Qué es |
|---|---|
| `main.py` | La API: modelos de Pydantic, almacén en memoria y CRUD completo |
| `test_main.py` | Tests con `TestClient` |
| `probar.sh` | Peticiones de ejemplo con `curl` |
| `Dockerfile` / `docker-compose.yml` | Imagen y arranque con Docker (`fastapi run`, puerto 8000) |
| `docs/` | Las diapositivas de la masterclass en PDF |

## Reto

En la diapositiva «Reto: amplía la API de tareas» tienes seis ejercicios para ampliar `main.py`: fecha límite, filtros, estadísticas, 409 Conflict, PUT y más tests. Como paso siguiente, prueba a separar el código con `APIRouter` como se explica en la diapositiva «APIRouter y estructura de proyecto».
