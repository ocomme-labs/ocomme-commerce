#!/usr/bin/env bash

set -euo pipefail

APP_MODULE=${APP_MODULE:-config.wsgi:application}
PORT=${PORT:-8000}

DB_HOST=${DB_HOST:-postgres}
DB_PORT=${DB_PORT:-5432}

MAX_RETRIES=${MAX_RETRIES:-30}
RETRY_INTERVAL=${RETRY_INTERVAL:-2}

RUN_MIGRATIONS=${RUN_MIGRATIONS:-false}
RUN_COLLECTSTATIC=${RUN_COLLECTSTATIC:-false}

log() {
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] [$1] $2"
}

check_db_connection() {
python << END
import socket,sys
try:
    socket.create_connection(("$DB_HOST", int("$DB_PORT")), timeout=2)
    sys.exit(0)
except Exception:
    sys.exit(1)
END
}

wait_for_db() {

    log INFO "waiting_for_database target=$DB_HOST:$DB_PORT"

    count=0

    until check_db_connection; do
        count=$((count + 1))

        if [ "$count" -gt "$MAX_RETRIES" ]; then
            log CRITICAL "database_unreachable after=$MAX_RETRIES attempts"
            exit 1
        fi

        log WARN "database_not_ready retry=${count}/${MAX_RETRIES}"
        sleep "$RETRY_INTERVAL"
    done

    log INFO "database_ready"
}

run_migrations() {

    if [ "$RUN_MIGRATIONS" = "true" ]; then
        log INFO "running_django_migrations"
        python manage.py migrate --noinput
    fi
}

collect_static() {

    if [ "$RUN_COLLECTSTATIC" = "true" ]; then
        log INFO "collecting_static_files"
        python manage.py collectstatic --noinput
    fi
}

start_gunicorn() {

    log INFO "starting_gunicorn port=$PORT module=$APP_MODULE"

    exec gunicorn "$APP_MODULE" \
        --bind 0.0.0.0:$PORT \
        --workers ${GUNICORN_WORKERS:-3} \
        --threads ${GUNICORN_THREADS:-2} \
        --timeout ${GUNICORN_TIMEOUT:-60} \
        --access-logfile - \
        --error-logfile -
}

main() {

    wait_for_db

    run_migrations

    collect_static

    log INFO "launching_application"

    if [ "$#" -gt 0 ]; then
        exec "$@"
    else
        start_gunicorn
    fi
}

main "$@"