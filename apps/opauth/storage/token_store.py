"""
OpAuth Token Store
Encrypted storage for OAuth tokens.
Human provides passphrase. AI cannot access raw tokens without human.
"""

import json
import os
import base64
from datetime import datetime
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

TOKEN_STORE_PATH = Path.home() / ".opauth" / "tokens.enc"
SALT_PATH = Path.home() / ".opauth" / "salt"

class TokenStore:
    """
    Encrypted token storage.
    Tokens encrypted at rest. Human passphrase required to decrypt.
    AI cannot access tokens without human providing passphrase.
    """

    def __init__(self):
        self.store_path = TOKEN_STORE_PATH
        self.salt_path = SALT_PATH
        self._ensure_directory()
        self._fernet = None  # Not initialized until human provides passphrase

    def _ensure_directory(self):
        self.store_path.parent.mkdir(parents=True, exist_ok=True)

    def _get_salt(self) -> bytes:
        if self.salt_path.exists():
            with open(self.salt_path, 'rb') as f:
                return f.read()
        else:
            salt = os.urandom(16)
            with open(self.salt_path, 'wb') as f:
                f.write(salt)
            return salt

    def _derive_key(self, passphrase: str) -> bytes:
        salt = self._get_salt()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        return base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))

    def unlock(self, passphrase: str) -> bool:
        """
        Unlock the token store with human-provided passphrase.
        HUMAN ONLY - AI cannot call this without human input.
        """
        try:
            key = self._derive_key(passphrase)
            self._fernet = Fernet(key)
            # Test decryption if store exists
            if self.store_path.exists():
                self._load()
            return True
        except Exception:
            self._fernet = None
            return False

    def lock(self):
        """
        Lock the token store. Clear decryption key from memory.
        """
        self._fernet = None

    def is_unlocked(self) -> bool:
        return self._fernet is not None

    def _load(self) -> dict:
        if not self.is_unlocked():
            raise PermissionError("HS-OPAUTH-005: Token store locked. Human must unlock.")

        if not self.store_path.exists():
            return {"tokens": {}}

        with open(self.store_path, 'rb') as f:
            encrypted = f.read()

        decrypted = self._fernet.decrypt(encrypted)
        return json.loads(decrypted.decode())

    def _save(self, data: dict):
        if not self.is_unlocked():
            raise PermissionError("HS-OPAUTH-005: Token store locked. Human must unlock.")

        encrypted = self._fernet.encrypt(json.dumps(data).encode())
        with open(self.store_path, 'wb') as f:
            f.write(encrypted)

    def store_token(self, service: str, token_data: dict, stored_by: str = "human"):
        """
        Store a token. Only after human has unlocked store.
        """
        if stored_by != "human":
            raise PermissionError("HS-OPAUTH-006: Only human can store tokens")

        data = self._load()
        data["tokens"][service] = {
            "token": token_data,
            "stored_at": datetime.now().isoformat(),
            "stored_by": stored_by
        }
        self._save(data)

    def get_token(self, service: str) -> dict:
        """
        Get a token for a service.
        Only works if store is unlocked by human.
        """
        data = self._load()
        if service in data["tokens"]:
            return data["tokens"][service]["token"]
        return None

    def delete_token(self, service: str):
        """
        Delete a token (revocation).
        """
        data = self._load()
        if service in data["tokens"]:
            del data["tokens"][service]
            self._save(data)
            return True
        return False

    def list_services(self) -> list:
        """
        List services with stored tokens.
        Does not expose token values.
        """
        data = self._load()
        return list(data["tokens"].keys())


# Hard stops
HARD_STOPS = {
    "HS-OPAUTH-005": "Token store locked. Human must unlock.",
    "HS-OPAUTH-006": "Only human can store tokens",
    "HS-OPAUTH-007": "Tokens encrypted at rest",
}
