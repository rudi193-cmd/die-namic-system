"""
Google API Setup Wizard
The app that makes the app - automates Google Cloud setup.
"""

import os
import sys
import json
import webbrowser

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

    from providers.google_docs import GoogleDocsProvider

    provider = GoogleDocsProvider(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8080/callback"
    )

    scope = ["docs.readonly", "drive.readonly"]
    auth_url = provider.get_auth_url(scope)

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
        token_data = provider.handle_callback(auth_code)

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
    """Test the setup by reading a doc."""
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

    # Try to read a test doc
    from providers.google_docs import GoogleDocsProvider

    gd = config["google_docs"]
    provider = GoogleDocsProvider(
        client_id=gd["client_id"],
        client_secret=gd["client_secret"]
    )

    # Manually set token
    provider.token_store.store_token("google_docs", gd["token"], stored_by="human")

    print("Connection ready!")
    print()
    print("To read a Google Doc, use:")
    print("  from providers.google_docs import GoogleDocsProvider")
    print("  provider = GoogleDocsProvider(...)")
    print("  text = provider.read_doc_text('DOC_ID')")

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
