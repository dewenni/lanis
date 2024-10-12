# Basis-Image
FROM python:3-slim

# Arbeitsverzeichnis erstellen
WORKDIR /app

# App-Dateien kopieren
COPY app/ /app/

# Abhängigkeiten installieren
RUN pip install --no-cache-dir -r requirements.txt

# Supervisor installieren
RUN apt-get update && apt-get install -y supervisor

# Supervisor-Konfiguration kopieren
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start Supervisor
CMD ["/usr/bin/supervisord"]