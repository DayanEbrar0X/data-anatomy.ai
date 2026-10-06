from facts import FACTS

found = {"Acme"}
for rel in ["supplies", "used_in", "ordered_by"]:
    found = {o for s, r, o in FACTS
             if s in found and r == rel}
print("affected:", sorted(found))
