import grpc
import grpc_output.sum_amount_pb2 as sum_amount_proto
import grpc_output.sum_amount_pb2_grpc as sum_amount_grpc

from pydantic import ValidationError

from persistence.transactions_repository import TransactionsRepository
from validation.sum_amount_request import SumAmountRequest


class TransactionsServicer(sum_amount_grpc.TransactionsServicer):
    def __init__(self):
        self._transactions_repository = TransactionsRepository()

    def SumAmount(self, request, context):
        try:
            db_request = SumAmountRequest(
                user_uuid=request.user_uuid,
                timestamp_start_utc=request.timestamp_start_utc,
                timestamp_end_utc=request.timestamp_end_utc,
                direction=request.direction,
            )
        except ValidationError as e:
            error_message = e.json()

            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(error_message)

            return sum_amount_proto.SumAmountResponse()

        result = self._transactions_repository.get_transactions_sum(db_request)

        if not result.sum_amount:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User with this ID not found!")
            return sum_amount_proto.SumAmountResponse()

        return sum_amount_proto.SumAmountResponse(
            sum_amount=str(result.sum_amount), response_time_seconds=result.response_time_seconds
        )
