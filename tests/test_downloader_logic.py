import sys
import os
import time
import shutil
import traceback
from pathlib import Path

# Add app to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtCore import QCoreApplication

try:
    from app.downloader import DownloadManager, DownloadState
    from app.settings import SettingsManager
except ImportError:
    print("Import Error!")
    traceback.print_exc()
    sys.exit(1)

def test_downloader():
    print("Testing Downloader Logic...")
    
    # Init QCoreApplication for signals
    app = QCoreApplication(sys.argv)
    
    try:
        # Setup Test Dir
        test_dir = Path("d:/Works/Projects/hi10anime-dl/tests/downloads_test")
        if test_dir.exists():
            shutil.rmtree(test_dir)
        test_dir.mkdir(parents=True)
        
        # Setup Settings
        settings = SettingsManager()
        settings.set("download_path", str(test_dir))
        settings.set("max_concurrent_downloads", 2)
        settings.set("parts_per_file", 4)
        
        mgr = DownloadManager() # Singleton initialization
        
        print("Adding tasks...")
        mgr.add_download("https://disk.sample.cat/samples/mp4/1416529-uhd_3840_2160_30fps.mp4", "file1.mp4", "Anime1", "Season1")
        mgr.add_download("https://disk.sample.cat/samples/webm/1416529-sd_960_540_30fps.webm", "file2.webm", "Anime1", "Season1")
        mgr.add_download("https://disk.sample.cat/samples/avi/1416529-sd_640_360_30fps.avi", "file3.avi", "Anime2", "Season1")
            
        # Check immediately
        active = [t for t in mgr.tasks.values() if t.state == DownloadState.DOWNLOADING]
        queued = [t for t in mgr.tasks.values() if t.state == DownloadState.QUEUED]
        
        print(f"Active: {len(active)}, Queued: {len(queued)}")
        
        # Since we just added them, and they are threaded, they might be in DOWNLOADING state fairly quickly.
        # But limited by max_concurrent=2
        
        if len(active) <= 2:
             print("[PASS] Queue limit respected (<=2 active).")
        else:
             print(f"[FAIL] Queue limit exceeded. Active: {len(active)}")
             
        # Test Persistence
        print("Testing Persistence...")
        mgr.save_session()
        
        session_file = settings.app_data_dir / "session.json"
        if session_file.exists():
            print("[PASS] Session file created.")
            with open(session_file, 'r') as f:
                content = f.read()
                if "file3.mp4" in content:
                    print("[PASS] Session content verified.")
                else:
                    print("[FAIL] Session content missing items.")
        else:
            print("[FAIL] Session file not found.")

        # Cleanup
        # shutil.rmtree(test_dir)
        
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    test_downloader()
