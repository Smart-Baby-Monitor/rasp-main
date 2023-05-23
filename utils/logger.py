import logging
import env
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename= env.logs_folder +"/logs.log"
)

# Create a logger instance
logger = logging.getLogger(__name__)

# Log an informational message
def info(message):
    logger.info(message)

def error(message):
   logger.error(message)

def warning(messaage):
    logger.warning(messaage)

def debug(message):
    logger.debug(message)

def critical(message):
    logger.critical(message)

def exception(message):
    logger.exception(message)
