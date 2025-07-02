# Dockerfile para Sistema de Inventario FA (Django + PostgreSQL)
FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de la app
WORKDIR /app

# Copiar requirements y archivos de entorno
COPY requirements.txt ./

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Variables de entorno para Django
ENV PYTHONUNBUFFERED=1

# Recopilar archivos estáticos (ignora errores si no existen)
RUN python manage.py collectstatic --noinput || true

# Exponer el puerto de Django
EXPOSE 8000

# Comando por defecto: migrar y lanzar el servidor
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"] 