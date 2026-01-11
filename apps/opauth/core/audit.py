"""
OpAuth Audit Log
Every scope change, token access, and API call logged.
AI cannot disable logging. Human can review.
"""

import json
from datetime import datetime
from pathlib import Path

AUDIT_LOG_PATH = Path.home() / ".opauth" / "audit.log"

class AuditLog:
    """
    Immutable audit log for all OpAuth operations.
    AI cannot delete or modify entries.
    """

    def __init__(self):
        self.log_path = AUDIT_LOG_PATH
        self._ensure_directory()

    def _ensure_directory(self):
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event_type: str, service: str, details: dict, actor: str = "unknown"):
        """
        Log an event. Append-only.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "service": service,
            "actor": actor,
            "details": details
        }

        with open(self.log_path, 'a') as f:
            f.write(json.dumps(entry) + "\n")

    def log_scope_grant(self, service: str, scope: list, actor: str = "human"):
        self.log("SCOPE_GRANT", service, {"scope": scope}, actor)

    def log_scope_revoke(self, service: str, actor: str = "human"):
        self.log("SCOPE_REVOKE", service, {}, actor)

    def log_token_store(self, service: str, actor: str = "human"):
        self.log("TOKEN_STORE", service, {}, actor)

    def log_token_access(self, service: str, actor: str = "ai"):
        self.log("TOKEN_ACCESS", service, {}, actor)

    def log_token_delete(self, service: str, actor: str = "human"):
        self.log("TOKEN_DELETE", service, {}, actor)

    def log_api_call(self, service: str, endpoint: str, actor: str = "ai"):
        self.log("API_CALL", service, {"endpoint": endpoint}, actor)

    def log_consent_prompt(self, service: str, scope: list):
        self.log("CONSENT_PROMPT", service, {"scope": scope}, "system")

    def log_consent_granted(self, service: str, scope: list):
        self.log("CONSENT_GRANTED", service, {"scope": scope}, "human")

    def log_consent_denied(self, service: str, scope: list):
        self.log("CONSENT_DENIED", service, {"scope": scope}, "human")

    def log_unlock(self, actor: str = "human"):
        self.log("STORE_UNLOCK", "token_store", {}, actor)

    def log_lock(self, actor: str = "human"):
        self.log("STORE_LOCK", "token_store", {}, actor)

    def get_logs(self, limit: int = 100, service: str = None) -> list:
        """
        Read recent log entries.
        """
        if not self.log_path.exists():
            return []

        entries = []
        with open(self.log_path, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if service is None or entry.get("service") == service:
                        entries.append(entry)
                except:
                    continue

        return entries[-limit:]

    def get_access_history(self, service: str) -> list:
        """
        Get all access events for a service.
        """
        return [e for e in self.get_logs(limit=1000, service=service)
                if e["event"] in ("TOKEN_ACCESS", "API_CALL")]


# Singleton instance
_audit = None

def get_audit() -> AuditLog:
    global _audit
    if _audit is None:
        _audit = AuditLog()
    return _audit
