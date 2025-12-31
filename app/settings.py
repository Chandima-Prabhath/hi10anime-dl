import json
import os
from pathlib import Path
from typing import Dict, Any

class SettingsManager:
    _instance = None
    DEFAULT_SETTINGS = {
        "download_path": str(Path.home() / "Downloads" / "Anime"),
        "max_concurrent_downloads": 3,
        "parts_per_file": 8,
        "theme": "Dark",
        "resume_on_startup": True,
        "use_proxy": True
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self.app_data_dir = self._get_app_data_dir()
        self.settings_file = self.app_data_dir / "settings.json"
        self._settings = self.DEFAULT_SETTINGS.copy()
        self._load()
        self._initialized = True

    def _get_app_data_dir(self) -> Path:
        """Get the application data directory."""
        # Use user's local app data
        path = Path(os.getenv('LOCALAPPDATA', Path.home())) / "Hi10AnimeDL"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _load(self):
        """Load settings from JSON file."""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    saved_settings = json.load(f)
                    # Update defaults with saved, keeping new defaults if structure changes
                    self._settings.update(saved_settings)
            except Exception as e:
                print(f"Error loading settings: {e}")

    def save(self):
        """Save current settings to JSON file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self._settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self._settings.get(key, default)

    def set(self, key: str, value: Any):
        """Set a setting value and save."""
        self._settings[key] = value
        self.save()

    def get_all(self) -> Dict[str, Any]:
        """Get all settings."""
        return self._settings.copy()
