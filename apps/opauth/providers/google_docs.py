"""
OpAuth Google Docs Provider
Read Google Docs with human-consented OAuth.
"""

from .google import GoogleProvider, GOOGLE_SCOPE_MAP

# Add Docs-specific scopes
GOOGLE_SCOPE_MAP.update({
    "docs.readonly": "https://www.googleapis.com/auth/documents.readonly",
    "drive.readonly": "https://www.googleapis.com/auth/drive.readonly",
})

class GoogleDocsProvider(GoogleProvider):
    """
    Google Docs reader with OAuth consent.
    Extends GoogleProvider for Docs-specific operations.
    """

    def __init__(self, client_id: str = None, client_secret: str = None, redirect_uri: str = None):
        super().__init__(client_id, client_secret, redirect_uri)
        self.service_name = "google_docs"

    def read_doc(self, doc_id: str) -> dict:
        """
        Read a Google Doc by ID.
        Requires: docs.readonly
        """
        if not self.check_scope("docs.readonly"):
            raise PermissionError("HS-OPAUTH-002: docs.readonly scope not authorized")

        endpoint = f"https://docs.googleapis.com/v1/documents/{doc_id}"
        return self.api_call(endpoint, "docs.readonly").json()

    def read_doc_text(self, doc_id: str) -> str:
        """
        Read a Google Doc and extract plain text.
        """
        doc = self.read_doc(doc_id)
        return self._extract_text(doc)

    def _extract_text(self, doc: dict) -> str:
        """
        Extract plain text from Google Docs API response.
        """
        text_parts = []
        content = doc.get("body", {}).get("content", [])

        for element in content:
            if "paragraph" in element:
                for para_element in element["paragraph"].get("elements", []):
                    if "textRun" in para_element:
                        text_parts.append(para_element["textRun"].get("content", ""))

        return "".join(text_parts)

    def read_gdoc_file(self, gdoc_path: str) -> str:
        """
        Read a .gdoc file from local path and fetch its content.
        .gdoc files contain JSON with the document URL/ID.
        """
        import json
        import re

        # Try to extract doc ID from gdoc file or path
        doc_id = self._extract_doc_id(gdoc_path)
        if doc_id:
            return self.read_doc_text(doc_id)

        raise ValueError(f"Could not extract document ID from: {gdoc_path}")

    def _extract_doc_id(self, path_or_url: str) -> str:
        """
        Extract Google Doc ID from various formats.
        """
        import re

        # Pattern for doc ID in URLs
        patterns = [
            r'/document/d/([a-zA-Z0-9-_]+)',
            r'/open\?id=([a-zA-Z0-9-_]+)',
            r'"doc_id":\s*"([a-zA-Z0-9-_]+)"',
            r'"url":\s*"[^"]*document/d/([a-zA-Z0-9-_]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, path_or_url)
            if match:
                return match.group(1)

        return None


def setup_gdoc_reader():
    """
    Interactive setup for Google Docs reader.
    Human must complete OAuth flow.
    """
    print("=" * 50)
    print("Google Docs Reader Setup")
    print("=" * 50)
    print()
    print("This will set up OAuth access to read Google Docs.")
    print("You'll need:")
    print("  1. Google Cloud Console project")
    print("  2. OAuth 2.0 credentials (client ID & secret)")
    print("  3. Enable Google Docs API")
    print()

    client_id = input("Client ID: ").strip()
    client_secret = input("Client Secret: ").strip()

    provider = GoogleDocsProvider(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8080/callback"
    )

    # Request authorization
    scope = ["docs.readonly", "drive.readonly"]
    auth_url = provider.get_auth_url(scope)

    print()
    print("Open this URL in your browser:")
    print(auth_url)
    print()

    auth_code = input("Paste the authorization code: ").strip()

    # Complete authorization
    token_data = provider.handle_callback(auth_code)
    provider.token_store.store_token("google_docs", token_data, stored_by="human")

    print()
    print("Setup complete! Google Docs access authorized.")
    return provider


if __name__ == "__main__":
    setup_gdoc_reader()
