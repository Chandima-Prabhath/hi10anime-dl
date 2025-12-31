import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from ..version import __version__
from ..widgets.theme_toggle import ThemeToggle
from ..widgets.update_banner import UpdateBanner


class HomeScreen(QWidget):
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Top Right Controls
        top_ctrl_layout = QHBoxLayout()
        top_ctrl_layout.addStretch()

        self.theme_toggle = ThemeToggle(self.parent_app.current_theme)
        self.theme_toggle.clicked.connect(self.parent_app.toggle_theme)
        top_ctrl_layout.addWidget(self.theme_toggle)

        layout.addLayout(top_ctrl_layout)
        layout.addStretch(1)

        # Hero Content
        hero_layout = QVBoxLayout()
        hero_layout.setSpacing(20)
        hero_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_label = QLabel()
        base_path = Path(
            getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent.parent)
        )
        logo_path = base_path / "app.png"
        if logo_path.exists():
            logo_label.setPixmap(
                QPixmap(str(logo_path)).scaled(
                    256,
                    256,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero_layout.addWidget(logo_label)

        ver_label = QLabel(f"v{__version__}")
        ver_label.setObjectName("versionLabel")
        ver_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero_layout.addWidget(ver_label)

        search_card = QFrame()
        search_card.setObjectName("heroSearchCard")
        search_card.setFixedWidth(600)

        search_layout = QHBoxLayout(search_card)
        search_layout.setContentsMargins(20, 20, 20, 20)

        self.home_search_input = QLineEdit()
        self.home_search_input.setPlaceholderText(
            "Search for anime... (e.g., 'One Piece')"
        )
        self.home_search_input.returnPressed.connect(self.perform_home_search)

        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.perform_home_search)
        search_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.use_proxy_checkbox = QCheckBox("Proxy")
        self.use_proxy_checkbox.setChecked(True)

        search_layout.addWidget(self.home_search_input)
        search_layout.addWidget(self.use_proxy_checkbox)
        search_layout.addWidget(search_btn)

        card_container = QWidget()
        card_layout = QHBoxLayout(card_container)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.addStretch()
        card_layout.addWidget(search_card)
        card_layout.addStretch()

        hero_layout.addWidget(card_container)

        layout.addLayout(hero_layout)
        layout.addStretch(1)

        self.update_banner = UpdateBanner()
        layout.addWidget(self.update_banner)

    def perform_home_search(self):
        term = self.home_search_input.text().strip()
        if not term:
            self.parent_app.toast.show_message("Please enter a search term!")
            return
        self.parent_app.execute_search(term)
