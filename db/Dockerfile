FROM postgres:latest

# install pg_cron
RUN apt-get update && apt-get install -y postgresql-16-cron

# install pg_partman dependencies
RUN apt-get install -y wget clang llvm make gcc libc-dev

# Install pg_partman
RUN set -ex \
    && wget -O pg_partman.tar.gz "https://github.com/pgpartman/pg_partman/archive/refs/tags/v5.0.0.tar.gz" \
    && mkdir -p /usr/src/pg_partman \
    && tar \
        --extract \
        --file pg_partman.tar.gz \
        --directory /usr/src/pg_partman \
        --strip-components 1 \
    && rm pg_partman.tar.gz \
    && cd /usr/src/pg_partman \
    && make NO_BGW=1 install \
    # Cleanup
    && rm -rf /usr/src/pg_partman \
    && apt-get remove -y wget clang llvm make gcc libc-dev \
    && apt-get autoremove --purge -y \
    && apt-get clean \
    && apt-get purge \
    && rm -rf /var/lib/apt/lists/*

# copy initial scripts
COPY configure_pg_cron.sh /docker-entrypoint-initdb.d/
COPY init_db.sql /docker-entrypoint-initdb.d/
