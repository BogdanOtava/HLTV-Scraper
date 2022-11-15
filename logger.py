import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

format = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%d-%m-%Y / %H:%M:%S")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(format)

logger.addHandler(stream_handler)