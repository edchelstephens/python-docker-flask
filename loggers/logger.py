import logging

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)
log.debug("DEBUG message")
log.info("INFO message")
log.warning("WARNING message")
log.error("ERROR message")
log.critical("CRITICAL message")
