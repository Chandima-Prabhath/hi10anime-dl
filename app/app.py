import sys
import logging
from pathlib import Path
import darkdetect

from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon

from .client import Hi10AnimeClient
from .proxy import ProxyService
from .styles import StyleSheet
from .version import __version__
from .updater import UpdateChecker
from .widgets.loading_overlay import LoadingOverlay
from .widgets.toast_notification import ToastNotification
from .screens.home_screen import HomeScreen
from .screens.results_screen import ResultsWidget
from .screens.links_screen import LinksWidget
from .config import config


class WorkerThread(QThread):
    """A QThread that executes a function in a separate thread.

    Signals:
        finished_signal (pyqtSignal): Emitted when the function finishes successfully.
        error_signal (pyqtSignal): Emitted when an exception occurs.
    """
    finished_signal = pyqtSignal(object)
    error_signal = pyqtSignal(str)

    def __init__(self, func, *args, **kwargs):
        """Initializes the WorkerThread.

        Args:
            func (function): The function to execute.
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.
        """
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """Executes the function and emits the appropriate signal."""
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished_signal.emit(result)
        except Exception as e:
            self.error_signal.emit(str(e))


class AnimeSearchApp(QMainWindow):
    """The main application window."""

    def __init__(self):
        """Initializes the main application window."""
        super().__init__()
        self.setWindowTitle(f"Hi10Anime DL v{__version__}")
        self.setGeometry(100, 100, 1000, 800)

        self.base_path = Path(
            getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent)
        )
        icon_path = self.base_path / "app.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self.default_theme = config.get("theme.default", "Dark")
        if not darkdetect.isDark():
            self.default_theme = "Light"
        self.current_theme = self.default_theme

        self.client = None
        self.worker = None

        self.setup_ui()
        self.apply_theme()

        QTimer.singleShot(1000, self.check_updates)

    def setup_ui(self):
        """Sets up the user interface of the application."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.stack = QStackedWidget()

        self.home_screen = HomeScreen(self)
        self.results_screen = ResultsWidget(self)
        self.links_screen = LinksWidget(self)

        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.results_screen)
        self.stack.addWidget(self.links_screen)

        self.main_layout.addWidget(self.stack)

        self.loading_overlay = LoadingOverlay(self.central_widget)
        self.toast = ToastNotification(self.central_widget)

    def apply_theme(self):
        """Applies the current theme to the application."""
        self.setStyleSheet(StyleSheet.get_stylesheet(self.current_theme))
        self.loading_overlay.update_theme(self.current_theme)
        self.toast.update_theme(self.current_theme)
        if hasattr(self.home_screen, "theme_toggle"):
            self.home_screen.theme_toggle.update_icon(self.current_theme)

    def toggle_theme(self):
        """Toggles the application theme between light and dark."""
        self.current_theme = "Light" if self.current_theme == "Dark" else "Dark"
        logging.info(f"Toggling theme to {self.current_theme}.")
        self.apply_theme()

    def check_updates(self):
        """Checks for application updates."""
        self.updater = UpdateChecker()
        self.updater.update_available.connect(
            self.home_screen.update_banner.show_update
        )
        self.updater.start()

    def resizeEvent(self, event):
        """Handles the resize event of the main window."""
        if hasattr(self, "loading_overlay"):
            self.loading_overlay.resize(self.central_widget.size())
        super().resizeEvent(event)

    def show_home(self):
        """Switches the view to the home screen."""
        self.stack.setCurrentWidget(self.home_screen)

    def execute_search(self, term):
        """Executes a search for a given term.

        Args:
            term (str): The search term.
        """
        logging.info(f"Executing search for '{term}'.")
        self.loading_overlay.show_loading(f"Searching for '{term}'...")

        self.results_screen.search_input.setText(term)
        self.stack.setCurrentWidget(self.results_screen)

        self.results_screen.clear_results()

        use_proxy = self.home_screen.use_proxy_checkbox.isChecked()
        proxies = ProxyService.get_proxies(use_proxy)
        logging.info(f"Using proxy: {use_proxy}")

        self.worker = WorkerThread(self._search_task, term, proxies)
        self.worker.finished_signal.connect(self.on_search_finished)
        self.worker.error_signal.connect(self.on_thread_error)
        self.worker.start()

    def _search_task(self, term, proxies):
        """The actual search task that is run in a worker thread.

        Args:
            term (str): The search term.
            proxies (dict): The proxies to use for the search.

        Returns:
            list: A list of search results.
        """
        client = Hi10AnimeClient(proxies=proxies)
        self.client = client
        return client.search(term)

    def on_search_finished(self, results):
        """Handles the finished signal of the search worker thread.

        Args:
            results (list): The search results.
        """
        logging.info(f"Search finished. Found {len(results)} results.")
        self.loading_overlay.stop()
        if not results:
            self.toast.show_message("No anime found.")
            return

        for result in results:
            self.results_screen.add_result(result)

    def on_thread_error(self, error_msg):
        """Handles the error signal of a worker thread.

        Args:
            error_msg (str): The error message.
        """
        logging.error(f"Thread error: {error_msg}")
        self.loading_overlay.stop()
        self.toast.show_message(f"Error: {error_msg}")
        self.stack.setCurrentWidget(self.home_screen)

    def fetch_links(self, url, title):
        """Fetches the download links for a given anime.

        Args:
            url (str): The URL of the anime page.
            title (str): The title of the anime.
        """
        logging.info(f"Fetching links for '{title}' at {url}.")
        self.loading_overlay.show_loading(f"Fetching links for {title}...")

        self.worker = WorkerThread(self.client.get_download_links, url)
        self.worker.finished_signal.connect(
            lambda links: self.on_links_fetched(links, title)
        )
        self.worker.error_signal.connect(self.on_thread_error)
        self.worker.start()

    def on_links_fetched(self, links, title):
        """Handles the finished signal of the link fetching worker thread.

        Args:
            links (set): The download links.
            title (str): The title of the anime.
        """
        logging.info(f"Fetched {len(links)} links for '{title}'.")
        self.loading_overlay.stop()
        if not links:
            self.toast.show_message("No download links found.")
            return

        self.links_screen.setup_links(title, links)
        self.stack.setCurrentWidget(self.links_screen)
