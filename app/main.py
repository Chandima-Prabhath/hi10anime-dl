import sys
import logging
from PyQt6.QtWidgets import QApplication
from .app import AnimeSearchApp
from .logger import setup_logger


def main():
    setup_logger()
    logging.info("Application started.")
    app = QApplication(sys.argv)
    window = AnimeSearchApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
