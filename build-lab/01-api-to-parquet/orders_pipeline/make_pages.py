# Builds the recorded API responses used by the episode (3 pages, 2 duplicate orders across pages).
import json
import random
from pathlib import Path

random.seed(7)
customers = ["Acme", "Kestrel", "Orbis", "Vela", "Zenco", "Nimbus"]
orders = []
for i in range(1, 121):
    orders.append({
        "order_id": f"A-{1000 + i}",
        "customer": random.choice(customers),
        "amount": f"{random.uniform(8, 240):.2f}",
        "created": f"2026-09-{random.randint(1, 30):02d}T{random.randint(8, 20):02d}:{random.randint(0, 59):02d}:00Z",
        "status": random.choice(["paid", "paid", "paid", "refunded"]),
    })
pages = [orders[0:40], orders[40:80], orders[80:120]]
pages[1].append(dict(orders[39]))  # the API repeats an order at a page boundary
pages[2].append(dict(orders[79]))
Path("api").mkdir(exist_ok=True)
for n, rows in enumerate(pages, 1):
    nxt = n + 1 if n < 3 else None
    Path(f"api/orders_p{n}.json").write_text(json.dumps({"data": rows, "next_page": nxt}, indent=2))
