from pipeline import load, stored, embed
from pipeline import upsert, ask
for day in ["day1", "day1", "day2"]:
    seen = stored()  # source -> hash, in LanceDB
    docs = [d for d in load(day)
            if seen.get(d["source"]) != d["hash"]]
    rows = upsert(embed(docs))  # key: chunk id
    print(f"{day}: {len(rows)} chunks embedded")
ask("How long is the refund window?")
