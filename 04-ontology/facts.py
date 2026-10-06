# Instance data: rows from purchasing (ERP), product data (PLM)
# and orders (CRM), written as (subject, relation, object) triples.
FACTS = [
    ("Acme", "supplies", "bolt"),
    ("Acme", "supplies", "hinge"),
    ("Zenco", "supplies", "gasket"),
    ("bolt", "used_in", "Drone"),
    ("hinge", "used_in", "Locker"),
    ("gasket", "used_in", "Pump"),
    ("Drone", "ordered_by", "Kestrel"),
    ("Locker", "ordered_by", "Orbis"),
    ("Pump", "ordered_by", "Orbis"),
    ("Pump", "ordered_by", "Vela"),
]
