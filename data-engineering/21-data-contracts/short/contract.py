from typing import Literal
from pydantic import BaseModel, StrictInt
from shop import oct8, run
class Order(BaseModel):  # the contract
    order_id: StrictInt
    amount: float  # required, never null
    status: Literal["paid", "refunded"]
run(oct8)  # no contract
run(oct8, check=Order.model_validate)
