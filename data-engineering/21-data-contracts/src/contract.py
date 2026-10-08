import json
from typing import Literal
from pydantic import BaseModel, StrictInt
from pydantic import ValidationError
from shop import warehouse, load, report

class Order(BaseModel):  # the contract
    order_id: StrictInt
    amount: float  # required, never null
    status: Literal["paid", "refunded"]

oct8 = json.load(open("oct8.json"))

db = warehouse()  # Oct 7 already loaded
load(db, oct8)    # no contract
report(db, "no contract:")

db = warehouse()
try:
    for row in oct8:
        Order.model_validate(row)
    load(db, oct8)  # only if every row passes
except ValidationError as e:
    print("Oct 8 rejected before load:")
    for err in e.errors():
        field = err["loc"][0]
        print(f"  {field}: {err['msg']}")
report(db, "with contract:")
