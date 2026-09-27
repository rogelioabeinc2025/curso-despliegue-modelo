# Imagen base de Python
FROM python:3.11-slim

# Crear directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos de dependencias primero (para aprovechar cache de Docker)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto al contenedor
COPY . .

# Exponer el puerto que usará FastAPI (Render asigna $PORT automáticamente)
EXPOSE 8000

# Comando de arranque: En Render colocar: uvicorn api.main:app --host 0.0.0.0 --port $PORT
# ete sera para pruebas locales
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
