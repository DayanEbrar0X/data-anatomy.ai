# Company docs, already split into short chunks, plus the toy embedding.
import math
import re

DOCS = {
    "hr-1": "New hires get 15 vacation days a year",
    "hr-2": "Unused vacation days roll over",
    "hr-3": "Sick days need no manager approval",
    "hr-4": "Parental leave is 16 weeks, fully paid",
    "it-1": "New hires get a laptop on day one",
    "it-2": "Change your password every 90 days",
    "fin-1": "Expenses over 500 dollars need approval",
    "fin-2": "Book all travel in the finance portal",
}

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
