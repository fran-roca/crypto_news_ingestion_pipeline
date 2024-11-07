import logging
import os
from src.config.settings import get_settings  # Adjust import based on your structure

def setup_logging(log_level=None):
    # Fetch settings
    settings = get_settings()

    # Determine the log level
    if log_level is None:
        log_level = os.getenv('LOG_LEVEL', 'INFO')

    # Define the basic log format
    log_format = '%(asctime)s %(levelname)s:%(message)s'

    # Set up the configuration parameters
    config_params = {
        'level': getattr(logging, log_level.upper()),
        'format': log_format,
        'force': True  # Ensures existing handlers are replaced
    }

    # Add the appropriate handler based on LOG_TO_FILE setting
    if settings.LOG_TO_FILE:
        config_params['filename'] = 'ingestion.log'
    else:
        config_params['handlers'] = [logging.StreamHandler()]

    # Pass the configuration parameters to basicConfig
    logging.basicConfig(**config_params)
