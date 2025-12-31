from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QApplication,
)
from .episode_card import EpisodeCard


class QualityTab(QWidget):
    def __init__(self, quality_name, episodes: list, parent_widget):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 10, 0, 10)
        self.layout.setSpacing(5)

        action_bar = QHBoxLayout()
        action_bar.setContentsMargins(5, 0, 5, 0)

        count_lbl = QLabel(f"{len(episodes)} Episodes")
        count_lbl.setObjectName("smallText")

        copy_all_btn = QPushButton("Copy This Quality")
        copy_all_btn.setObjectName("ghostBtn")
        copy_all_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        copy_all_btn.clicked.connect(lambda: self.copy_all(episodes, parent_widget))

        action_bar.addWidget(count_lbl)
        action_bar.addStretch()
        action_bar.addWidget(copy_all_btn)

        self.layout.addLayout(action_bar)

        for ep in episodes:
            name = f"Episode {ep['episode']}"
            if ep["episode"] in ["N/A", "Extras"] or ep.get("filename"):
                name = ep.get("filename") or name

            card = EpisodeCard(name, ep["link"], ep["file_type"], parent_widget)
            self.layout.addWidget(card)

    def copy_all(self, episodes, parent):
        links = [e["link"] for e in episodes]
        cb = QApplication.clipboard()
        cb.setText("\\n".join(links))
        parent.show_toast(f"Copied {len(links)} links!")
