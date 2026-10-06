# Runs the code from the video and checks it prints exactly what the video shows.
import subprocess
import sys
from pathlib import Path

LESSON = Path(__file__).resolve().parents[1]


def run(script):
    result = subprocess.run([sys.executable, LESSON / script],
                            capture_output=True, text=True, check=True)
    return result.stdout


def test_agent_answers_in_three_steps():
    assert run("src/agent.py") == (
        "0 search -> Q3 revenue: 4200000\n"
        "1 calc -> 630000.0\n"
        "answer: $630,000\n"
    )
