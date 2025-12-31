import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

if getattr(sys, "frozen", False):
    # The application is running as a bundled executable
    BASE_DIR = Path(sys.executable).parent
else:
    # The application is running in a normal Python environment
    BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"


def setup_logger():
    try:
        LOG_DIR.mkdir(exist_ok=True)
        log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
        log_filepath = LOG_DIR / log_filename

        file_handler = logging.FileHandler(log_filepath)
        handlers = [file_handler, logging.StreamHandler()]

        logging.basicConfig(
            level=logging.DEBUG,
            format="[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
            handlers=handlers,
        )

        cleanup_logs()
        return True  # Indicate success
    except PermissionError:
        # Fallback to console-only logging if file permissions fail
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
            handlers=[logging.StreamHandler()],
        )
        logging.warning("Permission denied to create log file. Logging to console only.")
        return False  # Indicate failure


def cleanup_logs():
    now = datetime.now()
    seven_days_ago = now - timedelta(days=7)
    for f in LOG_DIR.glob("*.log"):
        file_path = os.path.join(LOG_DIR, f)
        file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
        if file_creation_time < seven_days_ago:
            os.remove(file_path)
