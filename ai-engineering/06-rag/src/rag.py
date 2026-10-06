import math, re
from docs import DOCS, VOCAB

def embed(text):
    words = re.findall(r"[a-z]+", text.lower())
    return [words.count(w) for w in VOCAB]

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.hypot(*a) * math.hypot(*b))

ask = "How many vacation days do new hires get?"
q = embed(ask)
scores = {d: cosine(q, embed(t))
          for d, t in DOCS.items()}
top = sorted(scores, key=scores.get,
             reverse=True)[:2]
context = "\n".join(DOCS[d] for d in top)
prompt = f"{context}\n\nQuestion: {ask}"
for d in top:
    print(d, f"{scores[d]:.2f}", DOCS[d])
print("sources:", *top)
