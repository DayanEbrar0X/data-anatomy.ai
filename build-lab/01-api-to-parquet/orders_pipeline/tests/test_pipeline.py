# Checks each step of the pipeline, then runs the whole thing like the video does.
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))

from fetch import fetch_orders  # noqa: E402
from transform import clean  # noqa: E402


def test_fetch_reads_every_page(monkeypatch):
    monkeypatch.chdir(PROJECT)
    assert len(fetch_orders()) == 122


def test_clean_fixes_types_and_drops_duplicates(monkeypatch):
    monkeypatch.chdir(PROJECT)
    df = clean(fetch_orders())
    assert len(df) == 120
    assert df["order_id"].is_unique
    assert df["amount"].dtype == float
    assert str(df["created"].dtype).startswith("datetime64")


def test_main_prints_what_the_video_shows():
    result = subprocess.run([sys.executable, "main.py"], cwd=PROJECT,
                            capture_output=True, text=True, check=True)
    assert result.stdout == (
        "122 rows fetched, 120 kept\n"
        "JSON 19.0 KB -> Parquet 5.6 KB\n"
        "[('paid', 99), ('refunded', 21)]\n"
    )
