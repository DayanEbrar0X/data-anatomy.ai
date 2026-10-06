# Runs the code from the video and checks it prints exactly what the video shows.
import subprocess
import sys
from pathlib import Path

LESSON = Path(__file__).resolve().parents[1]


def run(script):
    result = subprocess.run([sys.executable, LESSON / script],
                            capture_output=True, text=True, check=True)
    return result.stdout


def test_retrieves_the_vacation_policy():
    assert run("src/rag.py") == (
        "hr-1 0.91 New hires get 15 vacation days a year\n"
        "it-1 0.55 New hires get a laptop on day one\n"
        "sources: hr-1 it-1\n"
    )


def test_short_version():
    assert run("short/rag.py") == (
        "New hires get 15 vacation days a year\n"
        "source: hr-1 0.91\n"
    )
