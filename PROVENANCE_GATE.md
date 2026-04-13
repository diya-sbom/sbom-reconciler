name: Provenance Gate

on:
  push:
    branches: [ main ]

jobs:
  verify:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run Provenance Gate
        run: |
          echo "hello world" > artifact.txt
          HASH=$(sha256sum artifact.txt | awk '{print $1}')
          python3 provenance_gate/provenance_check.py artifact.txt provenance_gate/examples/provenance_example.json $HASH
