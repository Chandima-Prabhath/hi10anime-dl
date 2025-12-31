import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


def setup_logger():
    log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
    log_filepath = LOG_DIR / log_filename

    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
        handlers=[logging.FileHandler(log_filepath), logging.StreamHandler()],
    )

    cleanup_logs()


def cleanup_logs():
    now = datetime.now()
    seven_days_ago = now - timedelta(days=7)
    for f in LOG_DIR.glob("*.log"):
        file_path = os.path.join(LOG_DIR, f)
        file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
        if file_creation_time < seven_days_ago:
            os.remove(file_path)
