import requests
import logging
import httpx
from config import PUSHOVER_API, PUSHOVER_USERS

LOGGER = logging.getLogger("LanisAPP")

def sendPushover(title, message):
    """Sendet eine Pushover-Nachricht an alle definierten Empfänger."""
    
    url = "https://api.pushover.net/1/messages.json"
    for user_key in PUSHOVER_USERS:
        data = {
            "token": PUSHOVER_API,
            "user": user_key,
            "title": title,
            "message": message
        }
        try:
            response = httpx.post(url, data=data)
            if response.status_code == 200:
                LOGGER.info(f"Nachricht erfolgreich an {user_key} gesendet.")
            else:
                LOGGER.warning(f"Fehler beim Senden an {user_key}: {response.text}")
        except httpx.RequestError as e:
            LOGGER.warning(f"HTTP-Fehler bei der Verbindung zu Pushover für {user_key}: {e}")

   
    
