# transactions
The project includes a Python gRPC service and a PostgreSQL database that can be ran alongside in Docker containers, to calculate the sum of transaction amounts on a large dataset
## Database
- The database is initialized with 2 tables: "Users" and "Transactions" with an entrypoint .sql script. Each user can be a sender or a receiver in a transaction
- "Transations" table is indexed on it's "timestamp" column with a [BRIN index](https://www.postgresql.org/docs/current/brin-intro.html), which performs well on time series data, and default B-tree indices on sender and receiver ids
- "Transations" table is partitioned by "timestamp" column. Partitioning is done with [pg_partman](https://github.com/pgpartman/pg_partman) PostgreSQL extension, which is installed on container startup, it creates daily partitions from 01-01-2023 and 30 extra ones for future data inserts
- A cron job is set up with [pg_cron](https://github.com/citusdata/pg_cron) extension to create more partitions for future inserts
- Database can be queried directly on port **5432** to validate app's responses
## gRPC service
- A Python gRPC service that can retrieve the sum of transactions amount for a user in specified time range
- Request schema for SumAmount servicer (.proto file can be found in source code):
```
{
  user_uuid
  timestamp_start_utc // ISO format - "2023-06-01T00:00:00"
  timestamp_end_utc
  string direction // "sender" or "receiver"
}
```
- App uses SQLAlchemy to connect to and query the database and Pydantic for request validation
- On startup app checks the amount of records in "Users" and "Transactions" table, and generates **2 000** users and **3 000 000** transactions if needed. It can take a few minutes (view container log for data generation progress)
- Once fake data is generated, app starts a gRPC service that listens on port **50051** and is ready to receive requests
- The app returns the total amount of transactions a user made in specified timeframe + time the database took to produce a result:
```
{
    "sum_amount": "871705.91465",
    "response_time_seconds": 0.05963873863220215
}
```
## Run the project
- clone the repo
- run ```docker-compose up```
- wait until dummy users and transactions are generated if you launched the project 1st time (view gRPC service container logs for progress)
- grab any user uuid from gRPC service container logs
- query the app via Postman at localhost:50051
- query the database at localhost:5432
Query example:
<img width="1453" alt="SCR-20231128-qjzb" src="https://github.com/ikudryashov/transactions/assets/87234755/7437f541-1795-4795-9841-fba7f0781218">
## How can it be improved?
- Add unit tests for the transactions repository with mock database object
- Add unit tests for the gRPC servicer to test request validation
- Make I/O async with asyncio and sqlalchemy
- Use more linters - add flake8 and mypy
- Add pre-commit git hook for linters
