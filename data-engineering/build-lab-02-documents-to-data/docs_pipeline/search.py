from embed import embed
from store import build_index

table = build_index()
print(len(table), "invoices embedded, 384 dims")

q = "Which invoices were for caffeine?"
print("Q:", q)
hits = (table.search(embed([q])[0])
        .distance_type("cosine").limit(2).to_list())
for h in hits:
    score = round(1 - h["_distance"], 2)
    print(h["invoice_no"], h["vendor"], score)

ctx = "\n".join(f"[{h['invoice_no']}] {h['text']}"
                for h in hits)
prompt = ("Answer from these invoices only. "
          "Cite invoice numbers.\n\n"
          f"{ctx}\n\nQ: {q}")
# in production, this prompt goes to the LLM
ids = " ".join(f"[{h['invoice_no']}]" for h in hits)
print(f"prompt: {len(prompt)} chars, sources {ids}")
