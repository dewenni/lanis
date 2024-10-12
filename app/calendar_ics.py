import re
import os

from datetime import datetime
from ics import Calendar, Event
from config import CALENDAR_CATEGORIES, CALENDAR_KEYWORDS

#CALENDAR_FILE_PATH = 'output/lanis_calendar.ics'
CALENDAR_FILE_PATH = os.path.join(os.path.dirname(__file__), 'output', 'lanis_calendar.ics')

def filter_events_by_work(calendar):
    filtered_events = []
    
    for event in calendar.events:
        if "Arbeit" in event.title:
            filtered_events.append({
                "Datum": event.start.date(),
                "Titel": event.title,
                "Start": event.start.strftime("%Y-%m-%d %H:%M"),
                "Ende": event.end.strftime("%Y-%m-%d %H:%M")
            })
    
    return filtered_events

from datetime import datetime
import json

def filter_calendar_entries(calendar):
    filtered_entries = []

    # Durchlaufe die Events in den Kalenderdaten
    filtered_entries = []  # Stelle sicher, dass du die Liste hier initialisierst
    for event in calendar.events:
        # Überprüfen, ob die Kategorie in der Liste der Kategorien ist oder der Titel ein Schlüsselwort enthält
        if event['category'] in CALENDAR_CATEGORIES or any(keyword in event['title'] for keyword in CALENDAR_KEYWORDS):
            # Füge die relevanten Informationen in ein Dictionary ein
            filtered_entry = {
                'title': event['title'],
                'description': event['description'],
                'allDay': event['allDay'],
                'start': event['start'],
                'end': event['end']
            }
            filtered_entries.append(filtered_entry)

    return filtered_entries


def create_ics_file(filtered_entries):
    """
    Create an ICS file from the filtered calendar entries.

    Parameters
    ----------
    filtered_entries : list
        A list of filtered calendar entries to write to the ICS file.
    filename : str, default 'calendar.ics'
        The name of the ICS file to create.
    """
    calendar = Calendar()

    # Durchlaufe die gefilterten Einträge und füge sie dem Kalender hinzu
    for entry in filtered_entries:
        event = Event()
        event.name = entry['title']
        event.begin = entry['start']
        event.end = entry['end']
        event.description = entry['description']

        # Überprüfe, ob es sich um einen ganztägigen Termin handelt
        if entry['allDay']:
            event.make_all_day()

        calendar.events.add(event)

    # Schreibe den Kalender in die ICS-Datei
    with open(CALENDAR_FILE_PATH, 'w') as f:
        f.writelines(calendar)

    print(f'ICS file created: {CALENDAR_FILE_PATH}')




