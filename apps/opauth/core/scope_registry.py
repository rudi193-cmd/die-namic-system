"""
OpAuth Scope Registry
Tracks what services are connected and what permissions are granted.
AI operates within scope. Cannot expand scope.
"""

import json
import os
from datetime import datetime
from pathlib import Path

REGISTRY_PATH = Path.home() / ".opauth" / "scope_registry.json"

class ScopeRegistry:
    """
    Manages granted scopes for all connected services.
    Human grants scope. AI reads scope. AI cannot modify.
    """

    def __init__(self):
        self.registry_path = REGISTRY_PATH
        self._ensure_directory()
        self.scopes = self._load()

    def _ensure_directory(self):
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> dict:
        if self.registry_path.exists():
            with open(self.registry_path, 'r') as f:
                return json.load(f)
        return {"services": {}, "created": datetime.now().isoformat()}

    def _save(self):
        with open(self.registry_path, 'w') as f:
            json.dump(self.scopes, f, indent=2)

    def grant(self, service: str, scope: list, granted_by: str = "human"):
        """
        Grant scope to a service. HUMAN ONLY.
        AI cannot call this directly.
        """
        if granted_by != "human":
            raise PermissionError("HS-OPAUTH-001: Only human can grant scope")

        self.scopes["services"][service] = {
            "scope": scope,
            "granted_at": datetime.now().isoformat(),
            "granted_by": granted_by,
            "active": True
        }
        self._save()
        return True

    def revoke(self, service: str, revoked_by: str = "human"):
        """
        Revoke all scope for a service.
        """
        if service in self.scopes["services"]:
            self.scopes["services"][service]["active"] = False
            self.scopes["services"][service]["revoked_at"] = datetime.now().isoformat()
            self.scopes["services"][service]["revoked_by"] = revoked_by
            self._save()
            return True
        return False

    def check(self, service: str, required_scope: str) -> bool:
        """
        Check if a scope is granted. AI can call this.
        """
        if service not in self.scopes["services"]:
            return False

        svc = self.scopes["services"][service]
        if not svc.get("active", False):
            return False

        return required_scope in svc.get("scope", [])

    def list_services(self) -> dict:
        """
        List all services and their scopes.
        """
        return {
            name: {
                "scope": svc["scope"],
                "active": svc.get("active", False),
                "granted_at": svc.get("granted_at")
            }
            for name, svc in self.scopes["services"].items()
        }

    def get_scope(self, service: str) -> list:
        """
        Get granted scope for a service.
        """
        if service in self.scopes["services"]:
            svc = self.scopes["services"][service]
            if svc.get("active", False):
                return svc.get("scope", [])
        return []


# Hard stops - AI cannot bypass
HARD_STOPS = {
    "HS-OPAUTH-001": "Only human can grant scope",
    "HS-OPAUTH-002": "AI cannot expand existing scope",
    "HS-OPAUTH-003": "AI cannot prevent revocation",
    "HS-OPAUTH-004": "All scope changes logged",
}
