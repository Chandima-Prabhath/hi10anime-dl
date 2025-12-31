import sys
from pathlib import Path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal, QSize
from PyQt6.QtGui import QIcon


class Sidebar(QWidget):
    """A navigation sidebar with icon-based buttons."""
    home_button_clicked = pyqtSignal()
    downloads_button_clicked = pyqtSignal()
    settings_button_clicked = pyqtSignal()
    theme_button_clicked = pyqtSignal()

    def __init__(self, parent=None):
        """Initializes the Sidebar."""
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 20, 10, 20)
        self.layout.setSpacing(15)

        base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent.parent))

        self.home_button = QPushButton()
        self.home_button.setIcon(QIcon(str(base_path / "app" / "icons" / "home-100.png")))
        self.home_button.setIconSize(QSize(32, 32))

        self.downloads_button = QPushButton()
        self.downloads_button.setIcon(QIcon(str(base_path / "app" / "icons" / "downloads-100.png")))
        self.downloads_button.setIconSize(QSize(32, 32))

        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon(str(base_path / "app" / "icons" / "settings-100.png")))
        self.settings_button.setIconSize(QSize(32, 32))

        self.theme_toggle_button = QPushButton()

        # Set object names for styling
        self.home_button.setObjectName("sidebarButton")
        self.downloads_button.setObjectName("sidebarButton")
        self.settings_button.setObjectName("sidebarButton")
        self.theme_toggle_button.setObjectName("sidebarButton")

        # Connect signals
        self.home_button.clicked.connect(self.home_button_clicked)
        self.downloads_button.clicked.connect(self.downloads_button_clicked)
        self.settings_button.clicked.connect(self.settings_button_clicked)
        self.theme_toggle_button.clicked.connect(self.theme_button_clicked)

        # Add to layout
        self.layout.addWidget(self.home_button)
        self.layout.addWidget(self.downloads_button)
        self.layout.addStretch()
        self.layout.addWidget(self.settings_button)
        self.layout.addWidget(self.theme_toggle_button)

        self.setObjectName("sidebar")

    def update_theme_icon(self, theme):
        """Updates the theme toggle button's icon based on the current theme."""
        base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent.parent))
        if theme == "Dark":
            icon_path = base_path / "app" / "icons" / "toggle-on-100.png"
        else:
            icon_path = base_path / "app" / "icons" / "toggle-off-100.png"

        if icon_path.exists():
            self.theme_toggle_button.setIcon(QIcon(str(icon_path)))
            self.theme_toggle_button.setIconSize(QSize(32, 32))
        else:
            # Fallback text if icon is missing
            self.theme_toggle_button.setText("T" if theme == "Dark" else "L")