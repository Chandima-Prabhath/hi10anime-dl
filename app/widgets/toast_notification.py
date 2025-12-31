from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve


class ToastNotification(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.SubWindow)
        self.setObjectName("toastFrame")

        self.label = QLabel(self)
        self.label.setStyleSheet(
            "border: none; background: transparent; font-weight: 600;"
        )

        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.setContentsMargins(20, 10, 20, 10)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.fade_out)
        self.hide()

    def update_theme(self, theme):
        self.style().unpolish(self)
        self.style().polish(self)

    def show_message(self, message, duration=2500):
        self.label.setText(message)
        self.adjustSize()
        parent_geo = self.parent().geometry()
        x = (parent_geo.width() - self.width()) // 2
        y = parent_geo.height() - self.height() - 60
        self.move(x, y)
        self.show()
        self.raise_()
        self.opacity_effect.setOpacity(1.0)
        self.timer.start(duration)

    def fade_out(self):
        self.anim.setDuration(500)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.anim.finished.connect(self.hide)
        self.anim.start()
