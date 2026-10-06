# Runs the code from the video and checks it prints exactly what the video shows.
import subprocess
import sys
from pathlib import Path

LESSON = Path(__file__).resolve().parents[1]


def run(script):
    result = subprocess.run([sys.executable, LESSON / script],
                            capture_output=True, text=True, check=True)
    return result.stdout


def test_learns_minutes_per_km():
    assert run("src/delivery.py") == (
        "mins = 2.98 * km + 4.21\n"
        "12 km: 39.9 min\n"
    )


def test_short_version():
    assert run("short/learn.py") == (
        "12 km: 40.1 min\n"
    )
