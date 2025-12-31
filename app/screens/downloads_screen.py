from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class DownloadsScreen(QWidget):
    """A screen to display the downloads queue. Currently a placeholder."""
    def __init__(self, parent=None):
        """Initializes the DownloadsScreen."""
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Downloads - Under Development")
        font = self.label.font()
        font.setPointSize(24)
        self.label.setFont(font)

        self.layout.addWidget(self.label)
