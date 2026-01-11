"""
OpAuth SmartHome Provider
Integration for smart home devices.
HARD STOPS: AI cannot control locks or access camera streams.
"""

from .base import OAuthProvider
from ..core.consent import FORBIDDEN_SCOPES

class SmartHomeProvider(OAuthProvider):
    """
    Smart Home provider with strict safety limits.

    HARD STOPS:
    - HS-OPAUTH-010: AI cannot control door locks
    - HS-OPAUTH-011: AI cannot access camera streams
    """

    # Scopes AI can NEVER have
    FORBIDDEN = ["locks.control", "cameras.stream", "alarm.disarm"]

    def __init__(self, platform: str = "generic", client_id: str = None,
                 client_secret: str = None, redirect_uri: str = None):
        super().__init__(f"smarthome_{platform}")
        self.platform = platform
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def request_authorization(self, scope: list, reason: str = "") -> dict:
        """
        Request authorization - blocks forbidden scopes.
        """
        # Check for forbidden scopes
        for s in scope:
            if s in self.FORBIDDEN:
                raise PermissionError(
                    f"HS-OPAUTH-010: Scope '{s}' is forbidden. "
                    f"AI cannot control locks, cameras, or alarms."
                )

        return super().request_authorization(scope, reason)

    def get_auth_url(self, scope: list) -> str:
        """
        Get OAuth URL - platform specific.
        """
        # Block forbidden scopes even at URL generation
        for s in scope:
            if s in self.FORBIDDEN:
                raise PermissionError(f"HS-OPAUTH-010: Scope '{s}' is forbidden")

        # Platform-specific implementations would go here
        # This is a reference implementation
        raise NotImplementedError(
            f"SmartHome OAuth for platform '{self.platform}' not implemented. "
            "See platform-specific provider (google_home.py, smartthings.py, etc.)"
        )

    def handle_callback(self, auth_code: str) -> dict:
        raise NotImplementedError("Platform-specific implementation required")

    def refresh_token(self) -> bool:
        raise NotImplementedError("Platform-specific implementation required")

    def _make_request(self, endpoint: str, **kwargs):
        raise NotImplementedError("Platform-specific implementation required")

    # Safe operations

    def get_lights_status(self) -> dict:
        """
        Get status of all lights.
        Requires: lights.read
        """
        if not self.check_scope("lights.read"):
            raise PermissionError("HS-OPAUTH-002: lights.read scope not authorized")
        # Implementation depends on platform
        raise NotImplementedError()

    def set_light(self, device_id: str, on: bool, brightness: int = None) -> bool:
        """
        Control a light.
        Requires: lights.control
        """
        if not self.check_scope("lights.control"):
            raise PermissionError("HS-OPAUTH-002: lights.control scope not authorized")
        # Implementation depends on platform
        raise NotImplementedError()

    def get_thermostat(self) -> dict:
        """
        Get thermostat status.
        Requires: thermostat.read
        """
        if not self.check_scope("thermostat.read"):
            raise PermissionError("HS-OPAUTH-002: thermostat.read scope not authorized")
        raise NotImplementedError()

    def set_thermostat(self, temperature: float) -> bool:
        """
        Set thermostat temperature.
        Requires: thermostat.control
        """
        if not self.check_scope("thermostat.control"):
            raise PermissionError("HS-OPAUTH-002: thermostat.control scope not authorized")
        raise NotImplementedError()

    def get_lock_status(self) -> dict:
        """
        Get lock status (read only).
        Requires: locks.read
        AI CAN see if doors are locked.
        """
        if not self.check_scope("locks.read"):
            raise PermissionError("HS-OPAUTH-002: locks.read scope not authorized")
        raise NotImplementedError()

    def control_lock(self, device_id: str, lock: bool) -> bool:
        """
        FORBIDDEN - AI cannot control locks.
        """
        raise PermissionError(
            "HS-OPAUTH-010: AI cannot control door locks. "
            "This is a hard stop that cannot be overridden."
        )

    def get_camera_status(self) -> dict:
        """
        Get camera online/offline status (no streams).
        Requires: cameras.read
        """
        if not self.check_scope("cameras.read"):
            raise PermissionError("HS-OPAUTH-002: cameras.read scope not authorized")
        raise NotImplementedError()

    def get_camera_stream(self, device_id: str) -> str:
        """
        FORBIDDEN - AI cannot access camera streams.
        """
        raise PermissionError(
            "HS-OPAUTH-011: AI cannot access camera streams. "
            "This is a hard stop that cannot be overridden."
        )


# Hard stops that apply to ALL smart home platforms
SMARTHOME_HARD_STOPS = {
    "HS-OPAUTH-010": "AI cannot control door locks",
    "HS-OPAUTH-011": "AI cannot access camera streams",
    "HS-OPAUTH-012": "AI cannot disarm security systems",
    "HS-OPAUTH-013": "AI cannot open garage doors",
}
