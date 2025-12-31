from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QSpinBox, QFileDialog, QFrame, QCheckBox
)
from PyQt6.QtCore import Qt
from pathlib import Path

from .settings import SettingsManager

class SettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = SettingsManager()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Header
        title = QLabel("Settings")
        title.setObjectName("headerText")
        layout.addWidget(title)
        
        # Section: Downloads
        grp = self.create_group("Download Configuration")
        grp_layout = QVBoxLayout(grp)
        grp_layout.setSpacing(15)
        
        # Path
        path_row = QHBoxLayout()
        self.path_lbl = QLabel(self.settings.get("download_path"))
        self.path_lbl.setObjectName("pathText") # Style needed
        self.path_lbl.setStyleSheet("background: #1e1e2e; padding: 10px; border-radius: 5px; color: #cdd6f4;")
        
        browse_btn = QPushButton("Browse")
        browse_btn.setFixedSize(80, 40)
        browse_btn.clicked.connect(self.browse_path)
        
        path_row.addWidget(QLabel("Download Location:"))
        path_row.addWidget(self.path_lbl, 1)
        path_row.addWidget(browse_btn)
        grp_layout.addLayout(path_row)
        
        # Concurrency
        conc_row = QHBoxLayout()
        self.conc_spin = QSpinBox()
        self.conc_spin.setRange(1, 10)
        self.conc_spin.setValue(self.settings.get("max_concurrent_downloads", 3))
        self.conc_spin.valueChanged.connect(lambda v: self.settings.set("max_concurrent_downloads", v))
        
        conc_row.addWidget(QLabel("Max Concurrent Downloads:"))
        conc_row.addWidget(self.conc_spin)
        conc_row.addStretch()
        grp_layout.addLayout(conc_row)
        
        # Parts
        parts_row = QHBoxLayout()
        self.parts_spin = QSpinBox()
        self.parts_spin.setRange(1, 32)
        self.parts_spin.setValue(self.settings.get("parts_per_file", 8))
        self.parts_spin.valueChanged.connect(lambda v: self.settings.set("parts_per_file", v))
        
        parts_row.addWidget(QLabel("Parts per File:"))
        parts_row.addWidget(self.parts_spin)
        parts_row.addStretch()
        grp_layout.addLayout(parts_row)

        layout.addWidget(grp)
        
        # Section: Application
        app_grp = self.create_group("Application")
        app_layout = QVBoxLayout(app_grp)
        
        # Proxy
        self.proxy_chk = QCheckBox("Use Proxy (Recommended)")
        self.proxy_chk.setChecked(self.settings.get("use_proxy", True))
        self.proxy_chk.stateChanged.connect(lambda s: self.settings.set("use_proxy", s == 2))
        app_layout.addWidget(self.proxy_chk)
        
        layout.addWidget(app_grp)
        layout.addStretch()

    def create_group(self, title):
        group = QFrame()
        group.setObjectName("settingsGroup")
        group.setFrameShape(QFrame.Shape.StyledPanel)
        
        l = QVBoxLayout(group)
        lbl = QLabel(title)
        lbl.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 10px;")
        l.addWidget(lbl)
        
        content = QWidget()
        l.addWidget(content)
        return content

    def browse_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Download Folder", self.path_lbl.text())
        if path:
            self.settings.set("download_path", path)
            self.path_lbl.setText(path)
