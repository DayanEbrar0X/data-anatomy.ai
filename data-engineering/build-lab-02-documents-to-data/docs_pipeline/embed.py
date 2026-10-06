from fastembed import TextEmbedding

# small open model: runs on CPU, no API key
model = TextEmbedding("BAAI/bge-small-en-v1.5")


def embed(texts):
    # each text -> 384 numbers that capture meaning
    return [v.tolist() for v in model.embed(texts)]
