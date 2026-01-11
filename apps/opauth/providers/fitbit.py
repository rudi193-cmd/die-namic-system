"""
OpAuth Fitbit Provider
OAuth integration for Fitbit health data.
"""

import requests
import base64
from urllib.parse import urlencode
from .base import OAuthProvider

FITBIT_AUTH_URL = "https://www.fitbit.com/oauth2/authorize"
FITBIT_TOKEN_URL = "https://api.fitbit.com/oauth2/token"
FITBIT_API_BASE = "https://api.fitbit.com"

FITBIT_SCOPE_MAP = {
    "activity": "activity",
    "heartrate": "heartrate",
    "sleep": "sleep",
    "weight": "weight",
    "profile": "profile",
    "settings": "settings",
}

class FitbitProvider(OAuthProvider):
    """
    Fitbit OAuth provider.
    Access activity, heart rate, sleep, weight data.
    """

    def __init__(self, client_id: str = None, client_secret: str = None, redirect_uri: str = None):
        super().__init__("fitbit")
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri or "http://localhost:8080/callback"

    def _get_basic_auth(self) -> str:
        """Get basic auth header for token requests."""
        credentials = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(credentials.encode()).decode()

    def get_auth_url(self, scope: list) -> str:
        """
        Get Fitbit OAuth authorization URL.
        """
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(scope),
        }
        return f"{FITBIT_AUTH_URL}?{urlencode(params)}"

    def handle_callback(self, auth_code: str) -> dict:
        """
        Exchange authorization code for tokens.
        """
        headers = {
            "Authorization": f"Basic {self._get_basic_auth()}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }

        response = requests.post(FITBIT_TOKEN_URL, headers=headers, data=data)
        response.raise_for_status()
        return response.json()

    def refresh_token(self) -> bool:
        """
        Refresh the access token.
        """
        token_data = self.token_store.get_token(self.service_name)
        if not token_data or "refresh_token" not in token_data:
            return False

        headers = {
            "Authorization": f"Basic {self._get_basic_auth()}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "refresh_token": token_data["refresh_token"],
            "grant_type": "refresh_token",
        }

        response = requests.post(FITBIT_TOKEN_URL, headers=headers, data=data)
        if response.ok:
            new_token = response.json()
            self.token_store.store_token(self.service_name, new_token, stored_by="human")
            return True
        return False

    def _make_request(self, endpoint: str, method: str = "GET", **kwargs):
        """
        Make authenticated API request.
        """
        token = self.get_access_token()
        if not token:
            raise PermissionError("HS-OPAUTH-005: No access token.")

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"

        url = f"{FITBIT_API_BASE}{endpoint}" if endpoint.startswith("/") else endpoint
        response = requests.request(method, url, headers=headers, **kwargs)

        if response.status_code == 401:
            if self.refresh_token():
                token = self.get_access_token()
                headers["Authorization"] = f"Bearer {token}"
                response = requests.request(method, url, headers=headers, **kwargs)

        return response

    # Convenience methods

    def get_daily_activity(self, date: str = "today") -> dict:
        """
        Get daily activity summary.
        Requires: activity scope
        """
        if not self.check_scope("activity"):
            raise PermissionError("HS-OPAUTH-002: Activity scope not authorized")

        endpoint = f"/1/user/-/activities/date/{date}.json"
        return self.api_call(endpoint, "activity").json()

    def get_heart_rate(self, date: str = "today") -> dict:
        """
        Get heart rate data.
        Requires: heartrate scope
        """
        if not self.check_scope("heartrate"):
            raise PermissionError("HS-OPAUTH-002: Heart rate scope not authorized")

        endpoint = f"/1/user/-/activities/heart/date/{date}/1d.json"
        return self.api_call(endpoint, "heartrate").json()

    def get_sleep(self, date: str = "today") -> dict:
        """
        Get sleep data.
        Requires: sleep scope
        """
        if not self.check_scope("sleep"):
            raise PermissionError("HS-OPAUTH-002: Sleep scope not authorized")

        endpoint = f"/1.2/user/-/sleep/date/{date}.json"
        return self.api_call(endpoint, "sleep").json()

    def get_weight(self, date: str = "today") -> dict:
        """
        Get weight data.
        Requires: weight scope
        """
        if not self.check_scope("weight"):
            raise PermissionError("HS-OPAUTH-002: Weight scope not authorized")

        endpoint = f"/1/user/-/body/log/weight/date/{date}.json"
        return self.api_call(endpoint, "weight").json()
