"""
OpAuth Revocation Manager
Centralized revocation of OAuth tokens and consent.
Human-initiated only.
"""

from .consent import ConsentFlow
from .audit import get_audit
from ..storage.token_store import TokenStore

class RevocationManager:
    """
    Manages revocation of OAuth authorizations.
    AI cannot revoke - only human can.
    """

    def __init__(self):
        self.consent = ConsentFlow()
        self.token_store = TokenStore()
        self.audit = get_audit()

    def revoke_service(self, service: str, revoked_by: str = "human") -> dict:
        """
        Revoke all access for a service.
        HUMAN ONLY.
        """
        if revoked_by != "human":
            raise PermissionError(
                "HS-OPAUTH-020: Only human can revoke authorizations"
            )

        result = {
            "service": service,
            "consent_revoked": False,
            "token_deleted": False,
            "remote_revoked": False,
        }

        # Revoke consent
        try:
            self.consent.revoke_consent(service, revoked_by)
            result["consent_revoked"] = True
        except Exception as e:
            result["consent_error"] = str(e)

        # Delete token
        try:
            self.token_store.delete_token(service)
            result["token_deleted"] = True
        except Exception as e:
            result["token_error"] = str(e)

        self.audit.log_revocation(service, revoked_by, result)
        return result

    def revoke_all(self, revoked_by: str = "human") -> dict:
        """
        Emergency revocation of ALL services.
        HUMAN ONLY. Use with caution.
        """
        if revoked_by != "human":
            raise PermissionError(
                "HS-OPAUTH-020: Only human can revoke authorizations"
            )

        self.audit.log_event("EMERGENCY_REVOKE_ALL", {"revoked_by": revoked_by})

        results = {}
        services = self.consent.list_consents()

        for service in services:
            results[service] = self.revoke_service(service, revoked_by)

        return results

    def list_active_authorizations(self) -> dict:
        """
        List all active authorizations.
        AI can call this to see what's authorized.
        """
        consents = self.consent.list_consents()
        tokens = self.token_store.list_services()

        return {
            "consented_services": consents,
            "services_with_tokens": tokens,
        }

    def check_authorization_status(self, service: str) -> dict:
        """
        Check authorization status for a specific service.
        """
        return {
            "service": service,
            "has_consent": bool(self.consent.list_consents().get(service)),
            "has_token": service in self.token_store.list_services(),
        }


# Revocation hard stops
REVOCATION_HARD_STOPS = {
    "HS-OPAUTH-020": "Only human can revoke authorizations",
    "HS-OPAUTH-021": "AI cannot trigger emergency revoke all",
}
