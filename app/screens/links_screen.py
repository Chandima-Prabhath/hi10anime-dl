from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QScrollArea,
    QTabWidget,
    QApplication,
)
from PyQt6.QtCore import Qt
from ..parser import LinkParser
from ..widgets.collapsible_box import CollapsibleBox
from ..widgets.quality_tab import QualityTab


class LinksWidget(QWidget):
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        self.setup_ui()
        self.collapsibles = []

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Top Bar
        top_bar = QHBoxLayout()

        self.back_btn = QPushButton("Back")
        self.back_btn.setObjectName("secondaryBtn")
        self.back_btn.setFixedWidth(100)
        self.back_btn.clicked.connect(self.go_back)

        self.title_lbl = QLabel("Anime Title")
        self.title_lbl.setObjectName("subTitle")
        self.title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Tools
        tools_layout = QHBoxLayout()
        tools_layout.setSpacing(5)

        expand_btn = QPushButton("Expand All")
        expand_btn.setObjectName("ghostBtn")
        expand_btn.clicked.connect(lambda: self.toggle_all(True))

        collapse_btn = QPushButton("Collapse All")
        collapse_btn.setObjectName("ghostBtn")
        collapse_btn.clicked.connect(lambda: self.toggle_all(False))

        copy_all_btn = QPushButton("Copy ALL Links")
        copy_all_btn.clicked.connect(self.copy_all)

        tools_layout.addWidget(expand_btn)
        tools_layout.addWidget(collapse_btn)
        tools_layout.addWidget(copy_all_btn)

        top_bar.addWidget(self.back_btn)
        top_bar.addWidget(self.title_lbl, 1)
        top_bar.addLayout(tools_layout)

        layout.addLayout(top_bar)

        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(15)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll.setWidget(self.content_widget)
        layout.addWidget(self.scroll)

    def setup_links(self, title, links):
        self.title_lbl.setText(title)

        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.collapsibles = []
        categorized = LinkParser.parse(links)
        self.all_links = []

        for season, qualities in categorized.items():
            season_box = CollapsibleBox(f"  {season}  ")
            season_box.set_header_style("collageHeader")
            season_box.toggle_button.setObjectName("collageHeader")
            self.collapsibles.append(season_box)

            tabs = QTabWidget()
            tabs.setDocumentMode(True)

            for quality, episodes in qualities.items():
                for ep in episodes:
                    self.all_links.append(ep["link"])

                tab_content = QualityTab(quality, episodes, self)
                tabs.addTab(tab_content, quality)

            season_box.add_widget(tabs)
            self.content_layout.addWidget(season_box)

    def toggle_all(self, state):
        for box in self.collapsibles:
            box.toggle(state)

    def go_back(self):
        self.parent_app.stack.setCurrentWidget(self.parent_app.results_screen)

    def show_toast(self, msg):
        self.parent_app.toast.show_message(msg)

    def copy_list(self, links):
        cb = QApplication.clipboard()
        cb.setText("\\n".join(links))
        self.show_toast(f"Copied {len(links)} links!")

    def copy_all(self):
        if self.all_links:
            self.copy_list(self.all_links)
        else:
            self.show_toast("No links available.")
