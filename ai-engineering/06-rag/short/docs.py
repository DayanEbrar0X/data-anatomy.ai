# Loads the company docs (already split into short chunks), plus the toy embedding.
import json
import math
import re
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "handbook.json"
DOCS = json.loads(DATA.read_text())

# vocabulary: every word in the docs, minus filler words
STOP = {"a", "all", "in", "is", "no", "on", "over", "the", "your"}
VOCAB = sorted({w for t in DOCS.values()
                for w in re.findall(r"[a-z]+", t.lower())} - STOP)


def embed(text):
    # toy embedding: count each vocabulary word (real systems use a learned model)
    words = re.findall(r"[a-z]+", text.lower())
    return [words.count(w) for w in VOCAB]


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.hypot(*a) * math.hypot(*b))
