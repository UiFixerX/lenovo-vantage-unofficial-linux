import glob
import subprocess
import os
import shutil


def detect_capabilities() -> dict:
    has_hwmon = len(glob.glob("/sys/class/hwmon/hwmon*")) > 0
    return {
        "supported": has_hwmon,
        "partial": not has_hwmon,
        "reason": "hwmon available" if has_hwmon else "hwmon unavailable"
    }


def read_hwmon(name: str, file: str) -> int | None:
    for path in glob.glob("/sys/class/hwmon/hwmon*"):
        try:
            with open(f"{path}/name") as f:
                if f.read().strip() == name:
                    with open(f"{path}/{file}") as f_val:
                        return int(f_val.read().strip())
        except (FileNotFoundError, ValueError):
            continue
    return None


def get_cpu_temp() -> float:
    raw = read_hwmon("k10temp", "temp1_input")
    if raw is None:
        raw = read_hwmon("coretemp", "temp1_input")
    return raw / 1000.0 if raw else 0.0


def get_gpu_temp() -> float:
    raw_dgpu = read_hwmon("nouveau", "temp1_input")
    if raw_dgpu:
        return raw_dgpu / 1000.0
    raw_igpu = read_hwmon("amdgpu", "temp1_input")
    return raw_igpu / 1000.0 if raw_igpu else 0.0


def get_cpu_usage() -> float:
    try:
        with open('/proc/stat', 'r') as f:
            line1 = f.readline()
        import time
        time.sleep(0.1)
        with open('/proc/stat', 'r') as f:
            line2 = f.readline()

        def parse(line):
            parts = line.split()[1:]
            vals = [int(x) for x in parts[:4]]
            idle = vals[3]
            total = sum(vals)
            return idle, total

        idle1, total1 = parse(line1)
        idle2, total2 = parse(line2)
        total_diff = total2 - total1
        idle_diff = idle2 - idle1
        if total_diff == 0:
            return 0.0
        return min(100.0, (1.0 - idle_diff / total_diff) * 100.0)
    except Exception:
        return 0.0


def get_gpu_usage() -> float:
    try:
        if shutil.which("nvidia-smi"):
            res = subprocess.run(
                ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
                capture_output=True, text=True
            )
            return float(res.stdout.strip())
    except Exception:
        pass
    return 0.0


def get_fan_rpm() -> int:
    for name in ["ideapad", "thinkpad", "legion", "asus"]:
        raw = read_hwmon(name, "fan1_input")
        if raw is not None:
            return raw
    return 0
