#!/bin/bash

echo "Calling Diya..."

response=$(curl -s -X POST http://127.0.0.1:8000/verify \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DIYA_API_KEY" \
  -d '{
    "artifact": "test-image",
    "digest": "sha256:abc123",
    "builder": "github-actions"
  }')

echo "Response:"
echo "$response"

decision=$(echo "$response" | python3 -c 'import sys, json; print(json.load(sys.stdin)["decision"])')

if [ "$decision" != "PASS" ]; then
  echo "❌ Blocked by Diya"
  exit 1
fi

echo "✅ Passed Diya"
