FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# CAMBIO CLAVE: Actualizar a TF 2.15
RUN pip install --no-cache-dir \
    flask==2.3.3 \
    gunicorn==21.2.0 \
    numpy==1.26.4 \
    tensorflow-cpu==2.15.0  # Versión actualizada

COPY main.py .
COPY modelo_signals.h5 .

EXPOSE 8000

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "--workers", "1"]
