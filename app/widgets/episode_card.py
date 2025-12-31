import webbrowser
from PyQt6.QtWidgets import QFrame, QLabel, QPushButton, QHBoxLayout, QApplication
from PyQt6.QtCore import Qt


class EpisodeCard(QFrame):
    def __init__(self, name, link, link_type, parent_widget):
        super().__init__()
        self.setObjectName("episodeCard")
        self.link = link
        self.parent_widget = parent_widget

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)

        name_lbl = QLabel(name)
        name_lbl.setWordWrap(True)
        layout.addWidget(name_lbl, 1)

        type_lbl = QLabel(link_type)
        type_lbl.setObjectName("smallText")
        type_lbl.setFixedWidth(60)
        type_lbl.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(type_lbl)

        copy_btn = QPushButton("Copy")
        copy_btn.setObjectName("secondaryBtn")
        copy_btn.setFixedWidth(80)
        copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        copy_btn.clicked.connect(self.copy_link)

        open_btn = QPushButton("Open")
        open_btn.setObjectName("secondaryBtn")
        open_btn.setFixedWidth(80)
        open_btn.clicked.connect(self.open_link)

        layout.addWidget(copy_btn)
        layout.addWidget(open_btn)

    def copy_link(self):
        cb = QApplication.clipboard()
        cb.setText(self.link)
        if self.parent_widget:
            self.parent_widget.show_toast("Link copied!")

    def open_link(self):
        webbrowser.open(self.link)
