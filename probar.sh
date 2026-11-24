#!/usr/bin/env bash
# Bloque #06 · diapositiva «Probar la API»
# Con la API en marcha (fastapi dev main.py o docker compose up), en otra terminal:  bash probar.sh

URL=http://127.0.0.1:8000

echo "# Crear"
curl -s -X POST $URL/tareas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Repasar REST", "prioridad": 2}'
echo; echo

echo "# Listar"
curl -s $URL/tareas
echo; echo

echo "# Marcar como completada"
curl -s -X PATCH $URL/tareas/1 \
  -H "Content-Type: application/json" \
  -d '{"completada": true}'
echo; echo

echo "# Borrar (204, sin cuerpo)"
curl -s -i -X DELETE $URL/tareas/1
echo

echo "# Pedirla otra vez: 404"
curl -s $URL/tareas/1
echo
