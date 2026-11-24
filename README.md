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

### Desplegar en Sliplane

Crea un servicio desde este repositorio (rama `main`, Dockerfile en la raíz) con esta configuración:

- **Expose Service:** activado.
- **Override CMD:** vacío (se usa el `CMD` del Dockerfile).
- **Health check path:** `/`.
- **Variable de entorno** (opcional): `PORT=8000`. La API escucha en el puerto que indique `PORT` y, si no hay ninguno, en el 8000.

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

## Probar la API desplegada con curl

La API está desplegada en **https://apis-rest-fastapi.sliplane.app**. Puedes probarla desde cualquier terminal sin instalar nada (solo `curl`, que viene en macOS, Linux y Windows 10/11). Su documentación interactiva está en https://apis-rest-fastapi.sliplane.app/docs.

Guarda la URL base en una variable para no repetirla:

```bash
URL=https://apis-rest-fastapi.sliplane.app
```

**Bienvenida**

```bash
curl $URL/
```

**Crear una tarea** (responde `201` con la tarea y su `id`)

```bash
curl -X POST $URL/tareas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Repasar REST", "prioridad": 2}'
```

**Listar las tareas** (con paginación opcional)

```bash
curl $URL/tareas
curl "$URL/tareas?skip=0&limit=5"
```

**Ver una tarea** (cambia `1` por el `id` que te devolvió la creación)

```bash
curl $URL/tareas/1
```

**Marcar como completada** (PATCH: solo cambia los campos que envías)

```bash
curl -X PATCH $URL/tareas/1 \
  -H "Content-Type: application/json" \
  -d '{"completada": true}'
```

**Borrar una tarea** (`-i` muestra el código: `204 No Content`)

```bash
curl -i -X DELETE $URL/tareas/1
```

**Ver los errores**

```bash
curl -i $URL/tareas/9999          # 404: la tarea no existe
curl -i $URL/tareas/abc           # 422: el id no es un número
curl -i -X POST $URL/tareas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Ok", "prioridad": 9}'   # 422: título corto y prioridad fuera de rango
```

**Todo de una vez**: el script `probar.sh` crea una tarea, la lista, la marca como completada, la borra y comprueba que después da 404.

```bash
bash probar.sh https://apis-rest-fastapi.sliplane.app
```

> Las tareas se guardan en memoria y la API es compartida: verás también las tareas que creen otras personas, y todas se borran cuando se reinicia el servidor.

**En Windows:** en PowerShell, `curl` es un alias de otro comando y las comillas del JSON dan problemas. Usa `curl.exe` en lugar de `curl` y escapa las comillas interiores (`-d '{\"titulo\": \"Repasar REST\"}'`), o ejecuta los comandos en Git Bash. También puedes probarlo todo desde `/docs`.

## Probar en local con curl

Con la API en marcha en tu ordenador, en otra terminal:

```bash
bash probar.sh                   # usa http://127.0.0.1:8000 por defecto
```

Los mismos comandos de arriba funcionan cambiando la URL base: `URL=http://127.0.0.1:8000`.

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
