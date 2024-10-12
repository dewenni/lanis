import sys
import os
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib')))

from calendar import *
from pushover import *
from tasks import *
from conversation import *
from calendar_ics import *
from lanisapi import LanisClient, LanisAccount, LanisCookie, School
from config import LANIS_SCHOOL, LANIS_USER, LANIS_PASSWORD, OPT_TASKS, OPT_CONVERSATION, OPT_CALENDAR

# Lese den Intervallwert aus der Umgebungsvariable und wandle ihn in eine Ganzzahl um
INTERVAL = int(os.getenv('INTERVAL', 3600))  # Standardwert ist 3600 Sekunden, wenn die Variable nicht gesetzt ist


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
                        # Prüfe auf neue Hausaufgaben
                        current_tasks = client.get_tasks()
                        print(len(current_tasks))

                        # Laden der zuletzt gespeicherten Aufgaben
                        last_tasks = load_last_tasks()
                        print(len(last_tasks))

                        # Prüfen, ob es neue Aufgaben gibt
                        if has_new_tasks(current_tasks, last_tasks):
                            formattedTasks = formatTasks(current_tasks)
                            sendPushover("unerledigte Hausaufgaben", formattedTasks)
                            print(formattedTasks)
                            # Aktualisiere die zwischengespeicherten Aufgaben
                            save_last_tasks(current_tasks)
                        else:
                            print(f"[{datetime.now()}] Keine neuen Aufgaben gefunden.")

                    
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

                            # Aktualisiere die zwischengespeicherten Konversationen
                            save_last_conversations(current_conversations)
                        else:
                            print(f"[{datetime.now()}] Keine neuen Konversationen gefunden.")

                    #------------------------------------------------------------------------------------------------

                    if OPT_CALENDAR:
                        start_date = datetime(2024, 10, 2, 0, 0, 0) 
                        end_date = datetime(2025, 10, 2, 0, 0, 0)   
                        # filtere Events
                        filtered_events = filter_calendar_entries(client.get_calendar(start_date, end_date, True))
                        # Exportiere die gefilterten Events in eine .ics Datei
                        create_ics_file(filtered_events)
                        print("Kalender aktualisiert")

                # Wenn erfolgreich, dann Schleife beenden
                break

            except httpx.RequestError as e:
                print(f"Versuch {attempt + 1} fehlgeschlagen: {e}")
                if attempt < retries - 1:
                    print("Versuche es in 10 Sekunden erneut...")
                    time.sleep(10)  # Warte 10 Sekunden, bevor du es erneut versuchst
                else:
                    print("Maximale Anzahl an Versuchen erreicht. Warte auf das nächste Intervall.")

            except Exception as e:
                print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
                break  # Bei unerwarteten Fehlern Schleife verlassen

        print(f"Warte {INTERVAL} Sekunden bis zum nächsten Durchlauf...")
        time.sleep(INTERVAL)  # Warte das angegebene Intervall


if __name__ == "__main__":
    main()
