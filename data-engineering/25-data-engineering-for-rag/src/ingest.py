import re
from collections import Counter
from hashlib import sha256
from fastembed import TextEmbedding
from kb import load, new_table

model = TextEmbedding("BAAI/bge-small-en-v1.5")
table = new_table()  # LanceDB, 384-dim vectors

def chunk(text, size=200, overlap=40):
    text = re.sub(r"(?m)^#.*|\*", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    step = size - overlap
    return [text[i:i + size] for i in
            range(0, len(text) - overlap, step)]

def ingest(docs, run):
    old = table.to_arrow().to_pydict()
    seen = dict(zip(old["source"], old["hash"]))
    rows, n = [], Counter()
    for d in docs:
        src, parts = d["source"], chunk(d["text"])
        h = sha256(d["text"].encode()).hexdigest()
        if seen.get(src) == h:
            n["skipped"] += len(parts)
            continue
        n["re-embedded" if src in seen
          else "created"] += len(parts)
        for i, v in enumerate(model.embed(parts)):
            rows += [{**d, "id": f"{src}#{i}",
                      "text": parts[i], "hash": h,
                      "vector": v}]
    if rows:
        (table.merge_insert("id")
         .when_matched_update_all()
         .when_not_matched_insert_all()
         .execute(rows))
    print(f"run {run}: {n['created']} created, "
          f"{n['re-embedded']} re-embedded, "
          f"{n['skipped']} skipped")

def ask(q):
    v = next(model.query_embed(q))
    hit = table.search(v).limit(1).to_list()[0]
    fact = hit["text"].split(".")[0]
    meta = f"{hit['source']}, {hit['updated_at']}"
    print(f"  {meta}: {fact}")

ingest(load("day1"), 1)
ingest(load("day1"), 2)  # nightly rerun
ask("How long is the refund window?")
ingest(load("day2"), 3)  # refunds.md edited
ids = table.to_arrow()["id"].to_pylist()
print(f"{len(ids)} rows, {len(set(ids))} unique")
ask("How long is the refund window?")
