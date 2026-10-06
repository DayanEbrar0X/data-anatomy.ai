from facts import FACTS

# the ontology: types, and how they connect
ONTOLOGY = [("Supplier", "supplies", "Part"),
            ("Part", "used_in", "Product"),
            ("Product", "ordered_by", "Customer")]

def follow(start, path):
    found = {start}
    for rel in path:
        found = {o for s, r, o in FACTS
                 if s in found and r == rel}
        print(rel, "->", sorted(found))
    return sorted(found)

path = [rel for _, rel, _ in ONTOLOGY]
print("affected:", follow("Acme", path))
