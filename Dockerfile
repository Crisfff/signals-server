# Dockerfile definitivo
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# ----- 1️⃣  Dependencias básicas + Git-LFS -----
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git-lfs build-essential \
        libglib2.0-0 libsm6 libxext6 libxrender1 && \
    git lfs install && \
    rm -rf /var/lib/apt/lists/*

# ----- 2️⃣  Copiar repo y bajar los binarios LFS -----
COPY . .
RUN git lfs pull

# ----- 3️⃣  Instalar librerías Python -----
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        flask \
        gunicorn \
        numpy \
        tensorflow-cpu==2.14.0

EXPOSE 8000
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000"]
