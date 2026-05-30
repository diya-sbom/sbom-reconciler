from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import subprocess

app = FastAPI()

class VerifyRequest(BaseModel):
    baseline: str
    current: str

def run_sbom_diff(baseline, current):
    try:
        result = subprocess.run(
            ["python3", "src/sbom_diff.py", baseline, current],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return "PASS", result.stdout
        else:
            return "FAIL", result.stdout

    except Exception as e:
        return "FAIL", str(e)

@app.post("/verify")
def verify(req: VerifyRequest):
    decision, output = run_sbom_diff(req.baseline, req.current)

    return {
        "decision": decision,
        "reason": output,
        "timestamp": datetime.utcnow().isoformat()
    }
