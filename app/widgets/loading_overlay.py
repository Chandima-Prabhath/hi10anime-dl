from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer, QRectF
from PyQt6.QtGui import QColor, QPainter, QPen
from ..styles import StyleSheet


class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.hide()

        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)

        self.text_label = QLabel("Loading...", self)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; background: transparent;"
        )

        self.bg_color = QColor(0, 0, 0, 150)
        self.spinner_color = QColor("#89b4fa")

    def update_theme(self, theme):
        colors = StyleSheet.get_colors(theme)
        if theme == "Dark":
            self.bg_color = QColor(30, 30, 46, 210)
        else:
            self.bg_color = QColor(255, 255, 255, 220)

        self.spinner_color = QColor(colors["spinner"])
        self.text_label.setStyleSheet(
            f"color: {colors['fg']}; font-size: 16px; font-weight: bold; background: transparent;"
        )
        self.update()

    def rotate(self):
        self.angle = (self.angle + 10) % 360
        self.update()

    def show_loading(self, text="Loading..."):
        self.text_label.setText(text)
        self.resize(self.parent().size())
        self.show()
        self.raise_()
        self.timer.start(30)

    def stop(self):
        self.timer.stop()
        self.hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), self.bg_color)

        size = 60
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2 - 20
        rect = QRectF(x, y, size, size)

        pen = QPen(self.spinner_color)
        pen.setWidth(6)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        start_angle = -self.angle * 16
        span_angle = 270 * 16
        painter.drawArc(rect, start_angle, span_angle)

        self.text_label.setGeometry(0, y + size + 15, self.width(), 30)
