"""
Read GDocs from Willow Inbox
Uses OpAuth Google credentials to read .gdoc files.
"""

import os
import sys
import json
import glob

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

INBOX_PATH = r"G:\My Drive\Willow\Sweet-Pea-Rudi19\Inbox"
OUTPUT_PATH = r"C:\Users\Sean\gdoc_exports"

def load_config():
    """Load Google credentials from config."""
    config_path = os.path.expanduser("~/.opauth/google_config.json")
    if not os.path.exists(config_path):
        print("ERROR: Google not configured. Run setup_google.bat first.")
        return None

    with open(config_path) as f:
        return json.load(f)

def get_provider(config):
    """Get configured GoogleDocsProvider."""
    from providers.google_docs import GoogleDocsProvider

    gd = config["google_docs"]
    provider = GoogleDocsProvider(
        client_id=gd["client_id"],
        client_secret=gd["client_secret"]
    )
    provider.token_store.store_token("google_docs", gd["token"], stored_by="human")
    return provider

def list_gdocs(inbox_path):
    """List all .gdoc files in inbox."""
    pattern = os.path.join(inbox_path, "*.gdoc")
    return glob.glob(pattern)

def extract_doc_id_from_gdoc(gdoc_path):
    """
    Extract document ID from .gdoc file.
    .gdoc files are JSON containing doc URL.
    """
    import re

    # Try reading as JSON (older format)
    try:
        with open(gdoc_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            url = data.get('url', '')
            match = re.search(r'/document/d/([a-zA-Z0-9-_]+)', url)
            if match:
                return match.group(1)
    except:
        pass

    # .gdoc files on Google Drive are actually shortcuts
    # The doc ID might be in the filename or we need Drive API
    return None

def read_and_export(provider, gdoc_path, output_dir):
    """Read a gdoc and export to text file."""
    filename = os.path.basename(gdoc_path)
    name = os.path.splitext(filename)[0]

    doc_id = extract_doc_id_from_gdoc(gdoc_path)

    if not doc_id:
        print(f"  Could not extract doc ID from: {filename}")
        print(f"  (Google Drive .gdoc files need Drive API to resolve)")
        return None

    try:
        text = provider.read_doc_text(doc_id)
        output_file = os.path.join(output_dir, f"{name}.txt")

        os.makedirs(output_dir, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"  Exported: {output_file}")
        return output_file

    except Exception as e:
        print(f"  Error reading {filename}: {e}")
        return None

def main():
    print("=" * 60)
    print("   Willow Inbox GDoc Reader")
    print("=" * 60)
    print()

    config = load_config()
    if not config:
        return

    provider = get_provider(config)

    gdocs = list_gdocs(INBOX_PATH)
    print(f"Found {len(gdocs)} .gdoc files in inbox")
    print()

    if not gdocs:
        print("No .gdoc files found.")
        return

    print("Reading gdocs...")
    print()

    exported = []
    for gdoc in gdocs:
        print(f"Processing: {os.path.basename(gdoc)}")
        result = read_and_export(provider, gdoc, OUTPUT_PATH)
        if result:
            exported.append(result)

    print()
    print(f"Exported {len(exported)} of {len(gdocs)} files")
    print(f"Output directory: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
