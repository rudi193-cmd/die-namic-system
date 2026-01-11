"""
OpAuth Provider Base Class
All OAuth providers inherit from this.
"""

from abc import ABC, abstractmethod
from ..core.consent import ConsentFlow
from ..core.audit import get_audit
from ..storage.token_store import TokenStore

class OAuthProvider(ABC):
    """
    Base class for OAuth providers.
    Enforces consent and audit requirements.
    """

    def __init__(self, service_name: str):
        self.service_name = service_name
        self.consent = ConsentFlow()
        self.audit = get_audit()
        self.token_store = TokenStore()

    @abstractmethod
    def get_auth_url(self, scope: list) -> str:
        """
        Get the OAuth authorization URL.
        Human navigates to this URL to grant consent.
        """
        pass

    @abstractmethod
    def handle_callback(self, auth_code: str) -> dict:
        """
        Handle OAuth callback with authorization code.
        Exchange code for tokens.
        """
        pass

    @abstractmethod
    def refresh_token(self) -> bool:
        """
        Refresh access token using refresh token.
        """
        pass

    def request_authorization(self, scope: list, reason: str = "") -> dict:
        """
        Request authorization from human.
        Returns consent request for human review.
        """
        return self.consent.request_consent(self.service_name, scope, reason)

    def complete_authorization(self, scope: list, auth_code: str) -> bool:
        """
        Complete authorization after human grants consent.
        HUMAN must have called grant_consent first.
        """
        # Check consent was granted
        for s in scope:
            if not self.consent.check_consent(self.service_name, s):
                raise PermissionError(f"HS-OPAUTH-001: Scope '{s}' not consented")

        # Exchange code for token
        token_data = self.handle_callback(auth_code)

        # Store token (requires human to have unlocked store)
        self.token_store.store_token(self.service_name, token_data, stored_by="human")
        self.audit.log_token_store(self.service_name)

        return True

    def get_access_token(self) -> str:
        """
        Get access token for API calls.
        Logs access for audit.
        """
        self.audit.log_token_access(self.service_name, actor="ai")
        token_data = self.token_store.get_token(self.service_name)
        if token_data:
            return token_data.get("access_token")
        return None

    def revoke(self) -> bool:
        """
        Revoke authorization.
        """
        self.consent.revoke_consent(self.service_name)
        self.token_store.delete_token(self.service_name)
        return True

    def check_scope(self, required_scope: str) -> bool:
        """
        Check if a scope is authorized.
        AI should call this before making API requests.
        """
        return self.consent.check_consent(self.service_name, required_scope)

    def api_call(self, endpoint: str, required_scope: str, **kwargs):
        """
        Make an API call with scope checking.
        """
        if not self.check_scope(required_scope):
            raise PermissionError(f"HS-OPAUTH-002: Scope '{required_scope}' not authorized")

        self.audit.log_api_call(self.service_name, endpoint, actor="ai")
        return self._make_request(endpoint, **kwargs)

    @abstractmethod
    def _make_request(self, endpoint: str, **kwargs):
        """
        Provider-specific API request implementation.
        """
        pass
