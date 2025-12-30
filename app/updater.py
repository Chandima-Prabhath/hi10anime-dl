import requests
from PyQt6.QtCore import QThread, pyqtSignal
from .version import __version__

class UpdateChecker(QThread):
    update_available = pyqtSignal(str, str) # version, url
    error = pyqtSignal(str)

    def run(self):
        try:
            # Owner/Repo should be configured or passed in. 
            # Using the one from the prompt context: Chandima-Prabhath/hi10anime-dl
            repo_owner = "Chandima-Prabhath"
            repo_name = "hi10anime-dl"
            url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                latest_tag = data.get("tag_name", "") # e.g., "v1.1.0"
                html_url = data.get("html_url", "")
                
                # Simple version comparison
                # Remove 'v' prefix if present
                clean_latest = latest_tag.lstrip("v")
                clean_current = __version__.lstrip("v")
                
                if self.is_newer(clean_current, clean_latest):
                    self.update_available.emit(latest_tag, html_url)
            else:
                 # Be silent on 404/rate limits to not annoy user
                 pass
        except Exception:
            pass

    def is_newer(self, current, latest):
        try:
            cur_parts = [int(x) for x in current.split('.')]
            lat_parts = [int(x) for x in latest.split('.')]
            
            # Normalize lengths
            while len(cur_parts) < 3: cur_parts.append(0)
            while len(lat_parts) < 3: lat_parts.append(0)
            
            return lat_parts > cur_parts
        except ValueError:
            return False
