from pydantic import BaseModel, UUID4, model_validator
from datetime import datetime
from enum import Enum


class Direction(str, Enum):
    SENDER = "sender"
    RECEIVER = "receiver"


class SumAmountRequest(BaseModel):
    user_uuid: UUID4
    timestamp_start_utc: datetime
    timestamp_end_utc: datetime
    direction: Direction

    @model_validator(mode='after')
    def validate_timestamps(self):
        start = self.timestamp_start_utc
        end = self.timestamp_end_utc

        if start >= end:
            raise ValueError("Start timestamp must be earlier than end timestamp")

        return self
