import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    encoding="utf-8"),

logger = logging.getLogger("my_log")
logger.info("Логер запущен")