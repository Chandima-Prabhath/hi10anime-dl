import sys
import math
from pathlib import Path
import webbrowser
import darkdetect
from typing import Set, Dict, Optional, Any

from PyQt6.QtWidgets import (
    QApplication, QStackedWidget, QMainWindow, QVBoxLayout, QWidget, 
    QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, QScrollArea, 
    QHBoxLayout, QFrame, QGraphicsOpacityEffect, QSizePolicy, QGridLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer, QPoint, QRectF, QSize
from PyQt6.QtGui import QIcon, QColor, QFont, QPainter, QPen, QBrush, QPixmap

from .client import Hi10AnimeClient
from .proxy import ProxyService
from .parser import LinkParser
from .styles import StyleSheet

class WorkerThread(QThread):
    finished_signal = pyqtSignal(object)
    error_signal = pyqtSignal(str)

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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.hide()
        
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        
        self.text_label = QLabel("Loading...", self)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setStyleSheet("font-size: 16px; font-weight: bold; background: transparent;")
        
        self.bg_color = QColor(0, 0, 0, 150)
        self.spinner_color = QColor("#89b4fa")

    def update_theme(self, theme):
        colors = StyleSheet.get_colors(theme)
        if theme == "Dark":
            self.bg_color = QColor(30, 30, 46, 210)
        else:
             self.bg_color = QColor(255, 255, 255, 220)
        
        self.spinner_color = QColor(colors['spinner'])
        # Ensure text is contrasting or just use theme fg
        self.text_label.setStyleSheet(f"color: {colors['fg']}; font-size: 16px; font-weight: bold; background: transparent;")
        self.update()

    def rotate(self):
        self.angle = (self.angle + 10) % 360
        self.update()

    def show_loading(self, text="Loading..."):
        self.text_label.setText(text)
        self.resize(self.parent().size())
        self.show()
        self.raise_()
        self.timer.start(30) 

    def stop(self):
        self.timer.stop()
        self.hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), self.bg_color)
        
        size = 60
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2 - 20
        rect = QRectF(x, y, size, size)
        
        pen = QPen(self.spinner_color)
        pen.setWidth(6)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        start_angle = -self.angle * 16
        span_angle = 270 * 16
        painter.drawArc(rect, start_angle, span_angle)
        
        self.text_label.setGeometry(0, y + size + 15, self.width(), 30)

class ToastNotification(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.SubWindow)
        self.setObjectName("toastFrame")
        
        self.label = QLabel(self)
        self.label.setStyleSheet("border: none; background: transparent; font-weight: 600;")
        
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.setContentsMargins(20, 10, 20, 10)
        
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.fade_out)
        self.hide()

    def update_theme(self, theme):
        self.style().unpolish(self)
        self.style().polish(self)

    def show_message(self, message, duration=2500):
        self.label.setText(message)
        self.adjustSize()
        parent_geo = self.parent().geometry()
        x = (parent_geo.width() - self.width()) // 2
        y = parent_geo.height() - self.height() - 60
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


# --- New Widgets: Theme Toggle & Collapsible ---

class ThemeToggle(QPushButton):
    def __init__(self, current_theme="Dark", parent=None):
        super().__init__(parent)
        self.setObjectName("themeToggle")
        self.setFixedSize(40, 40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setIconSize(QSize(24, 24))
        self.update_icon(current_theme)

    def update_icon(self, theme):
        # Resolve icon path
        base_path = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
        # Assuming icons are in app/icons relative to this file
        icon_dir = base_path / 'icons'
        
        if theme == "Dark":
            icon_path = icon_dir / 'toggle-on-100.png'
        else:
            icon_path = icon_dir / 'toggle-off-100.png'
            
        if icon_path.exists():
            self.setIcon(QIcon(str(icon_path)))
        else:
            self.setText("T") # Fallback

class CollapsibleBox(QWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.toggle_button = QPushButton(f"▼ {title}") # Default expanded
        self.toggle_button.setObjectName("collageHeader") # Default style
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True) # Default expanded
        
        self.toggle_button.clicked.connect(self.on_pressed)

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.toggle_button)
        self.main_layout.addWidget(self.content_area)

    def set_header_style(self, style_name):
        self.toggle_button.setObjectName(style_name)

    def set_content_layout(self, layout):
        pass
        
    def add_widget(self, widget):
        self.content_layout.addWidget(widget)

    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        
        arrow = "▼ " if checked else "▶ "
        current_text = self.toggle_button.text()
        clean_text = current_text.replace("▼ ", "").replace("▶ ", "").strip()
        self.toggle_button.setText(f"{arrow}{clean_text}")
        
        self.content_area.setVisible(checked)

    def toggle(self, state):
        self.toggle_button.setChecked(state)
        # Manually update text
        arrow = "▼ " if state else "▶ "
        current_text = self.toggle_button.text()
        clean_text = current_text.replace("▼ ", "").replace("▶ ", "").strip()
        self.toggle_button.setText(f"{arrow}{clean_text}")
        
        self.content_area.setVisible(state)

# --- Link Widgets ---

class EpisodeCard(QFrame):
    def __init__(self, name, link, link_type, parent_widget):
        super().__init__()
        self.setObjectName("episodeCard")
        self.link = link
        self.parent_widget = parent_widget
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)
        
        name_lbl = QLabel(name)
        name_lbl.setWordWrap(True)
        layout.addWidget(name_lbl, 1)
        
        type_lbl = QLabel(link_type)
        type_lbl.setObjectName("smallText")
        type_lbl.setFixedWidth(60)
        type_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(type_lbl)
        
        copy_btn = QPushButton("Copy")
        copy_btn.setObjectName("secondaryBtn")
        copy_btn.setFixedWidth(60)
        copy_btn.clicked.connect(self.copy_link)
        
        open_btn = QPushButton("Open")
        open_btn.setObjectName("secondaryBtn")
        open_btn.setFixedWidth(60)
        open_btn.clicked.connect(self.open_link)
        
        layout.addWidget(copy_btn)
        layout.addWidget(open_btn)

    def copy_link(self):
        cb = QApplication.clipboard()
        cb.setText(self.link)
        if self.parent_widget:
            self.parent_widget.show_toast("Link copied!")

    def open_link(self):
        webbrowser.open(self.link)

# --- App ---

class AnimeSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hi10Anime DL")
        self.setGeometry(100, 100, 1000, 800)
        
        base_path = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent.parent))
        icon_path = base_path / 'app.ico'
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self.default_theme = "Dark"
        if not darkdetect.isDark():
            self.default_theme = "Light" 
        self.current_theme = self.default_theme

        self.client = None
        self.worker = None

        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.stack = QStackedWidget()
        
        self.search_screen = QWidget()
        self.setup_search_screen()
        
        self.links_screen = LinksWidget(self)
        
        self.stack.addWidget(self.search_screen)
        self.stack.addWidget(self.links_screen)
        
        self.main_layout.addWidget(self.stack)

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
        
        # Theme Toggle
        self.theme_toggle = ThemeToggle(self.current_theme)
        self.theme_toggle.clicked.connect(self.toggle_theme)
        
        header_layout.addWidget(self.header_label)
        header_layout.addStretch()
        header_layout.addWidget(self.theme_toggle)
        
        layout.addWidget(header_container)

        # Search Card
        search_card = QFrame()
        search_card.setObjectName("resultCard")
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

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.use_proxy_checkbox)
        search_layout.addWidget(self.search_button)
        
        layout.addWidget(search_card)

        # Results
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
        self.loading_overlay.update_theme(self.current_theme)
        self.toast.update_theme(self.current_theme)
        if hasattr(self, 'theme_toggle'):
            self.theme_toggle.update_icon(self.current_theme)

    def toggle_theme(self):
        self.current_theme = "Light" if self.current_theme == "Dark" else "Dark"
        self.apply_theme()

    def resizeEvent(self, event):
        if hasattr(self, 'loading_overlay'):
             self.loading_overlay.resize(self.central_widget.size())
        super().resizeEvent(event)

    def perform_search(self):
        term = self.search_input.text().strip()
        if not term:
            self.toast.show_message("Please enter a search term!")
            return

        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.loading_overlay.show_loading(f"Searching for '{term}'...")
        
        use_proxy = self.use_proxy_checkbox.isChecked()
        proxies = ProxyService.get_proxies(use_proxy)
        
        self.worker = WorkerThread(self._search_task, term, proxies)
        self.worker.finished_signal.connect(self.on_search_finished)
        self.worker.error_signal.connect(self.on_thread_error)
        self.worker.start()

    def _search_task(self, term, proxies):
        client = Hi10AnimeClient(proxies=proxies)
        self.client = client
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
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        layout.addWidget(title_lbl)
        layout.addStretch()
        
        arrow_lbl = QLabel("→")
        arrow_lbl.setStyleSheet("font-size: 20px; font-weight: bold;") 
        layout.addWidget(arrow_lbl)

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
        
        # Clear
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.collapsibles = []
        categorized = LinkParser.parse(links)
        self.all_links = []
        
        for season, qualities in categorized.items():
            # Season Collapsible
            season_box = CollapsibleBox(f"  {season}  ")
            season_box.set_header_style("collageHeader")
            self.collapsibles.append(season_box)
            
            # Aggregate links for season copy if needed? Keep simple for now.
            
            # Inside Season: Quality Collapsibles
            for quality, episodes in qualities.items():
                for ep in episodes:
                    self.all_links.append(ep['link'])
                
                q_links = [e['link'] for e in episodes]
                q_title = f"{quality} ({len(episodes)} eps)"
                
                # Quality Box
                quality_box = CollapsibleBox(q_title)
                quality_box.set_header_style("qualityHeader")
                
                # Add "Copy Quality" btn to header? 
                # CollapsibleBox needs custom header widget to support buttons inside it.
                # Current implementation implies just a button toggle.
                # Let's add a toolbar inside the content area top?
                
                # Content for quality
                q_content = QWidget()
                q_layout = QVBoxLayout(q_content)
                q_layout.setContentsMargins(10, 5, 5, 5)
                
                # Copy Quality Button
                copy_q_btn = QPushButton("Copy Section Links")
                copy_q_btn.setObjectName("ghostBtn")
                copy_q_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                copy_q_btn.clicked.connect(lambda checked, l=q_links: self.copy_list(l))
                q_layout.addWidget(copy_q_btn)
                
                for ep in episodes:
                    name = f"Episode {ep['episode']}"
                    if ep['episode'] in ["N/A", "Extras"] or ep.get('filename'):
                        name = ep.get('filename') or name
                    
                    card = EpisodeCard(name, ep['link'], ep['file_type'], self)
                    q_layout.addWidget(card)
                    
                quality_box.add_widget(q_content)
                season_box.add_widget(quality_box)
                self.collapsibles.append(quality_box)
            
            self.content_layout.addWidget(season_box)

    def toggle_all(self, state):
        for box in self.collapsibles:
            box.toggle(state)

    def go_back(self):
        self.parent_app.stack.setCurrentWidget(self.parent_app.search_screen)
        
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