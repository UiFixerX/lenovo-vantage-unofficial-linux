"""Dashboard page — real-time telemetry + quick controls."""

from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QLabel, QComboBox, QProgressBar, QFrame,
    QVBoxLayout, QHBoxLayout,
)
from PyQt6.QtCore import Qt

from i18n import tr
from gui.widgets import create_row, create_scroll_page


def create_dashboard_page(gui):
    """Build the dashboard page.  ``gui`` is the VantageGUI main window."""
    page, layout = create_scroll_page(tr("Dashboard"))

    lbl_model = QLabel(get_laptop_model())
    lbl_model.setObjectName("DeviceSubtitle")
    layout.addWidget(lbl_model)

    # ── System Monitoring ────────────────────────────────────────────
    dash_group = QFrame()
    dash_group.setObjectName("DashboardCard")
    dash_layout = QHBoxLayout(dash_group)
    dash_layout.setContentsMargins(25, 25, 25, 25)
    dash_layout.setSpacing(40)

    # CPU
    cpu_w = QWidget()
    cpu_l = QGridLayout(cpu_w)
    cpu_l.setContentsMargins(0, 0, 0, 0)
    cpu_l.setVerticalSpacing(18)
    cpu_title = QLabel(tr("CPU"))
    cpu_title.setObjectName("MonitorTitle")
    cpu_l.addWidget(cpu_title, 0, 0, 1, 3)

    cpu_lbl_util = QLabel(tr("Utilization"))
    cpu_lbl_util.setObjectName("MonitorLabel")
    cpu_l.addWidget(cpu_lbl_util, 1, 0)
    gui.pb_cpu = QProgressBar()
    gui.pb_cpu.setFixedHeight(8)
    gui.pb_cpu.setRange(0, 100)
    cpu_l.addWidget(gui.pb_cpu, 1, 1)
    gui.lbl_cpu_util = QLabel("0.0%")
    gui.lbl_cpu_util.setAlignment(
        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
    )
    cpu_l.addWidget(gui.lbl_cpu_util, 1, 2)

    cpu_lbl_temp = QLabel(tr("Temperature"))
    cpu_lbl_temp.setObjectName("MonitorLabel")
    cpu_l.addWidget(cpu_lbl_temp, 2, 0)
    gui.pb_cput = QProgressBar()
    gui.pb_cput.setFixedHeight(8)
    gui.pb_cput.setRange(0, 100)
    cpu_l.addWidget(gui.pb_cput, 2, 1)
    gui.lbl_cpu_temp = QLabel("0.0 °C")
    gui.lbl_cpu_temp.setAlignment(
        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
    )
    cpu_l.addWidget(gui.lbl_cpu_temp, 2, 2)

    cpu_lbl_fan = QLabel(tr("Fan"))
    cpu_lbl_fan.setObjectName("MonitorLabel")
    cpu_l.addWidget(cpu_lbl_fan, 3, 0)
    gui.pb_cpuf = QProgressBar()
    gui.pb_cpuf.setFixedHeight(8)
    gui.pb_cpuf.setRange(0, 5000)
    cpu_l.addWidget(gui.pb_cpuf, 3, 1)
    gui.lbl_cpu_fan = QLabel("— RPM")
    gui.lbl_cpu_fan.setAlignment(
        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
    )
    cpu_l.addWidget(gui.lbl_cpu_fan, 3, 2)

    dash_layout.addWidget(cpu_w)

    # GPU
    gpu_w = QWidget()
    gpu_l = QGridLayout(gpu_w)
    gpu_l.setContentsMargins(0, 0, 0, 0)
    gpu_l.setVerticalSpacing(18)
    gpu_title = QLabel(tr("GPU"))
    gpu_title.setObjectName("MonitorTitle")
    gpu_l.addWidget(gpu_title, 0, 0, 1, 3)

    gpu_lbl_util = QLabel(tr("Utilization"))
    gpu_lbl_util.setObjectName("MonitorLabel")
    gpu_l.addWidget(gpu_lbl_util, 1, 0)
    gui.pb_gpu = QProgressBar()
    gui.pb_gpu.setFixedHeight(8)
    gui.pb_gpu.setRange(0, 100)
    gpu_l.addWidget(gui.pb_gpu, 1, 1)
    gui.lbl_gpu_util = QLabel("0.0%")
    gui.lbl_gpu_util.setAlignment(
        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
    )
    gpu_l.addWidget(gui.lbl_gpu_util, 1, 2)

    gpu_lbl_temp = QLabel(tr("Temperature"))
    gpu_lbl_temp.setObjectName("MonitorLabel")
    gpu_l.addWidget(gpu_lbl_temp, 2, 0)
    gui.pb_gput = QProgressBar()
    gui.pb_gput.setFixedHeight(8)
    gui.pb_gput.setRange(0, 100)
    gpu_l.addWidget(gui.pb_gput, 2, 1)
    gui.lbl_gpu_temp = QLabel("0.0 °C")
    gui.lbl_gpu_temp.setAlignment(
        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
    )
    gpu_l.addWidget(gui.lbl_gpu_temp, 2, 2)

    gpu_lbl_fan = QLabel(tr("Fan"))
    gpu_lbl_fan.setObjectName("MonitorLabel")
    gpu_l.addWidget(gpu_lbl_fan, 3, 0)
    gui.pb_gpuf = QProgressBar()
    gui.pb_gpuf.setFixedHeight(8)
    gui.pb_gpuf.setRange(0, 5000)
    gpu_l.addWidget(gui.pb_gpuf, 3, 1)
    gui.lbl_gpu_fan = QLabel("— RPM")
    gui.lbl_gpu_fan.setAlignment(
        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
    )
    gpu_l.addWidget(gui.lbl_gpu_fan, 3, 2)

    dash_layout.addWidget(gpu_w)
    layout.addWidget(dash_group)

    # ── Quick Controls ───────────────────────────────────────────────
    lbl_qc = QLabel(tr("Quick Controls"))
    lbl_qc.setObjectName("SectionTitle")
    layout.addWidget(lbl_qc)

    pm = QComboBox()
    pm.addItems(["Quiet", "Balance", "Performance"])
    gui.pm_combos.append(pm)
    pm.currentIndexChanged.connect(gui.auto_apply_change)
    gui.rows['power_dash'] = create_row(
        tr("Power Mode"), tr("Power Mode subtitle"), pm
    )
    layout.addWidget(gui.rows['power_dash'])

    gm = QComboBox()
    gm.addItems(["Hybrid", "Integrated", "Dedicated"])
    gui.gpu_combos.append(gm)
    gm.currentIndexChanged.connect(gui.auto_apply_change)
    gui.rows['gpu_dash'] = create_row(
        tr("GPU Working Mode"), tr("GPU Working Mode subtitle"), gm
    )
    layout.addWidget(gui.rows['gpu_dash'])

    fm = QComboBox()
    fm.addItems(["Standard", "Super Silent", "Dust Cleaning", "Performance"])
    gui.fan_combos.append(fm)
    fm.currentIndexChanged.connect(gui.auto_apply_change)
    gui.rows['fan_dash'] = create_row(
        tr("Active Cooling Policy"), tr("Active Cooling Policy subtitle"), fm
    )
    layout.addWidget(gui.rows['fan_dash'])

    layout.addStretch()
    return page


def get_laptop_model():
    import os
    try:
        with open("/sys/class/dmi/id/product_version") as f:
            val = f.read().strip()
            if val and val.lower() != "lenovo" and val != "None":
                return val
    except Exception:
        pass
    try:
        with open("/sys/class/dmi/id/product_name") as f:
            name = f.read().strip()
        try:
            with open("/sys/class/dmi/id/product_family") as f:
                family = f.read().strip()
            if family and family.lower() != "lenovo":
                return f"{family} ({name})"
        except Exception:
            pass
        return name
    except Exception:
        return tr("Device subtitle fallback")
