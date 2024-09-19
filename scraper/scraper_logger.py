import logging

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("scraper.log", mode="a", encoding="utf-8")

logger.addHandler(console_handler)
logger.addHandler(file_handler)
formatter = logging.Formatter(
    "{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.setLevel("ERROR")
