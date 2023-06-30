# Verwenden Sie ein offizielles Python-Image als Eltern-Image
FROM python:3.9-slim

RUN useradd -m tweetfeed

# Setzen Sie das Arbeitsverzeichnis im Container auf /app
WORKDIR /app

# Ändern Sie die Besitzverhältnisse des Verzeichnisses
RUN chown -R tweetfeed:tweetfeed /app

# Kopieren Sie die benötigten Dateien in den Container
COPY app.py /app
COPY templates /app/templates

# Ändern Sie die Besitzverhältnisse des Verzeichnisses
RUN chown -R tweetfeed:tweetfeed /app

USER tweetfeed


# Installieren Sie die benötigten Python-Bibliotheken
RUN pip install flask requests
RUN apt-get update && apt-get install -y openssl

# Setzen Sie die Umgebungsvariable für blockierte Domains
ENV BLOCKED_DOMAINS=""

# Starten Sie die App, wenn der Container gestartet wird
CMD ["python", "app.py"]
