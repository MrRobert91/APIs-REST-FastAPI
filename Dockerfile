FROM python:3.12-slim

# Evita archivos .pyc y muestra los logs al momento
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Primero las dependencias, para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py test_main.py ./

# Usuario sin privilegios
RUN useradd --create-home appuser
USER appuser

# Puerto en el que escucha la API. Plataformas como Sliplane pueden fijarlo
# con la variable de entorno PORT; si no, se usa 8000.
ENV PORT=8000
EXPOSE 8000

# fastapi run = modo producción (sin recarga automática).
# exec hace que fastapi sea el proceso principal y reciba las señales de parada.
CMD ["sh", "-c", "exec fastapi run main.py --host 0.0.0.0 --port ${PORT}"]
