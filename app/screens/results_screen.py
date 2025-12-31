import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QScrollArea,
    QFrame,
    QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class ResultsWidget(QWidget):
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header (Back, Icon, Search, Theme)
        header = QHBoxLayout()

        self.back_btn = QPushButton("Back")
        self.back_btn.setObjectName("secondaryBtn")
        self.back_btn.setFixedWidth(80)
        self.back_btn.clicked.connect(self.go_back_home)

        # Small Icon
        icon_lbl = QLabel()
        base_path = Path(
            getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent)
        )
        icon_path = base_path / "app.png"
        if icon_path.exists():
            icon_lbl.setPixmap(
                QPixmap(str(icon_path)).scaled(
                    32,
                    32,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.returnPressed.connect(self.perform_search)

        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.perform_search)

        header.addWidget(self.back_btn)
        header.addWidget(icon_lbl)
        header.addWidget(self.search_input, 1)  # Expand
        header.addWidget(self.search_btn)

        layout.addLayout(header)

        # Results Area
        self.results_scroll = QScrollArea()
        self.results_scroll.setWidgetResizable(True)
        self.results_scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)
        self.results_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.results_layout.setSpacing(15)

        self.results_scroll.setWidget(self.results_widget)
        layout.addWidget(self.results_scroll)

    def go_back_home(self):
        self.parent_app.show_home()

    def perform_search(self):
        term = self.search_input.text().strip()
        if term:
            self.parent_app.execute_search(term)

    def clear_results(self):
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def add_result(self, result):
        title = result.get("title", "Unknown")
        url = result.get("url", "")

        card = QFrame()
        card.setObjectName("resultCard")
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 16px; font-weight: bold;")

        layout.addWidget(title_lbl)
        layout.addStretch()

        arrow_lbl = QLabel("→")
        arrow_lbl.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(arrow_lbl)

        card.mouseReleaseEvent = lambda e: self.parent_app.fetch_links(url, title)

        self.results_layout.addWidget(card)
