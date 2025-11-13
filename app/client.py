import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Set

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