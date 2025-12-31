import sys
import logging
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from PyQt6.QtWidgets import QApplication, QMessageBox
from app.app import AnimeSearchApp
from app.logger import setup_logger


def main():
    app = QApplication(sys.argv)

    if not setup_logger():
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Icon.Warning)
        error_box.setText("Permission Error")
        error_box.setInformativeText(
            "Could not create the logs directory. "
            "Please run the application as an administrator for logging to work."
        )
        error_box.setWindowTitle("Logging Error")
        error_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_box.exec()

    logging.info("Application started.")
    window = AnimeSearchApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
