# Runs the code from the video and checks it prints exactly what the video shows.
import subprocess
import sys
from pathlib import Path

LESSON = Path(__file__).resolve().parents[1]


def run(script):
    result = subprocess.run([sys.executable, LESSON / script],
                            capture_output=True, text=True, check=True)
    return result.stdout


def test_follows_three_hops():
    assert run("src/ontology.py") == (
        "supplies -> ['bolt', 'hinge']\n"
        "used_in -> ['Drone', 'Locker']\n"
        "ordered_by -> ['Kestrel', 'Orbis']\n"
        "affected: ['Kestrel', 'Orbis']\n"
    )


def test_short_version():
    assert run("short/ontology.py") == (
        "affected: ['Kestrel', 'Orbis']\n"
    )
