FROM python:3.9-slim

# Instalar dependencias del sistema necesarias para TensorFlow
RUN apt-get update && apt-get install -y \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias de Python con versiones exactas
RUN pip install --no-cache-dir \
    flask==2.3.3 \
    gunicorn==21.2.0 \
    numpy==1.24.4 \
    tensorflow-cpu==2.14.0

COPY main.py .
COPY modelo_signals.h5 .

EXPOSE 8000

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "--workers", "1"]
