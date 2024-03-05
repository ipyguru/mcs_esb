import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Создаем папку logs, если она не существует
logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Настройка логгирования
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)

# Определяем имя файла с помощью текущей даты и времени
current_time = datetime.now().strftime("%Y-%m")
log_file = os.path.join(logs_dir, f"rabbitmq_{current_time}.log")

# Создаем RotatingFileHandler с новым именем файла
handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
logger.addHandler(handler)
