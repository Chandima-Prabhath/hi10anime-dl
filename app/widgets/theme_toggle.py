import sys
from pathlib import Path
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon


class ThemeToggle(QPushButton):
    def __init__(self, current_theme="Dark", parent=None):
        super().__init__(parent)
        self.setObjectName("themeToggle")
        self.setFixedSize(40, 40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setIconSize(QSize(28, 28))  # Updated size
        self.update_icon(current_theme)

    def update_icon(self, theme):
        base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
        icon_dir = base_path / "icons"

        if theme == "Dark":
            icon_path = icon_dir / "toggle-on-100.png"
        else:
            icon_path = icon_dir / "toggle-off-100.png"

        if icon_path.exists():
            self.setIcon(QIcon(str(icon_path)))
        else:
            self.setText("T")
