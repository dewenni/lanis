import logging
import sys

def setup_logger():
    logger = logging.getLogger('LanisAPP')
    logger.setLevel(logging.INFO)

    return logger

# Logger initialisieren
LANISLOG = setup_logger()