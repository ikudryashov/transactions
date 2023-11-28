import logging

import grpc
import os
from concurrent import futures

import grpc_output.sum_amount_pb2_grpc as sum_amount_grpc
from app.transactions_service import TransactionsServicer


class TransactionsServer:
    def __init__(self, port=os.environ["GRPC_PORT"], host=os.environ["GRPC_HOST"], max_workers=os.cpu_count()):
        self._port = port
        self._host = host
        self._max_workers = max_workers
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=self._max_workers))
        sum_amount_grpc.add_TransactionsServicer_to_server(TransactionsServicer(), self._server)

    def serve(self):
        self._server.add_insecure_port(f"{self._host}:{self._port}")
        self._server.start()
        logging.info(f"gRPC server started at {self._host}:{self._port}")
        self._server.wait_for_termination()
