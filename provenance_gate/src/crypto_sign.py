import json
import hashlib
import hmac
import base64
from typing import Dict

SECRET_KEY = b"provenance_secret_key_v1"

def canonical_json(data: Dict) -> bytes:
 	return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")

def sign(data: Dict) -> str:
    message = canonical_json(data)
    signature = hmac.new(SECRET_KEY, message, hashlib.sha256).digest()
    return base64.b64encode(signature).decode("utf-8")

def verify(data: Dict, signature: str) -> bool:
    expected_sig = sign(data)
    return hmac.compare_digest(expected_sig, signature)
