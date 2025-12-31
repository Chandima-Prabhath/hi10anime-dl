import json
import os
import sys
from pathlib import Path

from PyQt6.QtCore import QStandardPaths


class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._init_settings()
        return cls._instance

    def _init_settings(self):
        if getattr(sys, "frozen", False):
            # Running as a bundled executable
            app_name = "Hi10AnimeDL"
            self.settings_path = Path(
                QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
            ) / app_name
        else:
            # Running as a script
            self.settings_path = Path(__file__).resolve().parent.parent

        if not self.settings_path.exists():
            self.settings_path.mkdir(parents=True, exist_ok=True)

        self.settings_file = self.settings_path / "settings.json"
        self.settings = {}
        self.load()

    def load(self):
        if self.settings_file.exists():
            with open(self.settings_file, "r") as f:
                try:
                    self.settings = json.load(f)
                except json.JSONDecodeError:
                    self.settings = self._get_default_settings()
        else:
            self.settings = self._get_default_settings()
            self.save()

    def _get_default_settings(self):
        return {
            "theme": "Dark",
            "download_location": str(Path.home() / "Downloads"),
            "simultaneous_downloads": 3,
            "download_parts": 8,
            "proxy": {
                "http": "",
                "https": ""
            }
        }

    def save(self):
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key, default=None):
        keys = key.split(".")
        value = self.settings
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def set(self, key, value):
        keys = key.split(".")
        d = self.settings
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value
        self.save()


settings = Settings()
