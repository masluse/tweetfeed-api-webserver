# Verwenden Sie ein offizielles Python-Image als Eltern-Image
FROM python:3.9-slim

# Erstellen Sie einen neuen Benutzer namens tweetfeed
RUN useradd -m tweetfeed

# Setzen Sie das Arbeitsverzeichnis im Container auf /app
WORKDIR /app

# Installieren Sie die benötigten Python-Bibliotheken
RUN pip install flask requests

# Installieren Sie OpenSSL
RUN apt-get update && apt-get install -y openssl

# Kopieren Sie die benötigten Dateien in den Container
COPY app.py /app
COPY templates /app/templates

# Ändern Sie die Besitzverhältnisse des Verzeichnisses
RUN chown -R tweetfeed:tweetfeed /app

# Setzen Sie die Umgebungsvariable für blockierte Domains
ENV BLOCKED_DOMAINS=""

# Wechseln Sie zu dem tweetfeed-Benutzer
USER tweetfeed

# Starten Sie die App, wenn der Container gestartet wird
CMD ["python", "app.py"]
