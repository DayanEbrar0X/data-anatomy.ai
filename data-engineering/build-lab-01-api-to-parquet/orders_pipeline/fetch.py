import json
from pathlib import Path

def fetch_orders():
    rows, page = [], 1
    while page:
        # prod: requests.get(URL, params=...)
        raw = Path(f"api/orders_p{page}.json")
        body = json.loads(raw.read_text())
        rows += body["data"]
        page = body["next_page"]
    return rows
