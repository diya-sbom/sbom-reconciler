#!/bin/bash

set -e

echo "Starting Diya API..."
export DIYA_API_KEY="test-key"

python3 -m uvicorn api.server:app --host 127.0.0.1 --port 8000 &
PID=$!

sleep 3

echo "Calling /verify..."

RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/verify \
  -H "Content-Type: application/json" \
  -H "x-api-key: test-key" \
  -d @examples/pass/request.json)

echo "$RESPONSE" | tee gate_output.json

DECISION=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['decision'])")

if [ "$DECISION" != "PASS" ]; then
  echo "BLOCKED: verification failed"
  kill $PID
  exit 1
fi

echo "ALLOWED: verification passed"
kill $PID
