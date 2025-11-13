import os
try:
    import winreg
except ImportError:
    winreg = None
from typing import Optional, Dict, Set
import requests
from bs4 import BeautifulSoup
from PyQt6.QtWidgets import QApplication, QStackedWidget, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QScrollArea, QTreeWidget, QTreeWidgetItem
from PyQt6.QtWidgets import QHBoxLayout
import webbrowser
import darkdetect
import re


# Domain layer - Core business logic
class Hi10AnimeClient:
    BASE_URL = "https://hi10anime.com"
    LOGIN_URL = f"{BASE_URL}/wp-login.php"
    SEARCH_URL = f"{BASE_URL}/?s="
    JTOKEN = "jtoken=17d26554d7"

    def __init__(self, username: str = "imbpy@hi2.in", password: str = "imbpy@hi2.in", proxies: Optional[Dict[str, str]] = None):
        self.session = requests.Session()
        self.proxies = proxies
        self.username = username
        self.password = password
        self._login()

    def _login(self) -> None:
        data = {
            'log': self.username,
            'pwd': self.password
        }
        self.session.post(self.LOGIN_URL, data=data, proxies=self.proxies)

    def search(self, title: str) -> list[Dict[str, str]]:
        url = self.SEARCH_URL + title.replace(' ', '+')
        try:
            response = self.session.get(url, proxies=self.proxies)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            results = []
            for post in soup.find_all('article'):
                try:
                    anime_title = post.h1.a.text
                    anime_url = post.h1.a['href']
                    if not any(itm in anime_title for itm in ['Updates', 'Collection', 'Mirrors', 'Review']):
                        results.append({'title': anime_title, 'url': anime_url})
                except Exception:
                    continue
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return []

    def get_download_links(self, url: str) -> Set[str]:
        try:
            res = self.session.get(url, proxies=self.proxies)
            res.raise_for_status()
            soup = BeautifulSoup(res.content, 'lxml')
        except Exception as e:
            print(f"Failed to fetch page: {e}")
            return set()

        links = set()
        extractors = [
            self._extract_from_episodes_div,
            self._extract_from_show_links_table,
            self._extract_from_entry_content_paragraphs,
            self._extract_from_entry_content_tds,
            self._extract_from_entry_content_anchors
        ]
        for extractor in extractors:
            try:
                links.update(extractor(soup))
            except Exception:
                continue
        return links

    def _extract_from_episodes_div(self, soup: BeautifulSoup) -> Set[str]:
        links = set()
        episodes_div = soup.find('div', {'class': 'episodes'})
        if not episodes_div:
            return links
        for row in episodes_div.find_all('span', {'class': 'ddl'}):
            for a in row.find_all('a', href=True):
                href = a['href']
                if href.startswith('https://ouo.io/'):
                    token = self._extract_token(href)
                    if token:
                        links.add(token)
        return links

    def _extract_from_show_links_table(self, soup: BeautifulSoup) -> Set[str]:
        links = set()
        table = soup.find('table', {'class': 'showLinksTable'})
        if not table:
            return links
        tbody = table.tbody if table.tbody else table
        for row in tbody.find_all('tr'):
            tds = row.find_all('td')[2:]
            for td in tds:
                a = td.find('a', href=True)
                if a and a['href'].startswith('https://ouo.io/'):
                    token = self._extract_token(a['href'])
                    if token:
                        links.add(token)
        return links

    def _extract_from_entry_content_paragraphs(self, soup: BeautifulSoup) -> Set[str]:
        links = set()
        entry_content = soup.find('div', {'class': 'entry-content'})
        if not entry_content:
            return links
        for p in entry_content.find_all('p'):
            anchors = p.find_all('a', href=True)
            for a in anchors:
                href = a['href']
                if href.startswith('https://ouo.io/'):
                    token = self._extract_token(href)
                    if token:
                        links.add(token)
        return links

    def _extract_from_entry_content_tds(self, soup: BeautifulSoup) -> Set[str]:
        links = set()
        entry_content = soup.find('div', {'class': 'entry-content'})
        if not entry_content:
            return links
        for td in entry_content.find_all('td'):
            anchors = td.find_all('a', href=True)
            for a in anchors:
                href = a['href']
                if href.startswith('https://ouo.io/'):
                    token = self._extract_token(href)
                    if token:
                        links.add(token)
        return links

    def _extract_from_entry_content_anchors(self, soup: BeautifulSoup) -> Set[str]:
        links = set()
        entry_content = soup.find('div', {'class': 'entry-content'})
        if not entry_content:
            return links
        for a in entry_content.find_all('a', href=True):
            href = a['href']
            if href.startswith('https://ouo.io/'):
                token = self._extract_token(href)
                if token:
                    links.add(token)
        return links

    def _extract_token(self, href: str) -> Optional[str]:
        if 's=' in href:
            try:
                token = href.split('s=')[1].split('&')[0]
                return f"{token}?{self.JTOKEN}"
            except Exception:
                return None
        return None

# Infrastructure layer - External services
class ProxyService:
    @staticmethod
    def get_windows_proxy() -> Optional[str]:
        if winreg:
            try:
                with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
                ) as key:
                    if winreg.QueryValueEx(key, "ProxyEnable")[0]:
                        proxy = winreg.QueryValueEx(key, "ProxyServer")[0]
                        return proxy.split(";")[0] if ";" in proxy else proxy
            except (OSError, ValueError):
                return None
        return None

    @staticmethod
    def get_proxies(use_proxy: bool) -> Optional[Dict[str, str]]:
        if use_proxy:
            if proxy := ProxyService.get_windows_proxy():
                print(f"Using Windows system proxy: {proxy}")
                return {"http": proxy, "https": proxy}

            env_proxies = {
                "http": os.environ.get("http_proxy") or os.environ.get("HTTP_PROXY"),
                "https": os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY")
            }

            if any(env_proxies.values()):
                print(f"Using environment proxy: {env_proxies}")
                return env_proxies

        print("Warning: No proxy settings found. Trying without proxy.")
        return None
    

class LinkParser:
    @staticmethod
    def parse(links: Set[str]) -> Dict[str, Dict[str, list]]:
        categorized_links = {}

        for link in links:
            # Extract filename from the URL
            try:
                filename = link.split('/')[-1].split('?')[0]
            except IndexError:
                continue

            # Default values
            season = "Season 1"
            quality = "Unknown"
            episode = "N/A"
            file_type = "MKV"

            # Improved regex to find season/part information
            season_match = re.search(r'\[(.*?)\]', filename)
            if season_match:
                season_text = season_match.group(1)
                # More robust season detection
                if "season" in season_text.lower() or re.match(r'S\d+', season_text):
                    season = season_text
                elif re.search(r'II|III|IV|V', season_text): # Roman numerals for seasons
                    season = f"Season {season_text.count('I') + season_text.count('V')*4}"
                # Add other keywords that could indicate a new season or part
                elif any(s in season_text for s in ["Part", "Cour", "Book"]):
                    season = season_text


            # Regex to find quality
            quality_match = re.search(r'(\d{3,4}p)', filename)
            if quality_match:
                quality = quality_match.group(1)
            elif "BD" in filename:
                quality = "BD"

            # Regex for episode number
            episode_match = re.search(r' (\d{2,3}) ', filename)
            if episode_match:
                episode = episode_match.group(1)
            elif "NCOP" in filename:
                episode = "NCOP"
            elif "NCED" in filename:
                episode = "NCED"


            # Determine file type
            if ".torrent" in filename:
                file_type = "Torrent"

            # Build nested dictionary
            if season not in categorized_links:
                categorized_links[season] = {}
            if quality not in categorized_links[season]:
                categorized_links[season][quality] = []

            categorized_links[season][quality].append({
                "episode": episode,
                "file_type": file_type,
                "link": link
            })

        # Sort episodes within each quality
        for season in categorized_links.values():
            for quality_links in season.values():
                quality_links.sort(key=lambda x: x["episode"])

        return categorized_links
    
# Application layer - PyQt6 GUI
class AnimeSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hi10Anime  DL")
        self.setGeometry(100, 100, 900, 700)  # Larger window size for better layout
        self.setWindowIcon(QIcon("app.ico"))
        
        # Determine default theme based on system preference
        self.default_theme = "Dark" if darkdetect.isDark() else "Light"
        self.current_theme = self.default_theme
        self.apply_theme()
        
        self.client = None
            
        # Use a stacked widget for navigation between screens
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)
        
        # Initialize the two screens
        self.search_screen = QWidget()
        self.links_screen = LinksWidget(self)
        self.stack.addWidget(self.search_screen)
        self.stack.addWidget(self.links_screen)
        
        # Setup search screen UI
        self.setup_search_screen()

        # Store buttons to prevent garbage collection
        self.result_buttons = []
        self.link_buttons = []
        
        # Store header label for theme updates
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

        # Header
        self.header_label = QLabel("Hi10Anime Download Tool")
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;" if self.current_theme == "Light" else "font-size: 24px; font-weight: bold; color: #eee; margin-bottom: 10px;")
        self.search_layout.addWidget(self.header_label)

        # Search input area
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        self.search_label = QLabel("Enter anime title:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type anime name here...")
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(search_container)

        # Options area
        options_container = QWidget()
        options_layout = QHBoxLayout(options_container)
        self.use_proxy_checkbox = QCheckBox("Use Proxy")
        self.use_proxy_checkbox.setChecked(True)  # Enable proxy by default
        
        # Theme selection dropdown
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
        
        # Add status label for feedback
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-style: italic; color: #555;" if self.current_theme == "Light" else "font-style: italic; color: #aaa;")
        self.search_layout.addWidget(self.status_label)

        # Results area with scroll
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
        # Update dynamic styles for widgets created before theme change
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
        QApplication.processEvents()  # Update UI
        
        try:
            use_proxy = self.use_proxy_checkbox.isChecked()
            proxies = ProxyService.get_proxies(use_proxy)

            # Initialize client here, inside the search function
            self.client = Hi10AnimeClient(proxies=proxies)
                
            results = self.client.search(search_term)
            self.display_results(results)
            self.status_label.setText(f"Found {len(results)} results")
        except Exception as e:
            self.status_label.setText(f"Search error: {str(e)}")
            print(f"Search error details: {e}")

    def display_results(self, results: list[Dict[str, str]]):
        # Clear previous results
        for button in self.result_buttons:
            button.deleteLater()
        self.result_buttons.clear()
        
        # Clear the layout
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
        """Create a handler function for a specific URL to avoid lambda capture issues"""
        return lambda: self.show_links_screen(url, title)

    def show_links_screen(self, url: str, title: str):
        self.status_label.setText(f"Fetching links for: {title}...")
        QApplication.processEvents()  # Update UI
        
        try:
            links = self.client.get_download_links(url)
            if links:
                self.status_label.setText(f"Retrieved {len(links)} links")
                # Navigate to links screen instead of opening a new window
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
        
        # Top buttons
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
        
        # Header (will be updated dynamically)
        self.header_label = QLabel("")
        self.header_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;" if self.current_theme == "Light" else "font-size: 20px; font-weight: bold; color: #eee; margin-bottom: 10px;")
        self.layout.addWidget(self.header_label)

        # Tree widget for categorized links
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

                    # Actions widget
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

if __name__ == "__main__":
    app = QApplication([])
    window = AnimeSearchApp()
    window.show()
    app.exec()