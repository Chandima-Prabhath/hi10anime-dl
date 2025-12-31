from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout


class CollapsibleBox(QWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.toggle_button = QPushButton(f"▼ {title}")  # Default expanded
        self.toggle_button.setObjectName("collageHeader")  # Default style
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)  # Default expanded

        self.toggle_button.clicked.connect(self.on_pressed)

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.toggle_button)
        self.main_layout.addWidget(self.content_area)

    def set_header_style(self, style_name):
        self.toggle_button.setObjectName(style_name)

    def set_content_layout(self, layout):
        pass

    def add_widget(self, widget):
        self.content_layout.addWidget(widget)

    def on_pressed(self):
        checked = self.toggle_button.isChecked()

        arrow = "▼ " if checked else "▶ "
        current_text = self.toggle_button.text()
        clean_text = current_text.replace("▼ ", "").replace("▶ ", "").strip()
        self.toggle_button.setText(f"{arrow}{clean_text}")

        self.content_area.setVisible(checked)

    def toggle(self, state):
        self.toggle_button.setChecked(state)
        # Manually update text
        arrow = "▼ " if state else "▶ "
        current_text = self.toggle_button.text()
        clean_text = current_text.replace("▼ ", "").replace("▶ ", "").strip()
        self.toggle_button.setText(f"{arrow}{clean_text}")

        self.content_area.setVisible(state)
