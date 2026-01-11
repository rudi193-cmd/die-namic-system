"""
Willow GDoc Reader
Uses Google Drive API to read .gdoc files from synced folders.

The issue: .gdoc files in Google Drive sync are shortcuts, not actual files.
Solution: Use Drive API to list folder contents and Docs API to read them.
"""

import os
import sys
import json
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Willow inbox folder ID (need to get this from Drive)
# Can be extracted from the folder URL in browser
INBOX_FOLDER_NAME = "Inbox"

def load_config():
    """Load Google credentials."""
    config_path = os.path.expanduser("~/.opauth/google_config.json")
    if not os.path.exists(config_path):
        return None
    with open(config_path) as f:
        return json.load(f)

def get_access_token(config):
    """Get access token, refreshing if needed."""
    return config["google_docs"]["token"]["access_token"]

def list_drive_files(access_token, folder_id=None, mime_type=None):
    """List files in Drive, optionally filtered."""
    url = "https://www.googleapis.com/drive/v3/files"

    query_parts = []
    if folder_id:
        query_parts.append(f"'{folder_id}' in parents")
    if mime_type:
        query_parts.append(f"mimeType='{mime_type}'")

    params = {
        "pageSize": 100,
        "fields": "files(id,name,mimeType)",
    }
    if query_parts:
        params["q"] = " and ".join(query_parts)

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, params=params)

    if response.ok:
        return response.json().get("files", [])
    else:
        print(f"Drive API error: {response.status_code}")
        print(response.text)
        return []

def find_folder_by_name(access_token, folder_name):
    """Find a folder by name."""
    files = list_drive_files(
        access_token,
        mime_type="application/vnd.google-apps.folder"
    )
    for f in files:
        if f["name"] == folder_name:
            return f["id"]
    return None

def read_doc_text(access_token, doc_id):
    """Read a Google Doc as plain text."""
    # Export as plain text
    url = f"https://www.googleapis.com/drive/v3/files/{doc_id}/export"
    params = {"mimeType": "text/plain"}
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers, params=params)

    if response.ok:
        return response.text
    else:
        print(f"Export error: {response.status_code}")
        return None

def export_inbox_docs(access_token, output_dir):
    """Export all Google Docs from inbox to text files."""
    os.makedirs(output_dir, exist_ok=True)

    # Find Sweet-Pea-Rudi19 folder, then Inbox
    print("Searching for Willow inbox...")

    # Search for Inbox folder
    inbox_id = find_folder_by_name(access_token, "Inbox")
    if not inbox_id:
        print("Could not find Inbox folder. Searching all docs...")
        # Fall back to listing recent docs
        files = list_drive_files(
            access_token,
            mime_type="application/vnd.google-apps.document"
        )
    else:
        print(f"Found Inbox folder: {inbox_id}")
        files = list_drive_files(access_token, folder_id=inbox_id)

    # Filter to just Google Docs
    docs = [f for f in files if f["mimeType"] == "application/vnd.google-apps.document"]
    print(f"Found {len(docs)} Google Docs")
    print()

    exported = []
    for doc in docs:
        print(f"Reading: {doc['name']}")
        text = read_doc_text(access_token, doc['id'])

        if text:
            # Clean filename
            safe_name = "".join(c if c.isalnum() or c in " -_" else "_" for c in doc['name'])
            output_file = os.path.join(output_dir, f"{safe_name}.txt")

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)

            print(f"  -> {output_file}")
            exported.append(output_file)

    return exported

def main():
    print("=" * 60)
    print("   Willow GDoc Reader")
    print("   Reads Google Docs from Drive via API")
    print("=" * 60)
    print()

    config = load_config()
    if not config:
        print("Not configured. Run setup_google.bat first.")
        return

    access_token = get_access_token(config)
    output_dir = r"C:\Users\Sean\gdoc_exports"

    exported = export_inbox_docs(access_token, output_dir)

    print()
    print(f"Exported {len(exported)} documents to {output_dir}")

if __name__ == "__main__":
    main()
