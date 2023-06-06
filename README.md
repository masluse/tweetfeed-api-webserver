# TweetFeed Live Docker Flask-Anwendung

Diese Anwendung ist eine Docker-Flask-Anwendung, die Daten von der TweetFeed Live API abruft und anzeigt. Benutzer können ein Datum auswählen, und die Anwendung zeigt die entsprechenden Tweets und IPs an, die an diesem Tag veröffentlicht wurden.

## Voraussetzungen

Um diese Anwendung auszuführen, müssen die folgenden Voraussetzungen erfüllt sein:

- Docker: Stellen Sie sicher, dass Docker auf Ihrem System installiert ist.

## Installation

1. Klone das Repository auf deinen lokalen Computer und Navigiere in das Verzeichnis des geklonten Repositorys:
  ``` bash
  git clone https://github.com/masluse/tweetfeed-api-webserver
  cd tweetfeed-api-webserver
  ```
2. Baue das Docker-Image:
  ``` bash
  docker build -t masluse/tweetfeed-api-webserver:latest .
  ```
3. Führe den Docker-Container aus:
  ``` bash
  docker run -d -p 5000:5000 masluse/tweetfeed-api-webserver:latest
  ```
4. Öffne einen Webbrowser und gehe zu http://localhost:5000, um die Anwendung aufzurufen.
# Docker-Compose
``` yaml
version: "3.8"
services:
  tweetfeed-api-webserver:
    image: masluse/tweetfeed-api-webserver:latest
    container_name: tweetfeed-api-webserver
    ports:
      - 5000:5000
    environment:
      - BLOCKED_DOMAINS=domain1,domain2,domain3
      - TZ=Europe/Zurich
    restart: always
```

# Anwendung verwenden
- Stelle sicher, dass Docker auf deinem System ordnungsgemäß konfiguriert und ausgeführt wird.
- Die Anwendung ruft Daten von der TweetFeed Live API ab. Stelle sicher, dass du eine stabile Internetverbindung hast, um die API abzurufen.
- Diese Anwendung ist nur für den persönlichen Gebrauch gedacht und sollte nicht in einer produktiven Umgebung eingesetzt werden.

Docker Hub: https://hub.docker.com/r/masluse/tweetfeed-api-webserver
