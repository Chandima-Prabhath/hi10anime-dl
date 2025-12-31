from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QSpinBox,
    QComboBox,
    QGroupBox,
)
from PyQt6.QtCore import Qt
from ..settings import settings

class SettingsScreen(QWidget):
    """A screen for configuring application settings."""

    def __init__(self, parent=None):
        """Initializes the SettingsScreen."""
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Download Settings
        download_group = QGroupBox("Download Settings")
        download_layout = QFormLayout()

        self.download_location_input = QLineEdit()
        self.download_location_button = QPushButton("Browse")
        self.download_location_button.clicked.connect(self.browse_download_location)
        download_layout.addRow(QLabel("Download Location:"), self.download_location_input)
        download_layout.addRow("", self.download_location_button)


        self.simultaneous_downloads_spinbox = QSpinBox()
        self.simultaneous_downloads_spinbox.setMinimum(1)
        self.simultaneous_downloads_spinbox.setMaximum(16)
        download_layout.addRow(
            QLabel("Simultaneous Downloads:"), self.simultaneous_downloads_spinbox
        )

        self.download_parts_combobox = QComboBox()
        for i in range(2, 33):
            self.download_parts_combobox.addItem(str(i))
        download_layout.addRow(QLabel("Parts per Download:"), self.download_parts_combobox)

        download_group.setLayout(download_layout)
        self.layout.addWidget(download_group)

        # Proxy Settings
        proxy_group = QGroupBox("Proxy Settings")
        proxy_layout = QFormLayout()

        self.http_proxy_input = QLineEdit()
        proxy_layout.addRow(QLabel("HTTP Proxy:"), self.http_proxy_input)

        self.https_proxy_input = QLineEdit()
        proxy_layout.addRow(QLabel("HTTPS Proxy:"), self.https_proxy_input)

        proxy_group.setLayout(proxy_layout)
        self.layout.addWidget(proxy_group)

        # Load initial settings
        self.load_settings()

        # Connect signals
        self.download_location_input.editingFinished.connect(self.save_settings)
        self.simultaneous_downloads_spinbox.valueChanged.connect(self.save_settings)
        self.download_parts_combobox.currentIndexChanged.connect(self.save_settings)
        self.http_proxy_input.editingFinished.connect(self.save_settings)
        self.https_proxy_input.editingFinished.connect(self.save_settings)


    def browse_download_location(self):
        """Opens a dialog to select a download location."""
        directory = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if directory:
            self.download_location_input.setText(directory)
            self.save_settings()

    def load_settings(self):
        """Loads settings from the settings service and populates the UI."""
        self.download_location_input.setText(settings.get("download_location", ""))
        self.simultaneous_downloads_spinbox.setValue(settings.get("simultaneous_downloads", 3))
        self.download_parts_combobox.setCurrentText(str(settings.get("download_parts", 8)))
        self.http_proxy_input.setText(settings.get("proxy.http", ""))
        self.https_proxy_input.setText(settings.get("proxy.https", ""))

    def save_settings(self):
        """Saves the current settings to the settings service."""
        settings.set("download_location", self.download_location_input.text())
        settings.set("simultaneous_downloads", self.simultaneous_downloads_spinbox.value())
        settings.set("download_parts", int(self.download_parts_combobox.currentText()))
        settings.set("proxy.http", self.http_proxy_input.text())
        settings.set("proxy.https", self.https_proxy_input.text())
