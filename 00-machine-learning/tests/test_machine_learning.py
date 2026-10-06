# Runs the code from the video and checks it prints exactly what the video shows.
import subprocess
import sys
from pathlib import Path

LESSON = Path(__file__).resolve().parents[1]


def run(script):
    result = subprocess.run([sys.executable, LESSON / script],
                            capture_output=True, text=True, check=True)
    return result.stdout


def test_learns_the_price_rule():
    assert run("src/learn.py") == (
        "price = 3.33 * size + 2.44\n"
    )
