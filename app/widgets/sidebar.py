from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal

class Sidebar(QWidget):
    """A navigation sidebar with buttons to switch between different views."""
    home_button_clicked = pyqtSignal()
    downloads_button_clicked = pyqtSignal()
    settings_button_clicked = pyqtSignal()
    theme_button_clicked = pyqtSignal()

    def __init__(self, parent=None):
        """Initializes the Sidebar."""
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        self.home_button = QPushButton("Home")
        self.downloads_button = QPushButton("Downloads")
        self.settings_button = QPushButton("Settings")
        self.theme_toggle_button = QPushButton("Toggle Theme")

        self.home_button.clicked.connect(self.home_button_clicked)
        self.downloads_button.clicked.connect(self.downloads_button_clicked)
        self.settings_button.clicked.connect(self.settings_button_clicked)
        self.theme_toggle_button.clicked.connect(self.theme_button_clicked)

        self.layout.addWidget(self.home_button)
        self.layout.addWidget(self.downloads_button)
        self.layout.addWidget(self.settings_button)
        self.layout.addStretch()
        self.layout.addWidget(self.theme_toggle_button)

        self.setObjectName("sidebar")
