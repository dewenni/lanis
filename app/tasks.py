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

def _task_key(task):
    """Erzeugt einen stabilen Schlüssel, mit dem Aufgaben eindeutig verglichen werden."""
    task_date = getattr(task, 'date', None)
    if isinstance(task_date, datetime):
        normalized_date = task_date.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(task_date, str):
        try:
            normalized_date = datetime.strptime(task_date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            normalized_date = task_date
    else:
        normalized_date = ''

    return (
        getattr(task, 'title', None),
        normalized_date,
        getattr(task, 'subject_name', None),
    )


def get_new_tasks(current_tasks, last_tasks):
    """Gibt nur die Aufgaben zurück, die seit dem letzten Lauf neu hinzugekommen sind."""
    last_task_keys = {
        (
            last_task.get('title'),
            last_task.get('date'),
            last_task.get('subject_name'),
        )
        for last_task in last_tasks
    }

    return [
        task for task in current_tasks
        if _task_key(task) not in last_task_keys
    ]


def has_new_tasks(current_tasks, last_tasks):
    """Prüft, ob neue Aufgaben seit dem letzten Lauf hinzugekommen sind."""
    return bool(get_new_tasks(current_tasks, last_tasks))


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



