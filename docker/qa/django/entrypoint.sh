#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset



if [ -z "${CLINIC_POSTGRES_USER}" ]; then
    base_postgres_image_default_user='postgres'
    export CLINIC_POSTGRES_USER="${base_postgres_image_default_user}"
fi
export DATABASE_URL="postgres://${CLINIC_POSTGRES_USER}:${CLINIC_POSTGRES_PASSWORD}@${CLINIC_POSTGRES_HOST}:${CLINIC_POSTGRES_PORT}/${CLINIC_POSTGRES_DB}"

python << END

import sys
import time

import psycopg2

suggest_unrecoverable_after = 30
start = time.time()

while True:
    try:
        psycopg2.connect(
            dbname="${CLINIC_POSTGRES_DB}",
            user="${CLINIC_POSTGRES_USER}",
            password="${CLINIC_POSTGRES_PASSWORD}",
            host="${CLINIC_POSTGRES_HOST}",
            port="${CLINIC_POSTGRES_PORT}",
        )
        break
    except psycopg2.OperationalError as error:
        sys.stderr.write("Waiting for PostgreSQL to become available...\n")

        if time.time() - start > suggest_unrecoverable_after:
            sys.stderr.write("  This is taking longer than expected. The following exception may be indicative of an unrecoverable error: '{}'\n".format(error))

    time.sleep(1)
END

>&2 echo 'PostgreSQL is available'

exec "$@"
