<div align="center">
<img style="width: 100px;" src="./docs/lanis.jpeg"> 

<h3 style="text-align: center;">Lanis-App</h3>
</div>


-----

<div align="center">

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/dewenni/lanis/docker_build_latest.yml)
![Docker Pulls](https://img.shields.io/docker/pulls/dewenni/lanis)
![GitHub last commit](https://img.shields.io/github/last-commit/dewenni/lanis)
[![Current Release](https://img.shields.io/github/release/dewenni/lanis.svg)](https://github.com/dewenni/lanis/releases/latest)
![GitHub watchers](https://img.shields.io/github/watchers/dewenni/lanis?style=social)
[![GitHub stars](https://img.shields.io/github/stars/dewenni/lanis.svg?style=social&label=Star)](https://github.com/dewenni/lanis/stargazers/)

</div>

-----

<div align="center">
wenn es dir gefällt, drück den <b>[ Star ⭐️ ] </b> und klick auf <b>[ watch 👁 ]</b> um auf dem Laufenden zu bleiben
</div>

-----

# Lanis

Lanis ist eine Anwendung, die Informationen vom [Schulportal Hessen](https://start.schulportal.hessen.de/index.php) abruft und als Pushover-Nachrichten versendet. Die App ist als Docker-Anwendung vorbereitet und kann einfach über Docker Compose ausgeführt werden. Als Basis dient die [LanisAPI](https://github.com/lanis-mobile/LanisAPI)

## Features

- Abrufen von Informationen in einstellbaren Intervallen: Du kannst die Abfrageintervalle flexibel über die Konfigurationsdatei einstellen.
- Benachrichtigung bei neuen unerledigten Hausaufgaben: Sobald neue Hausaufgaben anstehen, erhältst du eine Benachrichtigung per Pushover.
- Benachrichtigung bei neuen Nachrichten: Wenn neue Nachrichten im Schulportal eintreffen, wirst du ebenfalls benachrichtigt.
- Kalenderintegration: Die App liest den Kalender aus und filtert nach Kategorien und Schlüsselwörtern. Bei neuen Einträgen wirst du per Pushover informiert. Zusätzlich werden zwei Kalenderdateien im ICS-Format erstellt, die über einen eingebauten Webserver bereitgestellt werden. Diese Kalender können von deiner Kalender-App abonniert werden.

## Installation

**Docker Compose:**  
Im Ordner `examples` findest du ein Beispiel für eine `docker-compose.yaml`.

**Konfigurationsdatei:**  
Eine Vorlage der `config.ini` liegt ebenfalls im `examples`-Ordner. Du kannst sie an deine Bedürfnisse anpassen.

> [!NOTE] 
> Ein aktuelles Image steht immer im [Docker-Hub](https://hub.docker.com/repository/docker/dewenni/lanis/general) zur Verfügung. Ihr benötigt eigentlich nur das `docker-compose.yaml` von dieser Git-Hub Seite!

## Docker Compose Setup

Um die Anwendung **Lanis** schnell in einem Docker-Container auszuführen, kannst du das bereitgestellte `docker-compose.yaml`-Beispiel verwenden. 
Der folgende Code kann als Referenz für dein Setup dienen:

`docker-compose.yaml`
```yaml
services:
  lanis-app:
    image: dewenni/lanis:latest
    network_mode: host
    container_name: lanis
    environment:
      - INTERVAL=3600     # Zeitintervall für Abfragen in Sekunden
      - HTTP_PORT=4040    # Umgebungsvariable für den HTTP-Server
    pull_policy: always
    volumes:
      - /volume1/docker/lanis/config:/app/config    # Verzeichnis für config.ini
      - /volume1/docker/lanis/output:/app/output    # Verzeichnis für output Dateien
      - /volume1/docker/lanis/log:/var/log          # Verzeichnis für log Datein
```

## Verwendung

Überprüfe und Ändere die Einstellungen im docker-compose.yaml nach deinen Bedürfnissen. Stelle sicher, dass die angegebenen Verzeichnise als Volume existieren.
Überprüfe und Ändere die Einstellungen in der config.ini mit deinen Daten und nach deinen Bedürfnissen.

```ini
[lanis]
school = 1234                   # ID der Schule
username = Vorname.Nachname     # Vorname.Name
password = Passwort             # Passwort 

[pushover]
user_keys = xxx                 # Pushover User-Keys (Mehrere User_Keys mit Komma trennen)
api_token = xxx                 # Pushover API-Token  

[options]
tasks = true                    # lese Hausaufgaben
conversations = true            # lese Benachrichtigungen
calendar = true                 # lese Kalendereinträge

[calendar]
start_date = 2024-10-02         # Start Datum für Kalenderabfrage
end_date = 2024-11-02           # Ende Datum für Kalenderabfrage
filter_categories = 12          # Filter auf Kalender Kategorien (12=Arbeiten)
filter_keywords = 5g1           # Filter auf Schlüsselwörter wie z.B. Klasse (Keyword1, Keyword2, ..)
```

## Hinweise

### Schul-ID
Die Schul-ID kann man aus der URL vom Schulportal herauslesen
(?=i) in der URL: `https://start.schulportal.hessen.de/?i=SCHOOLID`

### Pushover
Um Pushover verwenden zu können, müsst ihr euch bei Pushover anmelden.
Jede Anwendung, jeder Dienst oder jedes Dienstprogramm, das Benachrichtigungen über die API von Pushover sendet, benötigt ein eigenes API-Token, das alle API-Anfragen eindeutig identifiziert.
API-Tokens sind kostenlos und können über [Pushover-Website](https://pushover.net/apps/build) registriert werden.