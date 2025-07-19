#!/bin/sh
set -e

echo "=== Alembic migration start ==="
alembic upgrade head
echo "=== Alembic migration done ==="

echo "=== Starting FastAPI (uvicorn) ==="
exec uvicorn app:app --host 0.0.0.0 --port 8000 