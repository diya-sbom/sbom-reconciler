from __future__ import annotations

import os
import json
import hashlib
from datetime import datetime, UTC
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

app = FastAPI(title="Diya API", version="v1.0")

LEDGER_PATH = Path("ledger/ledger.jsonl")
RECORD_PATH = Path("verification_record.json")


# -----------------------------
# Models
# -----------------------------
class VerifyRequest(BaseModel):
    artifact: str
    digest: str
    builder: str
    justification: str | None = None
    approver: str | None = None


# -----------------------------
# Helpers
# -----------------------------
def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_previous_hash() -> str:
    if not LEDGER_PATH.exists():
        return ""

    lines = [
        line.strip()
        for line in LEDGER_PATH.read_text().splitlines()
        if line.strip()
    ]

    if not lines:
        return ""

    last = json.loads(lines[-1])
    return last.get("entry_hash", "")


# -----------------------------
# Core Logic
# -----------------------------
def evaluate_decision(req: VerifyRequest) -> str:
    allowed_builders = ["github-actions"]

    if not req.artifact or not req.digest or not req.builder:
        return "FAIL"

    if not req.digest.startswith("sha256:"):
        return "FAIL"

    if req.builder not in allowed_builders:
        return "FAIL"

    return "PASS"


def build_verification_record(
    req: VerifyRequest, decision: str
) -> dict[str, Any]:
    previous_hash = load_previous_hash()

    base_record = {
        "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "artifact": req.artifact,
        "digest": req.digest,
        "builder": req.builder,
        "decision": decision,
        "previous_hash": previous_hash,
    }

    entry_hash = sha256_text(canonical_json(base_record))
    base_record["entry_hash"] = entry_hash

    return base_record


def persist_record(record: dict[str, Any]) -> None:
    RECORD_PATH.write_text(json.dumps(record, indent=2))

    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)

    with LEDGER_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


# -----------------------------
# Routes
# -----------------------------
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/verify")
def verify(
    req: VerifyRequest,
    x_api_key: str | None = Header(default=None),
) -> dict[str, Any]:
    expected_api_key = os.getenv("DIYA_API_KEY")

    if not expected_api_key:
        raise HTTPException(
            status_code=500,
            detail="server missing DIYA_API_KEY",
        )

    if x_api_key != expected_api_key:
        raise HTTPException(
            status_code=401,
            detail="unauthorized",
        )

    decision = evaluate_decision(req)

    record = build_verification_record(req, decision)
    persist_record(record)

    return {
        "decision": decision,
        "verification_record": record,
        "ledger_entry_hash": record["entry_hash"],
    }
