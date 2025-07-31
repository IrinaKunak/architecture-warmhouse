#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be available..."

until pg_isready -h postgres -p 5432 -U postgres; do
  sleep 1
done

echo "PostgreSQL is ready. Applying migrations..."
alembic upgrade head

echo "Starting API server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8081
