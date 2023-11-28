FROM python:3.8

WORKDIR /grpc_app

COPY ./src /grpc_app/src
COPY pyproject.toml /grpc_app

RUN pip install --upgrade pip
RUN pip install -e .

ENV PYTHONPATH "${PYTHONPATH}:/grpc_app/src"

CMD ["python", "src/app/__main__.py"]