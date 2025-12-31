import logging
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Set
from .config import config


class Hi10AnimeClient:
    """A client for interacting with the Hi10Anime website."""

    BASE_URL = "https://hi10anime.com"
    LOGIN_URL = f"{BASE_URL}/wp-login.php"
    SEARCH_URL = f"{BASE_URL}/?s="
    JTOKEN = "jtoken=17d26554d7"

    def __init__(self, proxies: Optional[Dict[str, str]] = None):
        """Initializes the Hi10AnimeClient.

        Args:
            proxies (Optional[Dict[str, str]], optional): Proxies to use for requests. Defaults to None.
        """
        self.session = requests.Session()
        self.proxies = proxies
        self.username = config.get("credentials.username")
        self.password = config.get("credentials.password")
        self._login()

    def _login(self) -> None:
        """Logs in to the Hi10Anime website."""
        logging.info("Logging in...")
        data = {"log": self.username, "pwd": self.password}
        try:
            response = self.session.post(
                self.LOGIN_URL, data=data, proxies=self.proxies
            )
            response.raise_for_status()
            logging.info("Login successful.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Login failed: {e}")

    def search(self, title: str) -> list[Dict[str, str]]:
        """Searches for an anime on the Hi10Anime website.

        Args:
            title (str): The title of the anime to search for.

        Returns:
            list[Dict[str, str]]: A list of search results.
        """
        url = self.SEARCH_URL + title.replace(" ", "+")
        logging.info(f"Searching for '{title}' at {url}.")
        try:
            response = self.session.get(url, proxies=self.proxies)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "lxml")
            results = []
            for post in soup.find_all("article"):
                try:
                    anime_title = post.h1.a.text
                    anime_url = post.h1.a["href"]
                    if not any(
                        itm in anime_title
                        for itm in ["Updates", "Collection", "Mirrors", "Review"]
                    ):
                        results.append({"title": anime_title, "url": anime_url})
                except Exception as e:
                    logging.warning(f"Could not parse a search result item: {e}")
                    continue
            logging.info(f"Found {len(results)} search results.")
            return results
        except Exception as e:
            logging.error(f"Search error: {e}")
            return []

    def get_download_links(self, url: str) -> Set[str]:
        """Gets the download links from a given anime page.

        Args:
            url (str): The URL of the anime page.

        Returns:
            Set[str]: A set of download links.
        """
        logging.info(f"Getting download links from {url}.")
        try:
            res = self.session.get(url, proxies=self.proxies)
            res.raise_for_status()
            soup = BeautifulSoup(res.content, "lxml")
        except Exception as e:
            logging.error(f"Failed to fetch page: {e}")
            return set()

        links = set()
        extractors = [
            self._extract_from_episodes_div,
            self._extract_from_show_links_table,
            self._extract_from_entry_content_paragraphs,
            self._extract_from_entry_content_tds,
            self._extract_from_entry_content_anchors,
        ]
        for extractor in extractors:
            try:
                found_links = extractor(soup)
                logging.info(f"{extractor.__name__} found {len(found_links)} links.")
                links.update(found_links)
            except Exception as e:
                logging.warning(f"Extractor {extractor.__name__} failed: {e}")
                continue
        logging.info(f"Total links found: {len(links)}")
        return links

    def _extract_from_episodes_div(self, soup: BeautifulSoup) -> Set[str]:
        """Extracts download links from the 'episodes' div.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the page.

        Returns:
            Set[str]: A set of download links.
        """
        links = set()
        episodes_div = soup.find("div", {"class": "episodes"})
        if not episodes_div:
            return links
        for row in episodes_div.find_all("span", {"class": "ddl"}):
            for a in row.find_all("a", href=True):
                href = a["href"]
                if href.startswith("https://ouo.io/"):
                    token = self._extract_token(href)
                    if token:
                        links.add(token)
        return links

    def _extract_from_show_links_table(self, soup: BeautifulSoup) -> Set[str]:
        """Extracts download links from the 'showLinksTable' table.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the page.

        Returns:
            Set[str]: A set of download links.
        """
        links = set()
        table = soup.find("table", {"class": "showLinksTable"})
        if not table:
            return links
        tbody = table.tbody if table.tbody else table
        for row in tbody.find_all("tr"):
            tds = row.find_all("td")[2:]
            for td in tds:
                a = td.find("a", href=True)
                if a and a["href"].startswith("https://ouo.io/"):
                    token = self._extract_token(a["href"])
                    if token:
                        links.add(token)
        return links

    def _extract_from_entry_content_paragraphs(self, soup: BeautifulSoup) -> Set[str]:
        """Extracts download links from paragraphs in the 'entry-content' div.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the page.

        Returns:
            Set[str]: A set of download links.
        """
        links = set()
        entry_content = soup.find("div", {"class": "entry-content"})
        if not entry_content:
            return links
        for p in entry_content.find_all("p"):
            anchors = p.find_all("a", href=True)
            for a in anchors:
                href = a["href"]
                if href.startswith("https://ouo.io/"):
                    token = self._extract_token(href)
                    if token:
                        links.add(token)
        return links

    def _extract_from_entry_content_tds(self, soup: BeautifulSoup) -> Set[str]:
        """Extracts download links from table cells in the 'entry-content' div.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the page.

        Returns:
            Set[str]: A set of download links.
        """
        links = set()
        entry_content = soup.find("div", {"class": "entry-content"})
        if not entry_content:
            return links
        for td in entry_content.find_all("td"):
            anchors = td.find_all("a", href=True)
            for a in anchors:
                href = a["href"]
                if href.startswith("https://ouo.io/"):
                    token = self._extract_token(href)
                    if token:
                        links.add(token)
        return links

    def _extract_from_entry_content_anchors(self, soup: BeautifulSoup) -> Set[str]:
        """Extracts download links from anchors in the 'entry-content' div.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the page.

        Returns:
            Set[str]: A set of download links.
        """
        links = set()
        entry_content = soup.find("div", {"class": "entry-content"})
        if not entry_content:
            return links
        for a in entry_content.find_all("a", href=True):
            href = a["href"]
            if href.startswith("https://ouo.io/"):
                token = self._extract_token(href)
                if token:
                    links.add(token)
        return links

    def _extract_token(self, href: str) -> Optional[str]:
        """Extracts the token from a given URL.

        Args:
            href (str): The URL to extract the token from.

        Returns:
            Optional[str]: The extracted token, or None if it could not be extracted.
        """
        if "s=" in href:
            try:
                token = href.split("s=")[1].split("&")[0]
                return f"{token}?{self.JTOKEN}"
            except Exception:
                return None
        return None
