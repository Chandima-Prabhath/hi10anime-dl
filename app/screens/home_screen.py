import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon, QFontDatabase
from ..widgets.update_banner import UpdateBanner

# A custom card widget for the home screen
class QuickCard(QFrame):
    """A clickable card widget for the home screen."""
    clicked = pyqtSignal()

    def __init__(self, icon_char, title, description, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("quickCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        icon_label = QLabel(icon_char)
        icon_label.setObjectName("quickCardIcon")
        layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setObjectName("quickCardTitle")
        layout.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setObjectName("quickCardDesc")
        layout.addWidget(desc_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class HomeScreen(QWidget):
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        self.setObjectName("homeScreen")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top Navigation Bar
        top_nav = self._create_top_nav()
        main_layout.addWidget(top_nav)

        # 2. Main Content Area
        main_area = self._create_main_area()
        main_layout.addWidget(main_area, 1) # Add stretch factor

        # 3. Update Banner
        self.update_banner = UpdateBanner()
        main_layout.addWidget(self.update_banner)

    def _create_top_nav(self):
        """Creates the top navigation bar with search and window controls."""
        nav_widget = QFrame()
        nav_widget.setObjectName("topNav")
        nav_layout = QHBoxLayout(nav_widget)
        nav_layout.setContentsMargins(24, 0, 24, 0)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search anime titles...")
        self.search_input.setObjectName("modernInput")
        self.search_input.returnPressed.connect(self.perform_search)

        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0,0,0,0)
        search_layout.addWidget(self.search_input)

        nav_layout.addWidget(search_container)

        return nav_widget

    def _create_main_area(self):
        """Creates the central content area with logo, text, and cards."""
        area_widget = QWidget()
        area_layout = QVBoxLayout(area_widget)
        area_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        area_layout.setSpacing(32)

        # Logo
        logo_label = QLabel()
        base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent.parent))
        logo_path = base_path / "app.png"
        if logo_path.exists():
            pixmap = QPixmap(str(logo_path)).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Welcome Text
        welcome_title = QLabel("Hi10Anime DL")
        welcome_title.setObjectName("welcomeTitle")
        welcome_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        welcome_subtitle = QLabel("Search, organize, and download your favorite anime.")
        welcome_subtitle.setObjectName("welcomeSubtitle")
        welcome_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Quick Cards
        cards_widget = QWidget()
        cards_layout = QHBoxLayout(cards_widget)
        cards_layout.setSpacing(16)

        card1 = QuickCard("🔍", "Search Anime", "Find new series to watch")
        card1.clicked.connect(self.focus_search)

        card2 = QuickCard("🕒", "Recent", "View your history")

        card3 = QuickCard("🌐", "Proxy Status", "Direct Connection")

        cards_layout.addWidget(card1)
        cards_layout.addWidget(card2)
        cards_layout.addWidget(card3)

        area_layout.addStretch(1)
        area_layout.addWidget(logo_label)
        area_layout.addWidget(welcome_title)
        area_layout.addWidget(welcome_subtitle)
        area_layout.addWidget(cards_widget)
        area_layout.addStretch(2)

        return area_widget

    def focus_search(self):
        """Focuses the search input field."""
        self.search_input.setFocus()

    def perform_search(self):
        """Executes a search based on the input text."""
        term = self.search_input.text().strip()
        if not term:
            self.parent_app.toast.show_message("Please enter a search term!")
            return
        self.parent_app.execute_search(term)
