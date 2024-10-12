import requests
from config import PUSHOVER_API, PUSHOVER_USER

def sendPushover(title, message):

    # Daten für den API-Request
    data = {
        "title": title,
        "token": PUSHOVER_API,
        "user": PUSHOVER_USER,
        "message": message,
    }

    # HTTP POST-Anfrage an die Pushover API
    response = requests.post("https://api.pushover.net/1/messages.json", data=data)

    # Überprüfe, ob die Nachricht erfolgreich gesendet wurde
    if response.status_code == 200:
        print("Nachricht erfolgreich gesendet!")
    else:
        print(f"Fehler beim Senden der Nachricht: {response.status_code}")
