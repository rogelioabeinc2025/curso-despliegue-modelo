# Construir la imagen del servicio

# Construir la imagen base
# en donde va a correr el codigo
FROM python:3.12-slim

# La carpeta donde va a vivir dentro del contenedor

# puede ser cualquier nombre
WORKDIR /servicio

# quitar LOGS
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
    

# copia de archivo
# copiar solo el requirements
COPY requirements.txt .

# instalamos  las librerias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos los archivos
COPY . .

# Documentacion del puerto que utilizara
EXPOSE 8080

# Correr el despliegue
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]

