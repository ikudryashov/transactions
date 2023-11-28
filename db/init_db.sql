
CREATE DATABASE transactions_db;
\c transactions_db;

CREATE SCHEMA data;

CREATE TABLE data.users (
    id UUID,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    CONSTRAINT pk_users PRIMARY KEY (id)
);

CREATE TABLE data.transactions (
    id BIGSERIAL,
    amount DECIMAL NOT NULL,
    sender_id UUID NOT NULL,
    receiver_id UUID NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    CONSTRAINT pk_transactions PRIMARY KEY (id, timestamp),
    CONSTRAINT fk_sender_id FOREIGN KEY(sender_id) REFERENCES data.users (id),
    CONSTRAINT fk_receiver_id FOREIGN KEY(receiver_id) REFERENCES data.users (id)
) PARTITION BY RANGE(timestamp);

CREATE INDEX sender_id_index ON data.transactions
    USING btree (sender_id, "timestamp" DESC);

CREATE INDEX receiver_id_index ON data.transactions
    USING btree (receiver_id, "timestamp" DESC);

--BRIN index is more efficient for time series datasets
CREATE INDEX timestamp_index ON data.transactions
    USING BRIN (timestamp) WITH (pages_per_range = 92);

--Create partitions for each day from 2023-01-01 + 30 partitions for future inserts
CREATE SCHEMA partman;
CREATE EXTENSION pg_partman WITH SCHEMA partman;
SELECT partman.create_parent(
    p_parent_table => 'data.transactions',
    p_control => 'timestamp',
    p_interval => '1 day',
    p_start_partition => '2023-01-01',
    p_premake => 30
);

--Set up job to create new partitions for future inserts
CREATE EXTENSION pg_cron;
UPDATE partman.part_config
SET infinite_time_partitions = true,
    retention = '1 year',
    retention_keep_table = true
WHERE parent_table = 'data.transactions';
SELECT cron.schedule('@hourly', $$CALL partman.run_maintenance_proc()$$);