import re
import os
import json
import logging

from datetime import datetime
from ics import Calendar, Event
from config import CALENDAR_CATEGORIES, CALENDAR_KEYWORDS
from lanis_log import LANISLOG

ALL_EVENTS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'output', 'lanis_all_events.ics')
NEW_EVENTS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'output', 'lanis_new_events.ics')
EVENTS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'output', 'last_events.json')

def filter_calendar_entries(calendar):
    filtered_entries = []

    # Durchlaufe die Events in den Kalenderdaten
    filtered_entries = []  # Stelle sicher, dass du die Liste hier initialisierst
    for event in calendar.events:
        # Überprüfen, ob die Kategorie in der Liste der Kategorien ist oder der Titel ein Schlüsselwort enthält
        if event['category'] in CALENDAR_CATEGORIES or any(keyword in event['title'] for keyword in CALENDAR_KEYWORDS):
            # Füge die relevanten Informationen in ein Dictionary ein
            filtered_entry = {
                'Id': event['Id'],
                'title': event['title'],
                'description': event['description'],
                'allDay': event['allDay'],
                'start': event['start'],
                'end': event['end']
            }
            filtered_entries.append(filtered_entry)

    return filtered_entries


def load_last_events():
    """Lädt die zwischengespeicherten Events aus der Datei."""
    try:
        with open(EVENTS_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # Wenn die Datei nicht existiert, wird eine leere Liste zurückgegeben
        return []

def save_last_events(events):
    """Speichert die aktuellen Events als JSON in einer Datei."""
    with open(EVENTS_FILE_PATH, 'w') as file:
        # Speichere die Events als Liste von Dictionaries
        json.dump(events, file, indent=4)

def has_new_events(current_events, last_events):
    """Überprüft, ob es neue Events basierend auf den Event-IDs gibt."""
    current_ids = {event['Id'] for event in current_events}
    last_ids = {event['Id'] for event in last_events}
    
    # Gib nur die neuen Events zurück
    return [event for event in current_events if event['Id'] not in last_ids]

def format_events(events):
    """Formatiert die neuen Events für die Ausgabe per Pushover."""
    formatted_events = []
    
    for event in events:
        start_time = datetime.strptime(event['start'], '%Y-%m-%dT%H:%M:%S%z')
        end_time = datetime.strptime(event['end'], '%Y-%m-%dT%H:%M:%S%z')
        
        formatted_event = (f"Neuer Termin: {event['title']}\n"
                           f"Beginn: {start_time.strftime('%d.%m.%Y %H:%M')}\n"
                           f"Ende: {end_time.strftime('%d.%m.%Y %H:%M')}\n"
                           f"Beschreibung: {event['description']}\n")
        formatted_events.append(formatted_event)

    return "\n\n".join(formatted_events)

def create_and_compare_events(filtered_entries):
    """Erstellt die ICS-Datei und gibt neue Events zurück."""
    # Lade die letzten gespeicherten Events
    last_events = load_last_events()

    # Finde die neuen Events
    new_events = has_new_events(filtered_entries, last_events)

    # Überprüfe, ob new_events Einträge enthält
    if new_events:
        # Aktualisieren und erstelle neue ics Dateien
        create_ics_file(filtered_entries, new_events)

    # Aktualisiere die last_events.json mit den aktuellen Events
    save_last_events(filtered_entries)

    # Formatierte Ausgabe der neuen Events für Pushover
    formatted_new_events = format_events(new_events)
    
    return formatted_new_events


def create_ics_file(filtered_entries, new_entries):
    # Kalender für alle Einträge erstellen
    all_events_calendar = Calendar()

    # Kalender für neue Einträge erstellen
    new_events_calendar = Calendar()

    # Alle Einträge dem Kalender hinzufügen
    for entry in filtered_entries:
        event = Event()
        event.name = entry['title']
        event.begin = entry['start']
        event.end = entry['end']
        event.description = entry['description']

        if entry['allDay']:
            event.make_all_day()

        # Füge das Event dem Kalender für alle Einträge hinzu
        all_events_calendar.events.add(event)

        # Wenn das Event neu ist, füge es auch dem Kalender für neue Einträge hinzu
        if entry['Id'] in [e['Id'] for e in new_entries]:
            new_events_calendar.events.add(event)

    # Schreibe den Kalender für alle Events in die ICS-Datei
    with open(ALL_EVENTS_FILE_PATH, 'w') as f:
        f.writelines(all_events_calendar)

    LANISLOG.info('ics Datei mit allen Einträgen erstellt: %s', ALL_EVENTS_FILE_PATH)

    # Schreibe den Kalender für nur neue Events in die ICS-Datei
    with open(NEW_EVENTS_FILE_PATH, 'w') as f:
        f.writelines(new_events_calendar)

    LANISLOG.info('ics Datei mit neuen Einträgen erstellt: %s', NEW_EVENTS_FILE_PATH)