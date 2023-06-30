# Verwenden Sie ein offizielles Python-Image als Eltern-Image
FROM python:3.9-slim

# Setzen Sie das Arbeitsverzeichnis im Container auf /app
WORKDIR /app

# Installieren Sie die benötigten Python-Bibliotheken
RUN pip install flask requests

# Installieren Sie OpenSSL
RUN apt-get update && apt-get install -y openssl

# Kopieren Sie die benötigten Dateien in den Container
COPY app.py /app
COPY templates /app/templates

# Setzen Sie die Umgebungsvariable für blockierte Domains
ENV BLOCKED_DOMAINS=""

# Fügen Sie den nonrootuser hinzu und setzen Sie die Berechtigungen
RUN groupadd -r nonrootgroup && useradd -r -g nonrootgroup nonrootuser \
    && chown -R nonrootuser:nonrootgroup /app

# Wechseln Sie zum nonrootuser
USER nonrootuser

# Starten Sie die App, wenn der Container gestartet wird
CMD ["python", "app.py"]
