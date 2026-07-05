"""Actions & Automation page — placeholder for future automation engine."""

from PyQt6.QtWidgets import QComboBox, QLabel

from i18n import tr
from gui.widgets import create_row, create_scroll_page, set_row_state


def create_actions_page(gui):
    page, layout = create_scroll_page(tr("Actions & Automation"))

    lbl_info = QLabel(tr("Actions info"))
    lbl_info.setStyleSheet("color: #aaaaaa; margin-bottom: 10px;")
    layout.addWidget(lbl_info)

    mt = QComboBox()
    mt.addItems(["Disabled"])
    mt.setEnabled(False)
    mt_row = create_row(
        tr("Master Toggle"), tr("Master Toggle subtitle"), mt
    )
    set_row_state(mt_row, False)
    layout.addWidget(mt_row)

    lbl_trig = QLabel(tr("Triggers & Actions"))
    lbl_trig.setObjectName("SectionTitle")
    layout.addWidget(lbl_trig)

    tr_combo = QComboBox()
    tr_combo.addItems(["AC Connected", "AC Disconnected"])
    tr_combo.setEnabled(False)
    tr_row = create_row(
        tr("Available Triggers"), tr("Available Triggers subtitle"), tr_combo
    )
    set_row_state(tr_row, False)
    layout.addWidget(tr_row)

    ac = QComboBox()
    ac.addItems(["Set Power Mode", "Set GPU Mode"])
    ac.setEnabled(False)
    ac_row = create_row(
        tr("Mapped Actions"), tr("Mapped Actions subtitle"), ac
    )
    set_row_state(ac_row, False)
    layout.addWidget(ac_row)

    layout.addStretch()
    return page
