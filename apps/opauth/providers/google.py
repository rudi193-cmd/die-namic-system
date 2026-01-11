"""
OpAuth Google Provider
OAuth integration for Google services (Drive, Calendar, Gmail, etc.)
"""

import requests
from urllib.parse import urlencode
from .base import OAuthProvider

# Google OAuth endpoints
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_REVOKE_URL = "https://oauth2.googleapis.com/revoke"

# Scope mappings
GOOGLE_SCOPE_MAP = {
    "drive.readonly": "https://www.googleapis.com/auth/drive.readonly",
    "drive.file": "https://www.googleapis.com/auth/drive.file",
    "drive.appdata": "https://www.googleapis.com/auth/drive.appdata",
    "calendar.readonly": "https://www.googleapis.com/auth/calendar.readonly",
    "calendar.events": "https://www.googleapis.com/auth/calendar.events",
    "gmail.readonly": "https://www.googleapis.com/auth/gmail.readonly",
    "gmail.send": "https://www.googleapis.com/auth/gmail.send",
    "fitness.activity.read": "https://www.googleapis.com/auth/fitness.activity.read",
    "fitness.heart_rate.read": "https://www.googleapis.com/auth/fitness.heart_rate.read",
}

class GoogleProvider(OAuthProvider):
    """
    Google OAuth provider.
    Supports Drive, Calendar, Gmail, Fitness APIs.
    """

    def __init__(self, client_id: str = None, client_secret: str = None, redirect_uri: str = None):
        super().__init__("google")
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri or "http://localhost:8080/callback"

    def _map_scopes(self, scopes: list) -> list:
        """Map friendly scope names to Google scope URLs."""
        return [GOOGLE_SCOPE_MAP.get(s, s) for s in scopes]

    def get_auth_url(self, scope: list) -> str:
        """
        Get Google OAuth authorization URL.
        Human navigates here to grant consent.
        """
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self._map_scopes(scope)),
            "access_type": "offline",
            "prompt": "consent",
        }
        return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"

    def handle_callback(self, auth_code: str) -> dict:
        """
        Exchange authorization code for tokens.
        """
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }

        response = requests.post(GOOGLE_TOKEN_URL, data=data)
        response.raise_for_status()
        return response.json()

    def refresh_token(self) -> bool:
        """
        Refresh the access token.
        """
        token_data = self.token_store.get_token(self.service_name)
        if not token_data or "refresh_token" not in token_data:
            return False

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": token_data["refresh_token"],
            "grant_type": "refresh_token",
        }

        response = requests.post(GOOGLE_TOKEN_URL, data=data)
        if response.ok:
            new_token = response.json()
            # Preserve refresh token if not returned
            if "refresh_token" not in new_token:
                new_token["refresh_token"] = token_data["refresh_token"]
            self.token_store.store_token(self.service_name, new_token, stored_by="human")
            return True
        return False

    def _make_request(self, endpoint: str, method: str = "GET", **kwargs):
        """
        Make authenticated API request.
        """
        token = self.get_access_token()
        if not token:
            raise PermissionError("HS-OPAUTH-005: No access token. Human must authorize.")

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"

        response = requests.request(method, endpoint, headers=headers, **kwargs)

        # Auto-refresh on 401
        if response.status_code == 401:
            if self.refresh_token():
                token = self.get_access_token()
                headers["Authorization"] = f"Bearer {token}"
                response = requests.request(method, endpoint, headers=headers, **kwargs)

        return response

    # Convenience methods for common operations

    def list_drive_files(self, folder_id: str = "root", page_size: int = 100) -> dict:
        """
        List files in Google Drive.
        Requires: drive.readonly or drive.file
        """
        if not (self.check_scope("drive.readonly") or self.check_scope("drive.file")):
            raise PermissionError("HS-OPAUTH-002: Drive read scope not authorized")

        endpoint = "https://www.googleapis.com/drive/v3/files"
        params = {
            "q": f"'{folder_id}' in parents",
            "pageSize": page_size,
            "fields": "files(id,name,mimeType,modifiedTime)",
        }
        return self.api_call(endpoint, "drive.readonly", params=params).json()

    def read_drive_file(self, file_id: str) -> bytes:
        """
        Read a file from Google Drive.
        Requires: drive.readonly or drive.file
        """
        if not (self.check_scope("drive.readonly") or self.check_scope("drive.file")):
            raise PermissionError("HS-OPAUTH-002: Drive read scope not authorized")

        endpoint = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
        return self.api_call(endpoint, "drive.readonly").content

    def list_calendar_events(self, calendar_id: str = "primary", max_results: int = 10) -> dict:
        """
        List calendar events.
        Requires: calendar.readonly or calendar.events
        """
        if not (self.check_scope("calendar.readonly") or self.check_scope("calendar.events")):
            raise PermissionError("HS-OPAUTH-002: Calendar read scope not authorized")

        endpoint = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
        params = {"maxResults": max_results, "orderBy": "startTime", "singleEvents": True}
        return self.api_call(endpoint, "calendar.readonly", params=params).json()
