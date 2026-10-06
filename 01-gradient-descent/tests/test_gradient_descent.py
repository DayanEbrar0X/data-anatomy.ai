# Runs the code from the video and checks it prints exactly what the video shows.
import subprocess
import sys
from pathlib import Path

LESSON = Path(__file__).resolve().parents[1]


def run(script):
    result = subprocess.run([sys.executable, LESSON / script],
                            capture_output=True, text=True, check=True)
    return result.stdout


def test_loss_drops_to_almost_zero():
    assert run("src/descent.py") == (
        "20.8 -> 0.0001\n"
    )
