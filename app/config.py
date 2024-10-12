import configparser
import os
import shutil
import sys

config = configparser.ConfigParser()

# Absoluter Pfad relativ zum aktuellen Skript
config_path = os.path.join(os.path.dirname(__file__), 'config/config.ini')
config.read(config_path)


def get_bool_option(param, value):
    res = config.getboolean(param, value)
    return res


LANIS_SCHOOL = config['lanis']['school']
LANIS_USER = config['lanis']['username']
LANIS_PASSWORD = config['lanis']['password']

PUSHOVER_API = config['pushover']['api_token']
PUSHOVER_USER = config['pushover']['user_key']

OPT_TASKS = get_bool_option("options", "tasks")
OPT_CONVERSATION = get_bool_option("options", "conversations")
OPT_CALENDAR = get_bool_option("options", "calendar")

# Lese Kategorien und Schlüsselwörter aus der Konfiguration
CALENDAR_CATEGORIES = config.get('calendar', 'filter_categories').split(',')
CALENDAR_KEYWORDS = config.get('calendar', 'filter_keywords').split(',')

