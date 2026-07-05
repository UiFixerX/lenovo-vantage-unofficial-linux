"""About page — app info, version, dependencies."""

from PyQt6.QtWidgets import QLabel, QFrame, QVBoxLayout

from i18n import tr
from gui.widgets import create_scroll_page


def create_about_page(gui):
    page, layout = create_scroll_page(tr("About"))

    frame = QFrame()
    frame.setObjectName("SettingsRow")
    v = QVBoxLayout(frame)
    v.setContentsMargins(30, 30, 30, 30)
    v.setSpacing(10)

    title = QLabel(tr("About app title"))
    title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
    v.addWidget(title)

    v.addWidget(QLabel(tr("About app desc")))
    v.addSpacing(15)
    v.addWidget(QLabel(f"<b>{tr('Version')}:</b> 1.0.0-initial-release"))
    v.addWidget(QLabel(f"<b>{tr('Backend')}:</b> D-Bus System Service"))
    v.addWidget(
        QLabel(
            f"<b>{tr('Dependencies')}:</b> "
            "supergfxctl, ryzenadj, power-profiles-daemon"
        )
    )

    lbl_github = QLabel(
        '<b>GitHub:</b> <a href="https://github.com/nightcodex7/'
        'lenovo-vantage-unofficial-linux" '
        'style="color: #0078d4; text-decoration: none;">'
        'nightcodex7/vantage</a>'
    )
    lbl_github.setOpenExternalLinks(True)
    v.addWidget(lbl_github)

    layout.addWidget(frame)
    layout.addStretch()
    return page
