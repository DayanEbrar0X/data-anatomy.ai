# Loads the company docs (already split into short chunks) and builds the vocabulary.
import json
import re
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "handbook.json"
DOCS = json.loads(DATA.read_text())

# vocabulary: every word in the docs, minus filler words
STOP = {"a", "all", "in", "is", "no", "on", "over", "the", "your"}
VOCAB = sorted({w for t in DOCS.values()
                for w in re.findall(r"[a-z]+", t.lower())} - STOP)
