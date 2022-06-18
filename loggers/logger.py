import logging.config
import os
from pathlib import Path


parent_file = Path(__file__).parent
log_file = parent_file / "logging.ini"


logging.config.fileConfig(log_file, disable_existing_loggers=False)
log = logging.getLogger(__name__)

log.debug("DEBUG message")
log.info("INFO message")
log.warning("WARNING message")
log.error("ERROR message")
log.critical("CRITICAL message")
