"""
OpAuth Consent Flow
Human must explicitly consent to each service connection.
AI cannot bypass consent.
"""

from .scope_registry import ScopeRegistry
from .audit import get_audit

class ConsentFlow:
    """
    Manages consent prompts and grants.
    AI proposes. Human disposes.
    """

    def __init__(self):
        self.registry = ScopeRegistry()
        self.audit = get_audit()

    def request_consent(self, service: str, requested_scope: list, reason: str = "") -> dict:
        """
        AI requests consent for a scope.
        Returns a consent request object for human review.
        AI CANNOT auto-approve.
        """
        self.audit.log_consent_prompt(service, requested_scope)

        return {
            "service": service,
            "requested_scope": requested_scope,
            "reason": reason,
            "status": "pending",
            "instructions": "Human must call grant_consent() or deny_consent()"
        }

    def grant_consent(self, service: str, approved_scope: list, granted_by: str = "human") -> bool:
        """
        Human grants consent. HUMAN ONLY.
        """
        if granted_by != "human":
            raise PermissionError("HS-OPAUTH-001: Only human can grant consent")

        self.registry.grant(service, approved_scope, granted_by)
        self.audit.log_consent_granted(service, approved_scope)
        return True

    def deny_consent(self, service: str, denied_scope: list) -> bool:
        """
        Human denies consent.
        """
        self.audit.log_consent_denied(service, denied_scope)
        return True

    def revoke_consent(self, service: str, revoked_by: str = "human") -> bool:
        """
        Revoke previously granted consent.
        """
        self.registry.revoke(service, revoked_by)
        self.audit.log_scope_revoke(service, revoked_by)
        return True

    def check_consent(self, service: str, required_scope: str) -> bool:
        """
        Check if consent exists for a scope.
        AI can call this to check before making requests.
        """
        return self.registry.check(service, required_scope)

    def list_consents(self) -> dict:
        """
        List all granted consents.
        """
        return self.registry.list_services()


# Scope definitions for common services
GOOGLE_SCOPES = {
    "drive.readonly": "Read files from Google Drive",
    "drive.file": "Read/write files created by this app",
    "drive.appdata": "Access app-specific data folder",
    "calendar.readonly": "Read calendar events",
    "calendar.events": "Read/write calendar events",
    "gmail.readonly": "Read email messages",
    "gmail.send": "Send email on your behalf",
}

FITBIT_SCOPES = {
    "activity": "Activity and exercise data",
    "heartrate": "Heart rate data",
    "sleep": "Sleep data",
    "weight": "Weight data",
    "profile": "Profile information",
    "settings": "Account settings",
}

SMARTHOME_SCOPES = {
    "lights.read": "See light status",
    "lights.control": "Turn lights on/off",
    "thermostat.read": "See temperature",
    "thermostat.control": "Adjust temperature",
    "locks.read": "See lock status",
    # NO locks.control - hard stop
    "cameras.read": "See camera status",
    # NO cameras.stream - hard stop
}

# Hard stops for dangerous scopes
FORBIDDEN_SCOPES = {
    "locks.control": "HS-OPAUTH-010: AI cannot control door locks",
    "cameras.stream": "HS-OPAUTH-011: AI cannot access camera streams",
    "gmail.send": "HS-OPAUTH-012: AI cannot send email without per-message approval",
    "payments": "HS-OPAUTH-013: AI cannot make payments",
}
