import os
try:
    import winreg
except ImportError:
    winreg = None
from typing import Optional, Dict

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
