#!/usr/bin/env bash
# Bloque #06 · diapositiva «Probar la API»
# Con la API en marcha (fastapi dev main.py o docker compose up), en otra terminal:  bash probar.sh
# Contra la API desplegada:  bash probar.sh https://apis-rest-fastapi.sliplane.app

URL=${1:-http://127.0.0.1:8000}
echo "Probando $URL"; echo

echo "# Crear"
RESPUESTA=$(curl -s -X POST $URL/tareas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Repasar REST", "prioridad": 2}')
echo "$RESPUESTA"; echo

# El id lo asigna el servidor: lo sacamos de la respuesta
ID=$(echo "$RESPUESTA" | sed -n 's/.*"id":\([0-9]*\).*/\1/p')

echo "# Listar"
curl -s $URL/tareas
echo; echo

echo "# Marcar como completada la tarea $ID"
curl -s -X PATCH $URL/tareas/$ID \
  -H "Content-Type: application/json" \
  -d '{"completada": true}'
echo; echo

echo "# Borrar la tarea $ID (204, sin cuerpo)"
curl -s -i -X DELETE $URL/tareas/$ID
echo

echo "# Pedirla otra vez: 404"
curl -s $URL/tareas/$ID
echo
