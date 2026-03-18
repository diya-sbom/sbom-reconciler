#!/bin/bash
set -e

echo "=== BUILD ==="
echo "artifact built at $(date)" > artifact.txt

echo "=== DIYA GATE ==="
python3 cli/diya.py verify

echo "=== DEPLOY ==="
echo "DEPLOY SUCCESS"
