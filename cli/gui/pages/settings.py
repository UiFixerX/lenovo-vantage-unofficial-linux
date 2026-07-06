"""Settings page — language, theme, tray, autorun, boot logo."""

from PyQt6.QtWidgets import QComboBox, QLabel, QMessageBox, QCheckBox
from PyQt6.QtCore import Qt

from i18n import (
    tr, save_locale, set_locale, get_locale, save_theme, load_tray,
)
from gui.widgets import create_row, create_scroll_page, set_row_state


def create_settings_page(gui):
    page, layout = create_scroll_page(tr("Settings"))

    _build_general_section(gui, layout)
    _build_behavior_section(gui, layout)

    layout.addStretch()
    return page


def _build_general_section(gui, layout):
    lbl = QLabel(tr("General"))
    lbl.setObjectName("SectionTitle")
    layout.addWidget(lbl)

    lang = QComboBox()
    lang.addItems([tr("System Default"), tr("English"), tr("Russian")])
    current_lang = get_locale()
    if current_lang == "ru":
        lang.setCurrentIndex(2)
    elif current_lang == "en":
        lang.setCurrentIndex(1)
    else:
        lang.setCurrentIndex(0)
    lang.currentIndexChanged.connect(lambda idx: _on_language_changed(gui, idx))
    layout.addWidget(create_row(tr("Language"), tr("Language subtitle"), lang))

    theme = QComboBox()
    theme.addItems([tr("Dark Theme"), tr("Light Theme"), tr("System Default")])
    theme.setCurrentIndex(1 if gui.current_theme == "light" else 0)
    theme.currentIndexChanged.connect(lambda idx: _on_theme_changed(gui, idx))
    layout.addWidget(create_row(tr("Theme"), tr("Theme subtitle"), theme))


def _build_behavior_section(gui, layout):
    lbl = QLabel(tr("Behavior"))
    lbl.setObjectName("SectionTitle")
    layout.addWidget(lbl)

    tray_check = QCheckBox()
    tray_check.setChecked(load_tray())
    if not gui.tray_available:
        tray_check.setEnabled(False)
        tray_check.setChecked(False)
    tray_check.toggled.connect(lambda checked: gui.set_tray_enabled(checked))
    tray_row = create_row(
        tr("System Tray"), tr("System Tray subtitle"), tray_check
    )
    if not gui.tray_available:
        set_row_state(tray_row, False)
    layout.addWidget(tray_row)

    autorun = QComboBox()
    autorun.addItems(["Off"])
    autorun.setEnabled(False)
    autorun_row = create_row(tr("Autorun"), tr("Autorun subtitle"), autorun)
    set_row_state(autorun_row, False)
    layout.addWidget(autorun_row)

    bl = QComboBox()
    bl.addItems(["Disabled"])
    bl.setEnabled(False)
    bl_row = create_row(tr("Boot Logo"), tr("Boot Logo subtitle"), bl)
    set_row_state(bl_row, False)
    layout.addWidget(bl_row)


def _on_language_changed(gui, index):
    if index == 2:
        save_locale("ru")
        set_locale("ru")
    elif index == 1:
        save_locale("en")
        set_locale("en")
    else:
        return

    import sys, os, subprocess

    script = os.path.abspath(sys.argv[0]) if sys.argv[0] else None
    if not script or not os.path.exists(script):
        return

    subprocess.Popen([sys.executable, script])
    os._exit(0)


def _on_theme_changed(gui, index):
    if index == 1:
        gui.current_theme = "light"
    elif index == 0:
        gui.current_theme = "dark"
    else:
        from gui.styles import detect_system_theme
        gui.current_theme = detect_system_theme()
    gui._apply_theme(gui.current_theme)
    save_theme(gui.current_theme)
