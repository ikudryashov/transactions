echo "shared_preload_libraries=pg_cron" >> /var/lib/postgresql/data/postgresql.conf
echo "cron.database_name='transactions_db'" >> /var/lib/postgresql/data/postgresql.conf

pg_ctl restart