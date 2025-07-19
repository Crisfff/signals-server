# Imagen ligera, compatible con TensorFlow-CPU 2.14
FROM python:3.9-slim

# Evitar buffers en stdout/stderr
ENV PYTHONUNBUFFERED=1

# Instalar dependencias de sistema mínimas que TensorFlow necesita
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libglib2.0-0 libsm6 libxext6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Carpeta de trabajo
WORKDIR /app

# Copiar todo el código al contenedor
COPY . .

# Instalar librerías (solo CPU, ¡mucho más liviano!)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
         flask \
         gunicorn \
         numpy \
         tensorflow-cpu==2.14.0

# Puerto en el que escuchará gunicorn (Render pone $PORT)
EXPOSE 8000

# Arrancar el servidor
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000"]
