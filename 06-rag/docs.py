# Company docs, already split into short chunks.
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
