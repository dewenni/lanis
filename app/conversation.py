import json
import os
from datetime import datetime

CONVERSATIONS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'output', 'last_conversations.json')

def load_last_conversations():
    """Lädt die zwischengespeicherten Konversationen aus der Datei."""
    try:
        with open(CONVERSATIONS_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # Wenn die Datei nicht existiert, wird eine leere Liste zurückgegeben
        return []

def save_last_conversations(conversations):
    """Speichert die Konversationen als JSON in einer Datei."""
    with open(CONVERSATIONS_FILE_PATH, 'w') as file:
        # Speichere die Konversationen als Liste von Dictionaries
        json.dump([{
            'id': conv.id,
            'title': conv.title,
            'teacher': conv.teacher,
            'creation_date': conv.creation_date.strftime('%Y-%m-%d %H:%M:%S'),
            'newest_date': conv.newest_date.strftime('%Y-%m-%d %H:%M:%S'),
            'unread': conv.unread,
            'special_receivers': conv.special_receivers,
            'receivers': conv.receivers,
            'content': conv.content
        } for conv in conversations], file, indent=4)

def has_new_conversations(current_conversations, last_conversations):
    """Überprüft, ob es neue Konversationen basierend auf den IDs gibt."""
    current_ids = {conv.id for conv in current_conversations}
    last_ids = {conv['id'] for conv in last_conversations}

    return not current_ids.issubset(last_ids)


def formatConversations(conversations):
    """Formatiert die Konversationen für die Ausgabe."""
    formatted_conversations = []
    
    for conv in conversations:
        formatted_conv = (f"Titel: {conv.title}\n"
                          f"Lehrer: {conv.teacher}\n"
                          f"Erstellt am: {conv.creation_date.strftime('%d.%m.%Y')}\n"
                          f"Inhalt: {conv.content}\n")
        formatted_conversations.append(formatted_conv)

    return "\n\n".join(formatted_conversations)
