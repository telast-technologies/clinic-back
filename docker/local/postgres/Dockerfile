FROM postgres:16

RUN apt-get update && apt-get  install -y postgresql-16-postgis-3

COPY ./docker/local/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
