import logging
import sys

def setup_logger():

    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
    
    logger = logging.getLogger('LanisAPP')
    logger.setLevel(logging.INFO)

    return logger

# Logger initialisieren
LANISLOG = setup_logger()