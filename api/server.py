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
    allowed_builders = ["github-actions"]

    if not req.artifact or not req.digest or not req.builder:
        return "FAIL"
    if not req.digest.startswith("sha256:"):
        return "FAIL"
    if req.builder not in allowed_builders:
        return "FAIL"

    return "PASS"


def build_verification_record(req: VerifyRequest, decision: str) -> dict[str, Any]:
    previous_hash = load_previous_hash()

    base_record = {
        "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),

from datetime import datetime
from pathlib import Path

import os
import json
import yaml
from fastapi import Header, HTTPException
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class VerifyRequest(BaseModel):
    artifact: str
    digest: str
    builder: str
    justification: str | None = None
    approver: str | None = None


def load_policy(policy_name: str = "default-v1") -> dict:
    policy_path = Path("policy") / f"{policy_name}.yml"
    with open(policy_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/verify")
def verify(req: VerifyRequest, x_api_key: str | None = Header(default=None)):
    expected_api_key = os.getenv("DIYA_API_KEY")

    if not expected_api_key:
        raise HTTPException(status_code=500, detail="server missing DIYA_API_KEY")

    if x_api_key != expected_api_key:
        raise HTTPException(status_code=401, detail="unauthorized")

    policy = load_policy("default-v1")
    allowed_builders = ["github-actions"]

    if not req.artifact or not req.digest or not req.builder:
        decision = "FAIL"
        reason = "missing required fields"

    elif req.builder == "override":
        if not req.justification:
            decision = "FAIL"
            reason = "override requires justification"
        elif not req.approver:
            decision = "FAIL"
            reason = "override requires approver"
        elif policy.get("exception", {}).get("allowed"):
            decision = "EXCEPTION"
            reason = f"approved override by {req.approver}: {req.justification}"
        else:
            decision = "FAIL"
            reason = "override not allowed by policy"

    elif req.builder not in allowed_builders:
        decision = "FAIL"
        reason = "unauthorized builder"

    else:
        decision = "PASS"
        reason = "policy checks passed"

    verification_record = {
        "timestamp": datetime.utcnow().isoformat(),
        527e0c1 (Remove CLI verification path)
        "artifact": req.artifact,
        "digest": req.digest,
        "builder": req.builder,
        "decision": decision,
        HEAD
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

    }

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "artifact": req.artifact,
        "digest": req.digest,
        "builder": req.builder,
        "justification": req.justification,
        "approver": req.approver,
        "decision": decision,
        "reason": reason,
    }

    with open("decision_history.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

    return {
        "decision": decision,
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat(),
        "verification_record": verification_record,
    }
        527e0c1 (Remove CLI verification path)
