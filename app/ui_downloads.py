from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QPushButton, 
    QScrollArea, QFrame, QDialog, QCheckBox, QListWidget, QListWidgetItem,
    QMenu
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt6.QtGui import QAction, QCursor

from .downloader import DownloadManager, DownloadState

class DownloadItemWidget(QFrame):
    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.task = task
        self.setObjectName("downloadCard") # See styles.py
        self.setFrameShape(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Top Row: Filename + Status
        top_row = QHBoxLayout()
        self.name_lbl = QLabel(task.filename)
        self.name_lbl.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.status_lbl = QLabel(task.state.value)
        self.status_lbl.setObjectName("smallText")
        self.status_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        top_row.addWidget(self.name_lbl, 1)
        top_row.addWidget(self.status_lbl)
        layout.addLayout(top_row)
        
        # Middle: Progress Bar
        self.p_bar = QProgressBar()
        self.p_bar.setRange(0, 100)
        self.p_bar.setValue(int((task.downloaded_size / task.total_size * 100) if task.total_size else 0))
        self.p_bar.setFixedHeight(6)
        self.p_bar.setTextVisible(False)
        layout.addWidget(self.p_bar)
        
        # Bottom: Stats + Controls
        bot_row = QHBoxLayout()
        
        self.stats_lbl = QLabel("0 MB/s • ETA: N/A")
        self.stats_lbl.setObjectName("smallText")
        
        self.control_btn = QPushButton("Pause")
        self.control_btn.setFixedSize(60, 24)
        self.control_btn.setObjectName("secondaryBtn")
        self.control_btn.clicked.connect(self.toggle_task)
        
        self.cancel_btn = QPushButton("✕")
        self.cancel_btn.setFixedSize(24, 24)
        self.cancel_btn.setObjectName("secondaryBtn")
        self.cancel_btn.clicked.connect(self.cancel_task)
        
        bot_row.addWidget(self.stats_lbl, 1)
        bot_row.addWidget(self.control_btn)
        bot_row.addWidget(self.cancel_btn)
        layout.addLayout(bot_row)
        
        # Connect Signals
        task.progress_signal.connect(self.update_progress)
        task.status_signal.connect(self.update_status)
        
        self.update_status(task.id, task.state.value)

    def update_progress(self, _, progress, speed, eta):
        self.p_bar.setValue(int(progress))
        self.stats_lbl.setText(f"{speed} • ETA: {eta}")

    def update_status(self, _, status):
        self.status_lbl.setText(status)
        if status == DownloadState.DOWNLOADING.value:
            self.control_btn.setText("Pause")
        elif status == DownloadState.PAUSED.value:
            self.control_btn.setText("Resume")
        elif status in [DownloadState.COMPLETED.value, DownloadState.ERROR.value, DownloadState.CANCELED.value]:
            self.control_btn.setEnabled(False)
            self.control_btn.setText("-")

    def toggle_task(self):
        if self.task.state == DownloadState.DOWNLOADING:
            self.task.pause()
        elif self.task.state == DownloadState.PAUSED:
            self.task.resume()

    def cancel_task(self):
        self.task.stop()

class DownloadsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("Downloads")
        title.setObjectName("headerText") # Assuming style exists
        header.addWidget(title)
        header.addStretch()
        
        resume_all = QPushButton("Resume All")
        resume_all.clicked.connect(lambda: DownloadManager().resume_all())
        pause_all = QPushButton("Pause All")
        pause_all.clicked.connect(lambda: DownloadManager().pause_all())
        
        header.addWidget(resume_all)
        header.addWidget(pause_all)
        layout.addLayout(header)
        
        # List Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.list_layout.setSpacing(10)
        
        self.scroll.setWidget(self.list_container)
        layout.addWidget(self.scroll)
        
        # Connect to Manager
        self.mgr = DownloadManager()
        self.mgr.task_added.connect(self.add_task_widget)
        
        # Load existing tasks
        for task in self.mgr.get_all_tasks():
            self.add_task_widget(task)

    def add_task_widget(self, task):
        # Check if widget exists (optional, manager usually deduplicates tasks but widgets are new)
        item = DownloadItemWidget(task)
        self.list_layout.insertWidget(0, item) # Add to top

class BatchSelectionDialog(QDialog):
    def __init__(self, episodes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Batch Download")
        self.setMinimumWidth(400)
        self.resize(500, 600)
        
        self.layout = QVBoxLayout(self)
        
        lbl = QLabel("Select episodes to download:")
        self.layout.addWidget(lbl)
        
        # Tools
        tools = QHBoxLayout()
        self.check_all_btn = QPushButton("Check All")
        self.check_all_btn.clicked.connect(self.check_all)
        self.uncheck_all_btn = QPushButton("Uncheck All")
        self.uncheck_all_btn.clicked.connect(self.uncheck_all)
        tools.addWidget(self.check_all_btn)
        tools.addWidget(self.uncheck_all_btn)
        tools.addStretch()
        self.layout.addLayout(tools)
        
        # List
        self.list_widget = QListWidget()
        self.items = []
        for ep in episodes:
            name = f"Episode {ep['episode']}"
            if ep.get('filename'):
                name = ep.get('filename')
                
            item = QListWidgetItem(name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)
            item.setData(Qt.ItemDataRole.UserRole, ep) # Store full ep data
            
            self.list_widget.addItem(item)
            self.items.append(item)
            
        self.layout.addWidget(self.list_widget)
        
        # Buttons
        btns = QHBoxLayout()
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)
        
        self.download_btn = QPushButton("Download Selected")
        self.download_btn.setObjectName("primaryBtn") # Style
        self.download_btn.clicked.connect(self.accept)
        
        btns.addStretch()
        btns.addWidget(cancel)
        btns.addWidget(self.download_btn)
        self.layout.addLayout(btns)

    def check_all(self):
        for item in self.items:
            item.setCheckState(Qt.CheckState.Checked)
            
    def uncheck_all(self):
        for item in self.items:
            item.setCheckState(Qt.CheckState.Unchecked)

    def get_selected_episodes(self):
        selected = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                selected.append(item.data(Qt.ItemDataRole.UserRole))
        return selected
