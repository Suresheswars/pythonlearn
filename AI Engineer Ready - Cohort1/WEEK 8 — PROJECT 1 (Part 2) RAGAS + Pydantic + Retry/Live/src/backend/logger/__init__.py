# logger/__init__.py
from .customer_logger import CustomLogger



# Create a single shared logger instance
GLOBAL_LOGGER = CustomLogger().get_logger("multi_document_assist")