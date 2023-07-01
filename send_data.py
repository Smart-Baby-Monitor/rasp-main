from data_transfer.send_data import DataTransafer
from utils import logger
import utils.utils as utils

logger.info("Starting data send")
DataTransafer.send_data()
logger.info("Finished sata send")