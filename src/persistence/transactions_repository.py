from persistence.database import get_db
from persistence.models import Transaction
from validation.sum_amount_request import SumAmountRequest
from decimal import Decimal, ROUND_DOWN
from sqlalchemy import and_, func
import time

from validation.sum_amount_response import SumAmountResponse


class TransactionsRepository:
    def __init__(self):
        self._db = next(get_db())

    def get_transactions_sum(self, request: SumAmountRequest) -> SumAmountResponse:
        filter_conditions = [
            Transaction.timestamp >= request.timestamp_start_utc,
            Transaction.timestamp <= request.timestamp_end_utc,
        ]

        if request.direction == "sender":
            filter_conditions.append(Transaction.sender_id == request.user_uuid)
        else:
            filter_conditions.append(Transaction.receiver_id == request.user_uuid)

        query_start_time = time.time()
        sum_amount = self._db.query(func.sum(Transaction.amount)).filter(and_(*filter_conditions)).scalar()
        query_finish_time = time.time()

        query_duration = query_finish_time - query_start_time

        return SumAmountResponse(
            sum_amount=Decimal(sum_amount).quantize(Decimal("0.00001"), rounding=ROUND_DOWN) if sum_amount else None,
            response_time_seconds=query_duration,
        )
