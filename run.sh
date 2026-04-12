#!/bin/bash

echo "Starting Diya..."

export DIYA_API_KEY=test-key

python3 -m pip install --upgrade pip >/dev/null 2>&1

if [ -f requirements.txt ]; then
  pip install -r requirements.txt >/dev/null 2>&1
else
  pip install fastapi uvicorn pydantic pyyaml >/dev/null 2>&1
fi

nohup python3 -m uvicorn api.server:app --host 127.0.0.1 --port 8000 > server.log 2>&1 &

sleep 3

echo "Testing PASS case..."
curl -s -X POST http://127.0.0.1:8000/verify \
  -H "Content-Type: application/json" \
  -H "x-api-key: test-key" \
  -d @examples/pass/request.json

echo ""
echo "Testing FAIL case..."
curl -s -X POST http://127.0.0.1:8000/verify \
  -H "Content-Type: application/json" \
  -H "x-api-key: test-key" \
  -d @examples/fail/request.json

echo ""
echo "Done."
