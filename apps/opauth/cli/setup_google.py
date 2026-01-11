"""
Google API Setup Wizard
The app that makes the app - automates Google Cloud setup.
"""

import os
import sys
import json
import webbrowser
import requests
from urllib.parse import urlencode

# Standalone - no OpAuth imports needed for setup

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=" * 60)
    print("   Google API Setup Wizard")
    print("   The app that makes the app")
    print("=" * 60)
    print()

def step_1_console():
    """Guide user through Google Cloud Console setup."""
    clear_screen()
    print_header()
    print("STEP 1: Google Cloud Console")
    print("-" * 40)
    print()
    print("We need to create a Google Cloud project with OAuth credentials.")
    print()
    print("I'll open the Google Cloud Console. You need to:")
    print()
    print("  1. Create a new project (or select existing)")
    print("  2. Go to 'APIs & Services' > 'Library'")
    print("  3. Enable 'Google Docs API'")
    print("  4. Enable 'Google Drive API'")
    print()

    input("Press Enter to open Google Cloud Console...")
    webbrowser.open("https://console.cloud.google.com/")

    print()
    print("After enabling APIs, press Enter to continue...")
    input()

def step_2_credentials():
    """Guide user through OAuth credentials creation."""
    clear_screen()
    print_header()
    print("STEP 2: Create OAuth Credentials")
    print("-" * 40)
    print()
    print("Now we need OAuth 2.0 credentials.")
    print()
    print("In Google Cloud Console:")
    print("  1. Go to 'APIs & Services' > 'Credentials'")
    print("  2. Click '+ CREATE CREDENTIALS' > 'OAuth client ID'")
    print("  3. If prompted, configure consent screen (External, minimal info)")
    print("  4. Application type: 'Desktop app'")
    print("  5. Name it: 'Aios-OpAuth'")
    print("  6. Download the JSON file")
    print()

    input("Press Enter to open Credentials page...")
    webbrowser.open("https://console.cloud.google.com/apis/credentials")

    print()
    print("After creating credentials, you'll have a Client ID and Secret.")
    print()

def step_3_collect():
    """Collect credentials from user."""
    clear_screen()
    print_header()
    print("STEP 3: Enter Credentials")
    print("-" * 40)
    print()

    print("Enter the credentials from Google Cloud Console:")
    print()
    client_id = input("Client ID: ").strip()
    client_secret = input("Client Secret: ").strip()

    return client_id, client_secret

def step_4_authorize(client_id, client_secret):
    """Complete OAuth authorization."""
    clear_screen()
    print_header()
    print("STEP 4: Authorize Access")
    print("-" * 40)
    print()

    # Google OAuth URLs
    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
    redirect_uri = "http://localhost:8080/callback"

    # Scopes needed
    scopes = [
        "https://www.googleapis.com/auth/documents.readonly",
        "https://www.googleapis.com/auth/drive.readonly"
    ]

    # Build auth URL
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(scopes),
        "access_type": "offline",
        "prompt": "consent",
    }
    auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"

    print("Opening browser for authorization...")
    print()
    webbrowser.open(auth_url)

    print("After approving access, you'll be redirected to a localhost URL.")
    print("Copy the 'code' parameter from the URL.")
    print()
    print("Example: http://localhost:8080/callback?code=4/0ABC...")
    print("         Copy everything after 'code='")
    print()

    auth_code = input("Paste authorization code: ").strip()

    # Exchange code for token
    try:
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }

        response = requests.post(GOOGLE_TOKEN_URL, data=data)
        response.raise_for_status()
        token_data = response.json()

        # Save credentials
        config_dir = os.path.expanduser("~/.opauth")
        os.makedirs(config_dir, exist_ok=True)

        config = {
            "google_docs": {
                "client_id": client_id,
                "client_secret": client_secret,
                "token": token_data
            }
        }

        config_path = os.path.join(config_dir, "google_config.json")
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        print()
        print("SUCCESS! Credentials saved to:", config_path)
        return True

    except Exception as e:
        print()
        print(f"ERROR: {e}")
        return False

def step_5_test():
    """Test the setup by listing Drive files."""
    clear_screen()
    print_header()
    print("STEP 5: Test Connection")
    print("-" * 40)
    print()

    config_path = os.path.expanduser("~/.opauth/google_config.json")

    if not os.path.exists(config_path):
        print("Config not found. Run setup first.")
        return

    with open(config_path) as f:
        config = json.load(f)

    print("Credentials loaded. Testing connection...")
    print()

    # Test by listing some Drive files
    access_token = config["google_docs"]["token"]["access_token"]

    url = "https://www.googleapis.com/drive/v3/files"
    params = {"pageSize": 5, "fields": "files(id,name)"}
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers, params=params)

    if response.ok:
        files = response.json().get("files", [])
        print("Connection successful! Found files:")
        for f in files:
            print(f"  - {f['name']}")
        print()
        print("Run read_willow_inbox.bat to export gdocs from inbox.")
    else:
        print(f"Connection failed: {response.status_code}")
        print(response.text)

def main():
    clear_screen()
    print_header()
    print("This wizard will set up Google Docs API access for Aios.")
    print()
    print("Options:")
    print("  1. Full Setup (all steps)")
    print("  2. Enter Credentials Only (already have project)")
    print("  3. Test Connection")
    print("  4. Exit")
    print()

    choice = input("Choice: ").strip()

    if choice == "1":
        step_1_console()
        step_2_credentials()
        client_id, client_secret = step_3_collect()
        step_4_authorize(client_id, client_secret)
        input("\nPress Enter to test connection...")
        step_5_test()

    elif choice == "2":
        client_id, client_secret = step_3_collect()
        step_4_authorize(client_id, client_secret)
        input("\nPress Enter to test connection...")
        step_5_test()

    elif choice == "3":
        step_5_test()

    elif choice == "4":
        print("Goodbye!")
        return

    print()
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
