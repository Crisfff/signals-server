FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir flask gunicorn numpy tensorflow-cpu==2.14.0

COPY main.py .
COPY modelo_signals.h5 .

EXPOSE 8000

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000"]
