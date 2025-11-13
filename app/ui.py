from PyQt6.QtWidgets import QApplication, QStackedWidget, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, QScrollArea, QTreeWidget, QTreeWidgetItem, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import sys
from pathlib import Path
import webbrowser
import darkdetect

from .client import Hi10AnimeClient
from .proxy import ProxyService
from .parser import LinkParser
from typing import Set, Dict


class AnimeSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hi10Anime  DL")
        self.setGeometry(100, 100, 900, 700)
        # Resolve icon path relative to the executable or project root.
        # When bundled by PyInstaller, resources are in sys._MEIPASS.
        base_path = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent.parent))
        icon_path = base_path / 'app.ico'
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self.default_theme = "Dark" if darkdetect.isDark() else "Light"
        self.current_theme = self.default_theme
        self.apply_theme()

        self.client = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        self.search_screen = QWidget()
        self.links_screen = LinksWidget(self)
        self.stack.addWidget(self.search_screen)
        self.stack.addWidget(self.links_screen)

        self.setup_search_screen()

        self.result_buttons = []
        self.link_buttons = []

        self.header_label = None

    def apply_theme(self):
        if self.current_theme == "Dark":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2c2c2c;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    text-align: center;
                    font-size: 14px;
                    margin: 4px 2px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QLineEdit {
                    padding: 8px;
                    font-size: 14px;
                    border: 1px solid #555;
                    border-radius: 4px;
                    background-color: #3c3c3c;
                    color: white;
                }
                QLabel {
                    font-size: 14px;
                    color: #eee;
                }
                QCheckBox {
                    font-size: 14px;
                    color: #eee;
                }
                QComboBox {
                    padding: 8px;
                    font-size: 14px;
                    border: 1px solid #555;
                    border-radius: 4px;
                    background-color: #3c3c3c;
                    color: white;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox QAbstractItemView {
                    background-color: #3c3c3c;
                    color: white;
                    border: 1px solid #555;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f0f0f0;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    text-align: center;
                    font-size: 14px;
                    margin: 4px 2px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QLineEdit {
                    padding: 8px;
                    font-size: 14px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                QLabel {
                    font-size: 14px;
                    color: #333;
                }
                QCheckBox {
                    font-size: 14px;
                }
                QComboBox {
                    padding: 8px;
                    font-size: 14px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                QComboBox::drop-down {
                    border: none;
                }
            """)

    def setup_search_screen(self):
        self.search_layout = QVBoxLayout(self.search_screen)
        self.search_layout.setSpacing(10)
        self.search_layout.setContentsMargins(0, 0, 0, 0)

        self.header_label = QLabel("Hi10Anime Download Tool")
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;" if self.current_theme == "Light" else "font-size: 24px; font-weight: bold; color: #eee; margin-bottom: 10px;")
        self.search_layout.addWidget(self.header_label)

        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        self.search_label = QLabel("Enter anime title:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type anime name here...")
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(search_container)

        options_container = QWidget()
        options_layout = QHBoxLayout(options_container)
        self.use_proxy_checkbox = QCheckBox("Use Proxy")
        self.use_proxy_checkbox.setChecked(True)

        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Light", "Dark"])
        self.theme_selector.setCurrentText(self.default_theme)
        self.theme_selector.currentTextChanged.connect(self.change_theme)

        self.search_button = QPushButton("Search Anime")
        self.search_button.clicked.connect(self.perform_search)
        options_layout.addWidget(self.use_proxy_checkbox)
        options_layout.addWidget(self.theme_selector)
        options_layout.addWidget(self.search_button)
        options_layout.addStretch()
        self.search_layout.addWidget(options_container)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-style: italic; color: #555;" if self.current_theme == "Light" else "font-style: italic; color: #aaa;")
        self.search_layout.addWidget(self.status_label)

        self.results_area = QScrollArea()
        self.results_area.setWidgetResizable(True)
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)
        self.results_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.results_area.setWidget(self.results_widget)
        self.results_area.setStyleSheet("border: 1px solid #ddd; background-color: white; border-radius: 4px;" if self.current_theme == "Light" else "border: 1px solid #444; background-color: #3c3c3c; border-radius: 4px;")
        self.search_layout.addWidget(self.results_area)

    def change_theme(self, theme):
        self.current_theme = theme
        self.apply_theme()
        if self.header_label:
            self.header_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;" if theme == "Light" else "font-size: 24px; font-weight: bold; color: #eee; margin-bottom: 10px;")
        self.status_label.setStyleSheet("font-style: italic; color: #555;" if theme == "Light" else "font-style: italic; color: #aaa;")
        self.results_area.setStyleSheet("border: 1px solid #ddd; background-color: white; border-radius: 4px;" if theme == "Light" else "border: 1px solid #444; background-color: #3c3c3c; border-radius: 4px;")
        self.links_screen.update_theme(theme)

    def perform_search(self):
        search_term = self.search_input.text()
        if not search_term:
            self.status_label.setText("Please enter a search term")
            return

        self.status_label.setText(f"Searching for: {search_term}...")
        QApplication.processEvents()

        try:
            use_proxy = self.use_proxy_checkbox.isChecked()
            proxies = ProxyService.get_proxies(use_proxy)

            self.client = Hi10AnimeClient(proxies=proxies)

            results = self.client.search(search_term)
            self.display_results(results)
            self.status_label.setText(f"Found {len(results)} results")
        except Exception as e:
            self.status_label.setText(f"Search error: {str(e)}")
            print(f"Search error details: {e}")

    def display_results(self, results: list[Dict[str, str]]):
        for button in self.result_buttons:
            button.deleteLater()
        self.result_buttons.clear()

        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if results:
            for i, result in enumerate(results):
                try:
                    title = result.get('title', 'Unknown Title')
                    url = result.get('url', '')

                    if not url:
                        continue

                    result_container = QWidget()
                    result_layout = QHBoxLayout(result_container)
                    view_links_button = QPushButton(f"{i+1}. {title}")
                    view_links_button.setStyleSheet("background-color: transparent; color: #2196F3; text-align: left; border: none; text-decoration: underline;")
                    view_links_button.clicked.connect(self.create_link_handler(url, title))
                    result_layout.addWidget(view_links_button)
                    result_layout.addStretch()
                    self.results_layout.addWidget(result_container)
                    self.result_buttons.append(view_links_button)
                except Exception as e:
                    print(f"Error displaying result {i}: {e}")
        else:
            no_results_label = QLabel("No results found")
            no_results_label.setStyleSheet("color: #777; font-style: italic;" if self.current_theme == "Light" else "color: #aaa; font-style: italic;")
            self.results_layout.addWidget(no_results_label)
            self.result_buttons.append(no_results_label)
        self.results_layout.addStretch()

    def create_link_handler(self, url, title):
        return lambda: self.show_links_screen(url, title)

    def show_links_screen(self, url: str, title: str):
        self.status_label.setText(f"Fetching links for: {title}...")
        QApplication.processEvents()

        try:
            links = self.client.get_download_links(url)
            if links:
                self.status_label.setText(f"Retrieved {len(links)} links")
                self.links_screen.setup_links(title, links)
                self.stack.setCurrentWidget(self.links_screen)
            else:
                self.status_label.setText("No links found")
                print(f"No links found for {url}")
        except Exception as e:
            self.status_label.setText(f"Error fetching links: {str(e)}")
            print(f"Error fetching links for {url}: {e}")


class LinksWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.current_theme = parent.current_theme

        top_button_widget = QWidget()
        top_button_layout = QHBoxLayout(top_button_widget)
        top_button_layout.setContentsMargins(0, 0, 0, 0)

        back_button = QPushButton("Back to Search")
        back_button.clicked.connect(self.go_back)
        top_button_layout.addWidget(back_button)

        copy_all_button = QPushButton("Copy All Links")
        copy_all_button.clicked.connect(self.copy_all_links)
        top_button_layout.addWidget(copy_all_button)
        top_button_layout.addStretch()

        self.layout.addWidget(top_button_widget)

        self.header_label = QLabel("")
        self.header_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;" if self.current_theme == "Light" else "font-size: 20px; font-weight: bold; color: #eee; margin-bottom: 10px;")
        self.layout.addWidget(self.header_label)

        self.links_tree = QTreeWidget()
        self.links_tree.setHeaderLabels(["File", "Type", "Actions"])
        self.links_tree.setStyleSheet("""
            QTreeWidget {
                border: 1px solid #ddd;
                background-color: white;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 4px;
                border: 1px solid #ddd;
            }
        """ if self.current_theme == "Light" else """
            QTreeWidget {
                border: 1px solid #444;
                background-color: #3c3c3c;
                border-radius: 4px;
                color: white;
            }
            QHeaderView::section {
                background-color: #2c2c2c;
                padding: 4px;
                border: 1px solid #444;
                color: white;
            }
        """)
        self.layout.addWidget(self.links_tree)

        self.categorized_links = {}

    def update_theme(self, theme):
        self.current_theme = theme
        self.header_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;" if theme == "Light" else "font-size: 20px; font-weight: bold; color: #eee; margin-bottom: 10px;")
        self.links_tree.setStyleSheet("""
            QTreeWidget {
                border: 1px solid #ddd;
                background-color: white;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 4px;
                border: 1px solid #ddd;
            }
        """ if theme == "Light" else """
            QTreeWidget {
                border: 1px solid #444;
                background-color: #3c3c3c;
                border-radius: 4px;
                color: white;
            }
            QHeaderView::section {
                background-color: #2c2c2c;
                padding: 4px;
                border: 1px solid #444;
                color: white;
            }
        """)
        self.display_links()

    def setup_links(self, title: str, links: Set[str]):
        self.header_label.setText(f"Download Links for {title}")
        self.categorized_links = LinkParser.parse(links)
        self.display_links()

    def display_links(self):
        self.links_tree.clear()

        for season, qualities in self.categorized_links.items():
            season_item = QTreeWidgetItem(self.links_tree, [season])
            for quality, episodes in qualities.items():
                quality_item = QTreeWidgetItem(season_item, [quality])
                for episode_details in episodes:
                    link = episode_details['link']
                    episode_item = QTreeWidgetItem(quality_item, [f"Episode {episode_details['episode']}", episode_details['file_type']])
                    episode_item.setData(0, Qt.ItemDataRole.UserRole, link)

                    actions_widget = QWidget()
                    actions_layout = QHBoxLayout(actions_widget)
                    actions_layout.setContentsMargins(0, 0, 0, 0)

                    copy_button = QPushButton("Copy")
                    copy_button.clicked.connect(self.create_copy_handler(link))

                    open_button = QPushButton("Open")
                    open_button.clicked.connect(self.create_open_handler(link))

                    actions_layout.addWidget(copy_button)
                    actions_layout.addWidget(open_button)
                    actions_layout.addStretch()

                    self.links_tree.setItemWidget(episode_item, 2, actions_widget)

        self.links_tree.expandAll()

    def create_copy_handler(self, link: str):
        return lambda: self.copy_link(link)

    def create_open_handler(self, link: str):
        return lambda: self.open_link(link)

    def copy_link(self, link: str):
        clipboard = QApplication.clipboard()
        clipboard.setText(link)

    def open_link(self, link: str):
        webbrowser.open(link)

    def copy_all_links(self):
        all_links = []
        root = self.links_tree.invisibleRootItem()
        for i in range(root.childCount()):
            season_item = root.child(i)
            for j in range(season_item.childCount()):
                quality_item = season_item.child(j)
                for k in range(quality_item.childCount()):
                    episode_item = quality_item.child(k)
                    link = episode_item.data(0, Qt.ItemDataRole.UserRole)
                    if link:
                        all_links.append(link)

        if all_links:
            clipboard = QApplication.clipboard()
            clipboard.setText("\n".join(all_links))

    def go_back(self):
        self.parent.stack.setCurrentWidget(self.parent.search_screen)