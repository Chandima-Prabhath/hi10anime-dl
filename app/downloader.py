import os
import time
import json
import threading
import requests
from pathlib import Path
from enum import  Enum
from collections import  deque
from PyQt6.QtCore import QObject, pyqtSignal

from .settings import SettingsManager

class DownloadState(Enum):
    QUEUED = "Queued"
    DOWNLOADING = "Downloading"
    PAUSED = "Paused"
    MERGING = "Merging"
    COMPLETED = "Completed"
    ERROR = "Error"
    CANCELED = "Canceled"

class DownloadTask(QObject):
    progress_signal = pyqtSignal(str, float, str, str) # id, progress, speed, state
    status_signal = pyqtSignal(str, str) # id, state
    error_signal = pyqtSignal(str, str) # id, error_msg

    def __init__(self, url, filename, folder_path, parent=None):
        super().__init__(parent)
        self.url = url
        self.filename = filename
        self.folder_path = Path(folder_path)
        self.file_path = self.folder_path / filename
        self.meta_file_path = self.folder_path / f"{filename}.part.json"
        
        self.id = str(hash(f"{url}{filename}")) # Simple ID
        self.state = DownloadState.QUEUED
        self.settings = SettingsManager()
        
        self.total_size = 0
        self.downloaded_size = 0
        self.start_time = 0
        self.speed = 0
        self.eta = "N/A"
        
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._pause_event.set() # Start unpaused
        
        self.parts = [] # List of {"start": int, "end": int, "current": int}
        
        self.load_state()

    def load_state(self):
        if self.meta_file_path.exists():
            try:
                with open(self.meta_file_path, 'r') as f:
                    data = json.load(f)
                    self.total_size = data.get('total_size', 0)
                    self.downloaded_size = data.get('downloaded_size', 0)
                    self.parts = data.get('parts', [])
                    self.state = DownloadState(data.get('state', "Queued"))
                    if self.state == DownloadState.DOWNLOADING:
                        self.state = DownloadState.PAUSED
            except Exception as e:
                print(f"Error loading state: {e}")

    def save_state(self):
        data = {
            'url': self.url,
            'filename': self.filename,
            'folder_path': str(self.folder_path),
            'total_size': self.total_size,
            'downloaded_size': self.downloaded_size,
            'state': self.state.value,
            'parts': self.parts
        }
        try:
            with open(self.meta_file_path, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving state: {e}")

    def start(self):
        if self.state in [DownloadState.COMPLETED, DownloadState.MERGING]:
            return
            
        self.state = DownloadState.DOWNLOADING
        self._stop_event.clear()
        self._pause_event.set()
        
        threading.Thread(target=self._download_monitor, daemon=True).start()

    def pause(self):
        if self.state == DownloadState.DOWNLOADING:
            self.state = DownloadState.PAUSED
            self._pause_event.clear()
            self.save_state()
            self.status_signal.emit(self.id, self.state.value)

    def resume(self):
        if self.state == DownloadState.PAUSED:
            self.state = DownloadState.DOWNLOADING
            self._pause_event.set()
            # Threads check the event
            self.status_signal.emit(self.id, self.state.value)

    def stop(self):
        self.state = DownloadState.CANCELED
        self._stop_event.set()
        self.save_state()
        self.status_signal.emit(self.id, self.state.value)

    def _get_file_size(self):
        try:
            response = requests.head(self.url, allow_redirects=True)
            if 'Content-Length' in response.headers:
                return int(response.headers['Content-Length'])
        except:
            pass
        return 0

    def _download_part(self, part_index, start, end):
        part_file = self.folder_path / f"{self.filename}.part{part_index}"
        
        # Resume logic
        current = start
        mode = 'wb'
        if part_file.exists():
            current += part_file.stat().st_size
            mode = 'ab'
            
        if current > end:
            return # Already done
        
        headers = {'Range': f"bytes={current}-{end}"}
        
        try:
            with requests.get(self.url, headers=headers, stream=True, timeout=20) as r:
                r.raise_for_status()
                with open(part_file, mode) as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if self._stop_event.is_set():
                            return
                        while not self._pause_event.is_set():
                            time.sleep(0.5)
                            if self._stop_event.is_set():
                                return
                        
                        if chunk:
                            f.write(chunk)
                            self.parts[part_index]['current'] += len(chunk)
                            self.downloaded_size += len(chunk)
        except Exception as e:
            print(f"Part {part_index} error: {e}")
            # Retry logic could go here
            pass

    def _download_monitor(self):
        try:
            if not self.folder_path.exists():
                self.folder_path.mkdir(parents=True, exist_ok=True)

            if self.total_size == 0:
                self.total_size = self._get_file_size()
                # Initialize parts
                num_parts = self.settings.get("parts_per_file", 8)
                if self.total_size > 0:
                    chunk_size = self.total_size // num_parts
                    self.parts = []
                    for i in range(num_parts):
                        start = i * chunk_size
                        end = (i + 1) * chunk_size - 1 if i < num_parts - 1 else self.total_size - 1
                        self.parts.append({"start": start, "end": end, "current": start})
                else:
                    # Fallback single part if size unknown
                    self.parts = [{"start": 0, "end": "", "current": 0}]

            # Start Threads
            threads = []
            for i, part in enumerate(self.parts):
                if part['current'] <= part['end'] if isinstance(part['end'], int) else True:
                    t = threading.Thread(target=self._download_part, args=(i, part['start'], part['end']))
                    t.name = f"Part-{i}"
                    t.start()
                    threads.append(t)
            
            # Monitor loop
            self.start_time = time.time()
            last_size = 0
            
            while any(t.is_alive() for t in threads):
                if self._stop_event.is_set():
                    return
                
                # Check completion
                current_total = sum(p['current'] - p['start'] for p in self.parts)
                # Note: downloaded_size var is updated atomically by threads, but resetting it here safely
                self.downloaded_size = current_total
                
                # Metrics
                elapsed = time.time() - self.start_time
                if elapsed > 0:
                    self.speed = (self.downloaded_size - last_size) / 1.0 # approx 1 sec sleep
                    # Use a smoother speed?
                    remaining = self.total_size - self.downloaded_size
                    if self.speed > 0:
                        self.eta = self._format_time(remaining / self.speed)
                
                progress = (self.downloaded_size / self.total_size * 100) if self.total_size else 0
                speed_str = f"{self.speed / 1024 / 1024:.2f} MB/s"
                
                self.progress_signal.emit(self.id, progress, speed_str, self.eta)
                self.save_state() # Periodically save state
                
                time.sleep(1)
            
            # Use strict verification
            if self.downloaded_size >= self.total_size and self.total_size > 0:
                self.state = DownloadState.MERGING
                self.status_signal.emit(self.id, self.state.value)
                self._merge_parts()
                self._finalize()
            elif self.total_size == 0 and self.parts[0]['current'] > 0:
                 # Unknown size completed (single stream)
                 self._merge_parts()
                 self._finalize()

        except Exception as e:
            self.state = DownloadState.ERROR
            self.error_signal.emit(self.id, str(e))
            self.save_state()

    def _merge_parts(self):
        final_file = self.folder_path / self.filename
        with open(final_file, 'wb') as outfile:
            for i in range(len(self.parts)):
                part_file = self.folder_path / f"{self.filename}.part{i}"
                if part_file.exists():
                    with open(part_file, 'rb') as infile:
                        outfile.write(infile.read())
                    part_file.unlink()

    def _finalize(self):
        if self.meta_file_path.exists():
            self.meta_file_path.unlink()
            
        self.state = DownloadState.COMPLETED
        self.progress_signal.emit(self.id, 100.0, "0 MB/s", "0s")
        self.status_signal.emit(self.id, self.state.value)
        # Notify Manager to remove from active list or mark complete

    def _format_time(self, seconds):
        if seconds < 60:
            return f"{int(seconds)}s"
        minutes = int(seconds / 60)
        return f"{minutes}m"


class DownloadManager(QObject):
    task_added = pyqtSignal(object) # DownloadTask
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DownloadManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, parent=None):
        if self._initialized:
            return
        super().__init__(parent)
        self.settings = SettingsManager()
        self.queue = deque()
        self.tasks = {} 
        self.max_concurrent = self.settings.get("max_concurrent_downloads", 3)
        self.session_file = self.settings.app_data_dir / "session.json"
        self._initialized = True
        
        self._restore_session()

    def add_download(self, url, filename, anime_name, season_name):
        base_path = Path(self.settings.get("download_path"))
        folder_path = base_path / anime_name / season_name
        
        task = DownloadTask(url, filename, folder_path)
        
        if task.id in self.tasks:
            return
            
        self.tasks[task.id] = task
        self.queue.append(task)
        self.task_added.emit(task)
        self.save_session()
        self.process_queue()

    def process_queue(self):
        active_count = sum(1 for t in self.tasks.values() if t.state == DownloadState.DOWNLOADING)
        
        while active_count < self.max_concurrent and self.queue:
            task = self.queue.popleft()
            if task.state == DownloadState.QUEUED or task.state == DownloadState.PAUSED:
                task.start()
                active_count += 1
    
    def save_session(self):
        # Save list of "pending/active" tasks to restore later
        session_data = []
        for task in self.tasks.values():
            if task.state != DownloadState.COMPLETED:
                session_data.append({
                    'url': task.url,
                    'filename': task.filename,
                    'folder_path': str(task.folder_path)
                })
        
        try:
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=4)
        except Exception as e:
            print(f"Error saving session: {e}")

    def _restore_session(self):
        if not self.session_file.exists():
            return
            
        try:
            with open(self.session_file, 'r') as f:
                data = json.load(f)
                
            for item in data:
                task = DownloadTask(item['url'], item['filename'], item['folder_path'])
                self.tasks[task.id] = task
                self.queue.append(task)
                # Emitting task_added might be needed if UI is already connected, 
                # but usually this runs before UI. 
                # We'll emit when UI requests refresh or connect.
                
        except Exception as e:
            print(f"Error restoring session: {e}")

    def pause_all(self):
        for task in self.tasks.values():
            task.pause()

    def resume_all(self):
        for task in self.tasks.values():
            if task.state == DownloadState.PAUSED:
                task.resume()
                
    def get_task(self, task_id):
        return self.tasks.get(task_id)

    def get_all_tasks(self):
        return list(self.tasks.values())
