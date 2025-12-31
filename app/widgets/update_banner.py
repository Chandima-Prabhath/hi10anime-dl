import webbrowser
from PyQt6.QtWidgets import QFrame, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt


class UpdateBanner(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("updateBanner")
        self.hide()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        self.label = QLabel("New version available!")
        self.label.setObjectName("updateText")

        self.btn = QPushButton("View Update")
        self.btn.setObjectName("updateBtn")
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.clicked.connect(self.open_url)

        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.btn)

        self.url = ""

    def show_update(self, version, url):
        self.label.setText(f"Update Available: {version}")
        self.url = url
        self.show()

    def open_url(self):
        if self.url:
            webbrowser.open(self.url)
