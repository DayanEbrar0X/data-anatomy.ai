# The same ingestion steps as the full episode (src/ingest.py):
# clean + chunk with overlap, sha256 content hash, bge-small
# embeddings, a LanceDB table upserted on the chunk id.
import re
from hashlib import sha256

from fastembed import TextEmbedding

import kb

model = TextEmbedding("BAAI/bge-small-en-v1.5")
table = kb.new_table()


def load(day):
    return [{**d, "hash": sha256(d["text"].encode()).hexdigest()}
            for d in kb.load(day)]


def chunk(text, size=200, overlap=40):
    text = re.sub(r"(?m)^#.*|\*", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    step = size - overlap
    return [text[i:i + size]
            for i in range(0, len(text) - overlap, step)]


def stored():
    old = table.to_arrow().to_pydict()
    return dict(zip(old["source"], old["hash"]))


def embed(docs):
    rows = []
    for d in docs:
        parts = chunk(d["text"])
        for i, v in enumerate(model.embed(parts)):
            rows.append({**d, "id": f"{d['source']}#{i}",
                         "text": parts[i], "vector": v})
    return rows


def upsert(rows):
    if rows:
        (table.merge_insert("id").when_matched_update_all()
         .when_not_matched_insert_all().execute(rows))
    return rows


def ask(q):
    hit = table.search(next(model.query_embed(q))).limit(1).to_list()[0]
    fact = hit["text"].split(".")[0]
    print(f"  {hit['source']}, {hit['updated_at']}: {fact}")
