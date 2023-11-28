import uuid

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, BigInteger, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "data"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = {"schema": "data"}

    id = Column(BigInteger, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    amount = Column(DECIMAL, nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("data.users.id"), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("data.users.id"), nullable=False)
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
