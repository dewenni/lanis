import sys
import os
import httpx
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib')))

from calendar import *
from pushover import *
from tasks import *
from conversation import *
from calendar_ics import *
from lanisapi import LanisClient, LanisAccount, LanisCookie, School
from config import LANIS_SCHOOL, LANIS_USER, LANIS_PASSWORD, OPT_TASKS, OPT_CONVERSATION, OPT_CALENDAR, CALENDAR_START_DATE, CALENDAR_END_DATE

# Lese den Intervallwert aus der Umgebungsvariable und wandle ihn in eine Ganzzahl um
INTERVAL = int(os.getenv('INTERVAL', 3600))  # Standardwert ist 3600 Sekunden, wenn die Variable nicht gesetzt ist

LOGGER = logging.getLogger("LanisAPP")

def main():
    
    # LANIS-Client erstellen
    client = LanisClient(LanisAccount(LANIS_SCHOOL, LANIS_USER, LANIS_PASSWORD))

    while True:
        retries = 3  # Maximale Anzahl der Versuche
        for attempt in range(retries):
            try:
                # Erstelle einen neuen HTTP-Client für jede Iteration
                with httpx.Client() as http_client:
                    
                    # authentifizieren 
                    client.authenticate()

                    #------------------------------------------------------------------------------------------------
                    # Prüfe auf unerledigte Hausaufgaben und sende Pushover Nachricht
                    #------------------------------------------------------------------------------------------------

                    if OPT_TASKS:
                        
                        current_tasks = client.get_tasks()
                        last_tasks = load_last_tasks()

                        # Prüfen, ob es neue Aufgaben gibt
                        if has_new_tasks(current_tasks, last_tasks):
                            formattedTasks = formatTasks(current_tasks)
                            sendPushover("unerledigte Hausaufgaben", formattedTasks)
                            LOGGER.info("neue Aufgaben gefunden %s", formattedTasks)
                            # Aktualisiere die zwischengespeicherten Aufgaben
                            save_last_tasks(current_tasks)
                        else:
                            LOGGER.info("Keine neuen Aufgaben gefunden.")

                    
                    #------------------------------------------------------------------------------------------------
                    # Prüfen, ob neue Nachricht vorliegt und sende Pushover Nachricht
                    #------------------------------------------------------------------------------------------------

                    if OPT_CONVERSATION:
                    
                        # Abruf der aktuellen Konversationen
                        current_conversations = client.get_conversations(-1)

                        # Laden der zuletzt gespeicherten Konversationen
                        last_conversations = load_last_conversations()

                        # Prüfen, ob es neue Konversationen gibt
                        if has_new_conversations(current_conversations, last_conversations):
                            # Falls ja, formatiere und sende eine Nachricht
                            formatted_conversations = formatConversations(current_conversations)
                            sendPushover("aktuelle Nachtichten", formatted_conversations)
                            LOGGER.info("aktuelle Nachtichten %s", formatted_conversations)
                            # Aktualisiere die zwischengespeicherten Konversationen
                            save_last_conversations(current_conversations)
                        else:
                            LOGGER.info("Keine neuen Konversationen gefunden.")

                    #------------------------------------------------------------------------------------------------

                    if OPT_CALENDAR:
                    
                        filtered_events = filter_calendar_entries(client.get_calendar(CALENDAR_START_DATE, CALENDAR_END_DATE, True))
                        new_events = create_and_compare_events(filtered_events)
                        
                        # Überprüfe, ob new_events Einträge enthält
                        if new_events:
                            sendPushover("Neue Kalendereinträge", new_events)
                            LOGGER.info("Neue Kalendereinträge: %s", new_events)

                        else:
                            LOGGER.info("Keine neuen Kalendereinträge gefunden.")

                # Wenn erfolgreich, dann Schleife beenden
                break

            except httpx.RequestError as e:
                LOGGER.warning(f"Versuch {attempt + 1} fehlgeschlagen: {e}")
                if attempt < retries - 1:
                    LOGGER.info("Versuche es in 10 Sekunden erneut...")
                    time.sleep(10)  # Warte 10 Sekunden, bevor du es erneut versuchst
                else:
                    LOGGER.error("Maximale Anzahl an Versuchen erreicht. Warte auf das nächste Intervall.")

            except Exception as e:
                LOGGER.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
                break  # Bei unerwarteten Fehlern Schleife verlassen

        LOGGER.info("Warte %i Sekunden bis zum nächsten Durchlauf...", INTERVAL)
        time.sleep(INTERVAL)  # Warte das angegebene Intervall


if __name__ == "__main__":
    main()
