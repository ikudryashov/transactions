from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class SumAmountResponse(BaseModel):
    sum_amount: Optional[Decimal]
    response_time_seconds: float
