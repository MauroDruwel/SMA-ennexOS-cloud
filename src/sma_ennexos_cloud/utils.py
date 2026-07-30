import base64
import hashlib
import os
from typing import Any


def _b64url(data: bytes) -> str:
    """URL-safe base64 encode without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def generate_pkce() -> tuple[str, str]:
    """Generate PKCE code_verifier and code_challenge (S256)."""
    verifier = _b64url(os.urandom(32))
    challenge = _b64url(hashlib.sha256(verifier.encode()).digest())
    return verifier, challenge


def random_str() -> str:
    """Generate a cryptographically random string."""
    return _b64url(os.urandom(32))


def _asdict(instance: Any) -> dict[str, Any]:
    """Convert a dataclass instance to a dict, skipping None values."""
    result: dict[str, Any] = {}
    for field_name in instance.__dataclass_fields__:
        value = getattr(instance, field_name)
        if value is None:
            continue
        if hasattr(value, "to_dict"):
            result[field_name] = value.to_dict()
        elif isinstance(value, list):
            result[field_name] = [
                item.to_dict() if hasattr(item, "to_dict") else item for item in value
            ]
        else:
            result[field_name] = value
    return result
