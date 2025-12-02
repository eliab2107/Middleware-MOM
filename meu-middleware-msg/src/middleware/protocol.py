"""Message protocol definitions (simple JSON-serializable messages)."""
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
import time
import uuid


@dataclass
class Message:
    msg_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str = "request"  # or 'response'
    method: str = ""
    args: List[Any] = field(default_factory=list)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    reply_to: Optional[str] = None
    correlation_id: Optional[str] = None
    ttl_ms: int = 0
    created_at: float = field(default_factory=lambda: time.time())
    payload: Any = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        return cls(
            msg_id=data.get("msg_id") or str(uuid.uuid4()),
            type=data.get("type", "request"),
            method=data.get("method", ""),
            args=data.get("args", []),
            kwargs=data.get("kwargs", {}),
            reply_to=data.get("reply_to"),
            correlation_id=data.get("correlation_id"),
            ttl_ms=int(data.get("ttl_ms", 0) or 0),
            created_at=float(data.get("created_at", time.time())),
            payload=data.get("payload"),
        )

    @property
    def expires_at(self) -> Optional[float]:
        if not self.ttl_ms:
            return None
        return self.created_at + (self.ttl_ms / 1000.0)

    def is_expired(self) -> bool:
        exp = self.expires_at
        if exp is None:
            return False
        return time.time() > exp
