import logging

from transactions_server import TransactionsServer
from persistence.database import ensure_database_is_populated, ensure_db_connected

logging.basicConfig(level=logging.INFO)

logging.info("checking to see if database is ready to accept connections")
ensure_db_connected()

logging.info("checking to see if database has enough fake data")
ensure_database_is_populated()

logging.info("starting gRPC server")
transactions_server = TransactionsServer()
transactions_server.serve()
