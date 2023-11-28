import logging
import os
import time
import uuid
import random
from decimal import Decimal
from typing import List
from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine, func, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from persistence.models import Transaction, User

db_uri = f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_URI']}/{os.environ['DB_NAME']}"

engine = create_engine(db_uri)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ensure_db_connected():
    connected = False
    retries = 5

    while not connected and retries > 0:
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                connected = True
        except OperationalError:
            logging.error("retrying db connection")
            retries -= 1
            time.sleep(2)

    if not connected:
        raise Exception("Failed to connect to the database after several retries.")


def ensure_database_is_populated() -> None:

    db = next(get_db())

    user_count = db.query(func.count(User.id)).scalar()
    transaction_count = db.query(func.count(Transaction.id)).scalar()

    if user_count < 1000 or transaction_count < 1000000:
        populate_database_with_fake_data(2000, 3000000, 5000)


def populate_database_with_fake_data(num_users: int, num_transactions: int, bulk_size: int) -> None:
    logging.info(f"generating {num_users} users and {num_transactions} transactions...")
    db = next(get_db())

    users = generate_users(num_users)
    db.bulk_save_objects(users)
    db.commit()
    logging.info(f"inserted users into the database")

    for i in range(0, num_transactions, bulk_size):
        transactions = generate_transactions(users, bulk_size)
        db.bulk_save_objects(transactions)
        db.commit()
        logging.info(f"inserted {i} transactions into the database")

    logging.info(f"inserted all transactions into the database")


def generate_users(n: int) -> List[User]:
    users = []
    for i in range(n):
        user = User(id=uuid.uuid4(), first_name=f"fist_name_{i}", last_name=f"last_name_{i}")
        logging.info(f"generated user {user.id}")
        users.append(user)
    return users


def generate_transactions(users: List[User], n: int) -> List[Transaction]:
    transactions = []

    for _ in range(n):
        sender = random.choice(users)
        receiver = random.choice(users)

        while sender == receiver:
            receiver = random.choice(users)

        transaction = Transaction(
            amount=Decimal(random.uniform(10.0, 5000.0)),
            sender_id=sender.id,
            receiver_id=receiver.id,
            timestamp=datetime(2023, 1, 1, random.randint(0, 23), random.randint(0, 59), 0, 0, tzinfo=timezone.utc)
            + timedelta(days=random.randint(0, 365)),
        )
        transactions.append(transaction)
    return transactions
