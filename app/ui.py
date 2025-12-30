import sys
from pathlib import Path
import webbrowser
import darkdetect
from typing import Set, Dict, Optional, Any

from PyQt6.QtWidgets import (
    QApplication, QStackedWidget, QMainWindow, QVBoxLayout, QWidget, 
    QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, QScrollArea, 
    QTreeWidget, QTreeWidgetItem, QHBoxLayout, QFrame, QGraphicsOpacityEffect,
    QSizePolicy, QProgressBar, QTreeWidgetItemIterator
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer, QPoint
from PyQt6.QtGui import QIcon, QColor, QFont

from .client import Hi10AnimeClient
from .proxy import ProxyService
from .parser import LinkParser
from .styles import StyleSheet

class WorkerThread(QThread):
    """
    Generic worker thread to run blocking tasks.
    """
    finished_signal = pyqtSignal(object)  # Emits the result
    error_signal = pyqtSignal(str)        # Emits error message

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished_signal.emit(result)
        except Exception as e:
            self.error_signal.emit(str(e))

class LoadingOverlay(QWidget):
    """
    A semi-transparent overlay with a spinner/text to show loading state.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False) # block mouse
        self.hide()
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.card = QFrame()
        self.card.setStyleSheet("background-color: rgba(30, 30, 46, 0.9); border-radius: 12px; padding: 20px;")
        card_layout = QVBoxLayout(self.card)
        
        self.spinner = QProgressBar()
        self.spinner.setRange(0, 0) # Indeterminate mode
        self.spinner.setFixedWidth(200)
        self.spinner.setTextVisible(False)
        self.spinner.setStyleSheet("""
            QProgressBar {
                border: 2px solid #45475a;
                border-radius: 5px;
                background-color: transparent;
            }
            QProgressBar::chunk {
                background-color: #89b4fa;
                width: 20px; 
            }
        """)

        self.label = QLabel("Loading...")
        self.label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; margin-top: 10px;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card_layout.addWidget(self.spinner)
        card_layout.addWidget(self.label)
        layout.addWidget(self.card)

    def show_loading(self, text="Loading..."):
        self.label.setText(text)
        self.resize(self.parent().size())
        self.show()
        self.raise_()

    def stop(self):
        self.hide()

class ToastNotification(QFrame):
    """
    Non-intrusive popup notification.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.SubWindow)
        self.setStyleSheet("""
            QFrame {
                background-color: #313244; 
                color: #cdd6f4; 
                border-radius: 8px; 
                border: 1px solid #45475a;
                padding: 10px 20px;
            }
        """)
        self.label = QLabel(self)
        self.label.setStyleSheet("border: none; background: transparent; color: #cdd6f4; font-weight: 600;")
        
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.setContentsMargins(15, 10, 15, 10)
        
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.fade_out)
        self.hide()

    def show_message(self, message, duration=2500):
        self.label.setText(message)
        self.adjustSize()
        
        # Position at bottom center
        parent_geo = self.parent().geometry()
        x = (parent_geo.width() - self.width()) // 2
        y = parent_geo.height() - self.height() - 50
        self.move(x, y)
        
        self.show()
        self.raise_()
        self.opacity_effect.setOpacity(1.0)
        self.timer.start(duration)

    def fade_out(self):
        self.anim.setDuration(500)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.anim.finished.connect(self.hide)
        self.anim.start()

class AnimeSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hi10Anime DL")
        self.setGeometry(100, 100, 1000, 750)
        
        # Set Icon
        base_path = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent.parent))
        icon_path = base_path / 'app.ico'
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        # Theme Init
        self.default_theme = "Dark" # Default to Dark for modern feel
        if not darkdetect.isDark():
            self.default_theme = "Light" 
        self.current_theme = self.default_theme

        # Data
        self.client = None
        self.worker = None

        # UI Init
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Content Stack
        self.stack = QStackedWidget()
        
        self.search_screen = QWidget()
        self.setup_search_screen()
        
        self.links_screen = LinksWidget(self)
        
        self.stack.addWidget(self.search_screen)
        self.stack.addWidget(self.links_screen)
        
        self.main_layout.addWidget(self.stack)

        # Overlays
        self.loading_overlay = LoadingOverlay(self.central_widget)
        self.toast = ToastNotification(self.central_widget)

    def setup_search_screen(self):
        layout = QVBoxLayout(self.search_screen)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Header
        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.header_label = QLabel("Hi10Anime DL")
        self.header_label.setObjectName("headerTitle")
        
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Dark", "Light"])
        self.theme_selector.setCurrentText(self.current_theme)
        self.theme_selector.setFixedWidth(100)
        self.theme_selector.currentTextChanged.connect(self.change_theme)
        
        header_layout.addWidget(self.header_label)
        header_layout.addStretch()
        header_layout.addWidget(self.theme_selector)
        
        layout.addWidget(header_container)

        # Search Bar Area
        search_card = QFrame()
        search_card.setObjectName("resultCard") # Reusing card style
        search_layout = QHBoxLayout(search_card)
        search_layout.setContentsMargins(20, 20, 20, 20)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for anime... (e.g., 'One Piece')")
        self.search_input.returnPressed.connect(self.perform_search)
        
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)
        self.search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.use_proxy_checkbox = QCheckBox("Use Proxy")
        self.use_proxy_checkbox.setChecked(True)
        self.use_proxy_checkbox.setToolTip("Enable if you have connection issues")

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.use_proxy_checkbox)
        search_layout.addWidget(self.search_button)
        
        layout.addWidget(search_card)

        # Results Area
        self.results_scroll = QScrollArea()
        self.results_scroll.setWidgetResizable(True)
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)
        self.results_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.results_layout.setSpacing(10)
        
        self.results_scroll.setWidget(self.results_widget)
        layout.addWidget(self.results_scroll)

    def apply_theme(self):
        self.setStyleSheet(StyleSheet.get_stylesheet(self.current_theme))
        # Pass theme down if needed to custom components, though Stylesheet handles most globally

    def change_theme(self, theme):
        self.current_theme = theme
        self.apply_theme()
        if hasattr(self, 'links_screen'):
            self.links_screen.update_icons(theme)

    def resizeEvent(self, event):
        # Resize overlay when window resizes
        if hasattr(self, 'loading_overlay'):
             self.loading_overlay.resize(self.central_widget.size())
        super().resizeEvent(event)

    def perform_search(self):
        term = self.search_input.text().strip()
        if not term:
            self.toast.show_message("Please enter a search term!")
            return

        self.results_layout.removeWidget(self.results_widget) # Clear hack
        # Proper clear
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.loading_overlay.show_loading(f"Searching for '{term}'...")
        
        # Prepare Worker
        use_proxy = self.use_proxy_checkbox.isChecked()
        proxies = ProxyService.get_proxies(use_proxy)
        
        # If client not init or proxies changed, re-init. 
        # For simplicity, we can just create a fresh client or re-use.
        # Let's create a client wrapper function for the thread.
        
        self.worker = WorkerThread(self._search_task, term, proxies)
        self.worker.finished_signal.connect(self.on_search_finished)
        self.worker.error_signal.connect(self.on_thread_error)
        self.worker.start()

    def _search_task(self, term, proxies):
        # Initialize client here to run in thread? 
        # Requests Session is not thread class friendly sometimes if shared, 
        # but creating new one is fine.
        client = Hi10AnimeClient(proxies=proxies)
        self.client = client # Cache it for later use (link fetching)
        return client.search(term)

    def on_search_finished(self, results):
        self.loading_overlay.stop()
        if not results:
            self.show_no_results()
            return
            
        for result in results:
            self.add_result_card(result)

    def on_thread_error(self, error_msg):
        self.loading_overlay.stop()
        self.toast.show_message(f"Error: {error_msg}")

    def show_no_results(self):
        lbl = QLabel("No anime found. Try a different query.")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color: #888; font-size: 16px; margin-top: 20px;")
        self.results_layout.addWidget(lbl)

    def add_result_card(self, result):
        title = result.get('title', 'Unknown')
        url = result.get('url', '')
        
        card = QFrame()
        card.setObjectName("resultCard")
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QHBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        layout.addWidget(title_lbl)
        layout.addStretch()
        
        # Icon
        arrow_lbl = QLabel("→")
        arrow_lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #89b4fa;") # Accent color
        layout.addWidget(arrow_lbl)

        # Make entire card clickable
        # We can use an event filter or a transparent button on top, 
        # or just mousePressEvent override if we subclass QFrame.
        # Simpler: Button disguised as transparent overlay
        # Or just a button inside. simpler to just use mouseRelease
        
        # Let's use a button overlay
        overlay_btn = QPushButton(card)
        overlay_btn.setStyleSheet("background: transparent; border: none;")
        overlay_btn.resize(card.size()) # Initial size, needs resize event ideally
        # Hack: layout ensures size? No overlay is absolute.
        # Better: Standard button taking full space?
        # Let's actually Just use a custom widget signal.
        
        # For valid Clickable frame:
        card.mouseReleaseEvent = lambda e: self.fetch_links(url, title)
        
        self.results_layout.addWidget(card)

    def fetch_links(self, url, title):
        self.loading_overlay.show_loading(f"Fetching links for {title}...")
        
        self.worker = WorkerThread(self.client.get_download_links, url)
        self.worker.finished_signal.connect(lambda links: self.on_links_fetched(links, title, url))
        self.worker.error_signal.connect(self.on_thread_error)
        self.worker.start()

    def on_links_fetched(self, links, title, url):
        self.loading_overlay.stop()
        if not links:
            self.toast.show_message("No download links found for this anime.")
            return
            
        self.links_screen.setup_links(title, links)
        self.stack.setCurrentWidget(self.links_screen)


class LinksWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent_app = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
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
        
        self.copy_all_btn = QPushButton("Copy All Links")
        self.copy_all_btn.setFixedWidth(120)
        self.copy_all_btn.clicked.connect(self.copy_all)

        top_bar.addWidget(self.back_btn)
        top_bar.addWidget(self.title_lbl, 1) # stretch
        top_bar.addWidget(self.copy_all_btn)
        
        layout.addLayout(top_bar)

        # Tree View
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["File Name / Episode", "Format", "Actions"])
        # Set column widths
        self.tree.setColumnWidth(0, 400)
        self.tree.setColumnWidth(1, 100)
        layout.addWidget(self.tree)

    def update_icons(self, theme):
        # Could update specific icons here if needed
        pass

    def setup_links(self, title, links):
        self.title_lbl.setText(title)
        self.tree.clear()
        
        categorized = LinkParser.parse(links)
        
        for season, qualities in categorized.items():
            season_item = QTreeWidgetItem(self.tree, [season])
            season_item.setExpanded(True)
            
            for quality, episodes in qualities.items():
                quality_item = QTreeWidgetItem(season_item, [quality])
                quality_item.setExpanded(True)
                
                # Copy All Quality Button (Cell Widget)
                copy_q_btn = QPushButton("Copy Quality")
                copy_q_btn.setObjectName("secondaryBtn")
                copy_q_btn.setFixedSize(100, 24)
                copy_q_btn.setStyleSheet("""
                    QPushButton { padding: 0px 5px; font-size: 11px; }
                """)
                copy_q_btn.clicked.connect(lambda checked, eps=episodes: self.copy_list([e['link'] for e in eps]))
                
                # Container for button to center/align it
                q_widget = QWidget()
                q_layout = QHBoxLayout(q_widget)
                q_layout.setContentsMargins(0,0,0,0)
                q_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
                q_layout.addWidget(copy_q_btn)
                
                self.tree.setItemWidget(quality_item, 2, q_widget)

                for ep_data in episodes:
                    name = f"Episode {ep_data['episode']}"
                    if ep_data['episode'] in ["N/A", "Extras"] or ep_data.get('filename'):
                        name = ep_data['filename'] if ep_data['filename'] else name
                    
                    link = ep_data['link']
                    item = QTreeWidgetItem(quality_item, [name, ep_data['file_type']])
                    item.setData(0, Qt.ItemDataRole.UserRole, link)
                    
                    # Actions
                    actions_widget = QWidget()
                    actions_layout = QHBoxLayout(actions_widget)
                    actions_layout.setContentsMargins(0, 2, 0, 2)
                    actions_layout.setSpacing(5)
                    
                    copy_btn = QPushButton("Copy")
                    copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                    copy_btn.setFixedSize(60, 24)
                    copy_btn.setStyleSheet("font-size: 11px; padding: 0;")
                    copy_btn.clicked.connect(lambda checked, l=link: self.copy_one(l))
                    
                    open_btn = QPushButton("Open")
                    open_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                    open_btn.setObjectName("secondaryBtn")
                    open_btn.setFixedSize(60, 24)
                    open_btn.setStyleSheet("font-size: 11px; padding: 0;")
                    open_btn.clicked.connect(lambda checked, l=link: webbrowser.open(l))
                    
                    actions_layout.addWidget(copy_btn)
                    actions_layout.addWidget(open_btn)
                    actions_layout.addStretch()
                    
                    self.tree.setItemWidget(item, 2, actions_widget)

    def go_back(self):
        self.parent_app.stack.setCurrentWidget(self.parent_app.search_screen)

    def copy_one(self, link):
        cb = QApplication.clipboard()
        cb.setText(link)
        self.parent_app.toast.show_message("Link copied to clipboard!")

    def copy_list(self, links):
        if not links: 
            return
        cb = QApplication.clipboard()
        cb.setText("\n".join(links))
        self.parent_app.toast.show_message(f"Copied {len(links)} links!")

    def copy_all(self):
        urls = []
        iterator = QTreeWidgetItemIterator(self.tree)
        while iterator.value():
            item = iterator.value()
            link = item.data(0, Qt.ItemDataRole.UserRole)
            if link:
                urls.append(link)
            iterator += 1
            
        if urls:
            self.copy_list(urls)
        else:
            self.parent_app.toast.show_message("No links to copy.")