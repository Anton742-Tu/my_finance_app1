import logging
from .models.operations import Operation
from .services.data_processor import get_transactions

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
