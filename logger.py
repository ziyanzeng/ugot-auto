import logging
import os
from datetime import datetime

# Logger configuration
LOGS_DIR = "log"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Create a new log file with a timestamp
log_filename = datetime.now().strftime("log_%Y%m%d_%H%M%S.log")
log_filepath = os.path.join(LOGS_DIR, log_filename)

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create file handler which logs even debug messages
fh = logging.FileHandler(log_filepath)
fh.setLevel(logging.INFO)

# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('Logger initialized')
