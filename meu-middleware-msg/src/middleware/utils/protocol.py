"""Message protocol definitions (simple JSON-serializable messages)."""
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
import time
import uuid

@dataclass
class Message:
    def __init__(self, data: Dict[str, Any] = None):
        self.msg_id = field(default_factory=lambda: str(uuid.uuid4()))
        self.topic: str = data.get("topic") if data else ""
        self.type: str = data.get("type", "publication") if data else "publication"
        self.method: str = data.get("method", "publish") if data else "publish"
        self.service: str = data.get("service", "notification_engine") if data else "notification_engine"
        self.args: List[Any] = data.get("args", []) if data else []
        self.kwargs: Dict[str, Any] = data.get("kwargs", {}) if data else {}
        self.reply_to: Optional[str] = data.get("reply_to") if data else None
        self.correlation_id: Optional[str] = data.get("correlation_id") if data else None
        self.ttl_ms: int = int(data.get("ttl_ms", 0) or 0) if data else 0
        self.created_at: float = time.time()
        self.payload: Any = data.get("payload") if data else None
        self.sended: bool = False

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d

    @property
    def expires_at(self) -> Optional[float]:
        if self.ttl_ms != 0:
            return None
        return self.created_at + (self.ttl_ms / 1000.0)

    def is_expired(self) -> bool:
        exp = self.expires_at
        if exp is None:
            return False
        return time.time() > exp
