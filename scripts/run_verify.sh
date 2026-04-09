#!/bin/bash

set -e

echo "Starting Diya API..."
export DIYA_API_KEY="test-key"

python3 -m uvicorn api.server:app --host 127.0.0.1 --port 8000 &
PID=$!

sleep 3

echo "Calling /verify API..."

RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/verify \
  -H "Content-Type: application/json" \
  -H "x-api-key: test-key" \
  -d @examples/pass/request.json)

echo "Response:"
echo "$RESPONSE"

kill $PID
