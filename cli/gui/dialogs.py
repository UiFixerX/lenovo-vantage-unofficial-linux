"""Reusable dialogs for Vantage GUI."""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
)
from PyQt6.QtCore import Qt

from i18n import tr


class LanguageDialog(QDialog):
    """First-run language selection dialog."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("Language dialog title"))
        self.setModal(True)
        self.setFixedSize(360, 200)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        label = QLabel(tr("Language dialog text"))
        label.setObjectName("DialogLabel")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.btn_en = QPushButton("English")
        self.btn_en.setMinimumHeight(40)
        self.btn_en.clicked.connect(lambda: self._choose("en"))
        btn_row.addWidget(self.btn_en)

        self.btn_ru = QPushButton("Русский")
        self.btn_ru.setMinimumHeight(40)
        self.btn_ru.clicked.connect(lambda: self._choose("ru"))
        btn_row.addWidget(self.btn_ru)

        layout.addLayout(btn_row)

        self._chosen = None

    def _choose(self, code):
        self._chosen = code
        self.accept()

    def chosen(self):
        return self._chosen
