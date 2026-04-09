#!/bin/bash

echo "Running FAIL example..."

RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/verify \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DIYA_API_KEY" \
  -d @request.json)

echo "Response:"
echo "$RESPONSE"

STATUS=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['decision'])")

if [ "$STATUS" = "FAIL" ]; then
  echo "FAIL example behaved correctly"
  exit 0
else
  echo "Unexpected PASS"
  exit 1
fi
