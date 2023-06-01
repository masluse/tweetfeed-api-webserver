# Verwenden Sie ein offizielles Python-Image als Eltern-Image

FROM python:3.9-slim


# Setzen Sie das Arbeitsverzeichnis im Container auf /app

WORKDIR /app


# Kopieren Sie die benötigten Dateien in den Container

COPY app.py /app

COPY templates /app/templates


# Installieren Sie die benötigten Python-Bibliotheken

RUN pip install flask requests


# Starten Sie die App, wenn der Container gestartet wird

CMD ["python", "app.py"]

