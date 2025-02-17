import time
import json
import os
import logging
from datetime import datetime
from lanis_log import LANISLOG

TASKS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'output', 'last_tasks.json')

def load_last_tasks():
    """Lädt die zwischengespeicherten Aufgaben aus der Datei."""
    try:
        with open(TASKS_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # Wenn die Datei nicht existiert, wird eine leere Liste zurückgegeben
        LANISLOG.warning("Task file not found: %s", TASKS_FILE_PATH)
        return []

def save_last_tasks(tasks):
    """Speichert die Aufgaben als JSON in einer Datei."""
    with open(TASKS_FILE_PATH, 'w') as file:
        # Konvertiert die Task-Objekte zu einem speicherbaren Format (z.B. Dictionaries)
        json.dump([task.__dict__ for task in tasks], file, default=str, indent=4)

def has_new_tasks(current_tasks, last_tasks):
    """Vergleicht die aktuellen Aufgaben mit den zuletzt gespeicherten Aufgaben."""
    if len(current_tasks) != len(last_tasks):
        return True

    # Vergleiche die Titel, Daten und Fächer der Aufgaben
    for current_task, last_task in zip(current_tasks, last_tasks):
        
        date_string = last_task.get('date')
        if date_string is None:
            continue

        # Konvertiere das gespeicherte Datum (String) in ein datetime-Objekt
        last_task_date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        
        if (current_task.title != last_task.get('title') or 
            current_task.date != last_task_date or
            current_task.subject_name != last_task.get('subject_name')):
            return True

    return False


def formatTasks(tasks):
    # Prüfen, ob eine Liste von Aufgaben übergeben wurde
    if not isinstance(tasks, list):
        raise TypeError("Erwartet eine Liste von Aufgaben.")

    formatted_tasks = []

    for task in tasks:
        # Extrahiere die Daten aus dem Task-Objekt (sofern vorhanden)
        try:
            task_data = {
                'title': task.title,
                'date': task.date.strftime('%d.%m.%Y'),
                'subject_name': task.subject_name,
                'teacher': task.teacher,
                'description': task.description,
                'attachments': task.attachment  # Anhänge hinzufügen
            }
            
            # Formatiere die Aufgabe für die Ausgabe
            formatted_task = (f"Fach: {task_data['subject_name']}\n"
                              f"Lehrer: {task_data['teacher']}\n"
                              f"Datum: {task_data['date']}\n"
                              f"Titel: {task_data['title']}\n"
                              f"Beschreibung: {task_data['description']}")
            
            # Falls Anhänge vorhanden sind, füge die Namen hinzu
            if task_data['attachments']:
                formatted_task += "\nAnhänge:\n" + "\n".join(f"- {attachment}" for attachment in task_data['attachments'])

            formatted_tasks.append(formatted_task)
        
        except AttributeError:
            # Falls ein Attribut fehlt, überspringe diese Aufgabe
            continue

    # Kombiniere alle formatierten Aufgaben in einem String
    return "\n\n".join(formatted_tasks)



