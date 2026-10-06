# Runs the code from the video and checks it prints exactly what the video shows.
import subprocess
import sys
from pathlib import Path

LESSON = Path(__file__).resolve().parents[1]


def run(script):
    result = subprocess.run([sys.executable, LESSON / script],
                            capture_output=True, text=True, check=True)
    return result.stdout


def test_pass_rate_climbs_to_100():
    assert run("src/evals.py") == (
        "v1 pass rate 60%\n"
        "v2 pass rate 80%\n"
        "v3 pass rate 100%\n"
    )


def test_short_version():
    assert run("short/loop.py") == (
        "60% pass\n"
        "80% pass\n"
        "100% pass\n"
    )
