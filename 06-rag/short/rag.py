from docs import DOCS, embed, cosine
ask = "How many vacation days do new hires get?"
q = embed(ask)
scores = {d: cosine(q, embed(t))
          for d, t in DOCS.items()}
best = max(scores, key=scores.get)
prompt = f"{DOCS[best]}\n\nQuestion: {ask}"
print(DOCS[best])
print("source:", best, round(scores[best], 2))
