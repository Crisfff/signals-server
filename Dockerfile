# 1. Imagen base ligera con Python 3.9
FROM python:3.9-slim

# 2. Evitar buffers en logs
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo
WORKDIR /app

# 4. Copiar sólo los ficheros necesarios (incluye tu modelo .h5)
COPY main.py modelo_signals.h5 requirements.txt ./

# 5. Instalar dependencias Python (CPU-only)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libglib2.0-0 libsm6 libxext6 libxrender1 && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        flask \
        gunicorn \
        numpy \
        tensorflow-cpu==2.14.0 && \
    rm -rf /var/lib/apt/lists/*

# 6. Exponer puerto (Render usará el 8000 por defecto en Docker)
EXPOSE 8000

# 7. Comando de inicio
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000"]
