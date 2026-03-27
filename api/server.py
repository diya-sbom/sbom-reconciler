from __future__ import annotations

import json
import hashlib
from datetime import datetime, UTC
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Diya API", version="v1.0")


LEDGER_PATH = Path("ledger/ledger.jsonl")
RECORD_PATH = Path("verification_record.json")


class VerifyRequest(BaseModel):
    artifact: str = Field(..., description="Artifact name or identifier")
    digest: str = Field(..., description="Artifact digest, usually sha256")
    builder: str = Field(..., description="Builder identity")
    sbom: dict[str, Any] | None = None
    provenance: dict[str, Any] | None = None


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_previous_hash() -> str:
    if not LEDGER_PATH.exists():
        return ""
    lines = [line.strip() for line in LEDGER_PATH.read_text().splitlines() if line.strip()]
    if not lines:
        return ""
    last = json.loads(lines[-1])
    return last.get("entry_hash", "")


def evaluate_decision(req: VerifyRequest) -> str:
    # Minimal v1.0 API behavior:
    # PASS if required fields exist and digest looks like sha256:...
    # FAIL otherwise.
    if not req.artifact or not req.digest or not req.builder:
        return "FAIL"
    if not req.digest.startswith("sha256:"):
        return "FAIL"
    return "PASS"


def build_verification_record(req: VerifyRequest, decision: str) -> dict[str, Any]:
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


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/verify")
def verify(req: VerifyRequest) -> dict[str, Any]:
    try:
        decision = evaluate_decision(req)
        record = build_verification_record(req, decision)
        persist_record(record)

        return {
            "decision": decision,
            "verification_record": record,
            "ledger_entry_hash": record["entry_hash"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"verification_failed: {e}")
