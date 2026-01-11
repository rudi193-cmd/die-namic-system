"""
OpAuth CLI - Command Line Interface
Human-friendly management of OAuth authorizations.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.consent import ConsentFlow, GOOGLE_SCOPES, FITBIT_SCOPES, SMARTHOME_SCOPES
from core.revocation import RevocationManager
from core.audit import get_audit
from storage.token_store import TokenStore

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=" * 60)
    print("   OpAuth - Operator Authorization Manager")
    print("   Human controls AI's access to external services")
    print("=" * 60)
    print()

def print_menu():
    print("MAIN MENU")
    print("-" * 40)
    print("1. View Active Authorizations")
    print("2. Grant New Authorization")
    print("3. Revoke Authorization")
    print("4. Emergency Revoke All")
    print("5. View Audit Log")
    print("6. Unlock Token Store")
    print("7. Exit")
    print()

def view_authorizations():
    clear_screen()
    print_header()
    print("ACTIVE AUTHORIZATIONS")
    print("-" * 40)

    revocation = RevocationManager()
    status = revocation.list_active_authorizations()

    if not status["consented_services"]:
        print("No active authorizations.")
    else:
        for service, scopes in status["consented_services"].items():
            print(f"\n{service.upper()}")
            print(f"  Scopes: {', '.join(scopes) if scopes else 'None'}")
            print(f"  Token: {'Yes' if service in status['services_with_tokens'] else 'No'}")

    print()
    input("Press Enter to continue...")

def grant_authorization():
    clear_screen()
    print_header()
    print("GRANT AUTHORIZATION")
    print("-" * 40)
    print()
    print("Select service:")
    print("1. Google (Drive, Calendar, Gmail)")
    print("2. Fitbit (Health Data)")
    print("3. SmartHome (Lights, Thermostat)")
    print("0. Cancel")
    print()

    choice = input("Choice: ").strip()

    if choice == "0":
        return

    service_map = {
        "1": ("google", GOOGLE_SCOPES),
        "2": ("fitbit", FITBIT_SCOPES),
        "3": ("smarthome", SMARTHOME_SCOPES),
    }

    if choice not in service_map:
        print("Invalid choice.")
        input("Press Enter to continue...")
        return

    service, available_scopes = service_map[choice]

    clear_screen()
    print_header()
    print(f"GRANT {service.upper()} AUTHORIZATION")
    print("-" * 40)
    print()
    print("Available scopes:")

    scope_list = list(available_scopes.items())
    for i, (scope, desc) in enumerate(scope_list, 1):
        print(f"  {i}. {scope}: {desc}")

    print()
    print("Enter scope numbers (comma-separated), or 'all':")
    selection = input("Selection: ").strip()

    if selection.lower() == "all":
        selected_scopes = list(available_scopes.keys())
    else:
        try:
            indices = [int(x.strip()) - 1 for x in selection.split(",")]
            selected_scopes = [scope_list[i][0] for i in indices if 0 <= i < len(scope_list)]
        except (ValueError, IndexError):
            print("Invalid selection.")
            input("Press Enter to continue...")
            return

    if not selected_scopes:
        print("No scopes selected.")
        input("Press Enter to continue...")
        return

    print()
    print(f"You are about to grant AI access to: {', '.join(selected_scopes)}")
    print()
    confirm = input("Type 'GRANT' to confirm: ").strip()

    if confirm != "GRANT":
        print("Authorization cancelled.")
        input("Press Enter to continue...")
        return

    consent = ConsentFlow()
    consent.grant_consent(service, selected_scopes, granted_by="human")

    print()
    print(f"Authorization granted for {service}!")
    print(f"Scopes: {', '.join(selected_scopes)}")
    print()
    print("NOTE: AI still needs OAuth tokens to access the service.")
    print("Run the appropriate provider setup to complete OAuth flow.")
    input("Press Enter to continue...")

def revoke_authorization():
    clear_screen()
    print_header()
    print("REVOKE AUTHORIZATION")
    print("-" * 40)

    revocation = RevocationManager()
    status = revocation.list_active_authorizations()

    if not status["consented_services"]:
        print("No active authorizations to revoke.")
        input("Press Enter to continue...")
        return

    print()
    print("Select service to revoke:")
    services = list(status["consented_services"].keys())
    for i, service in enumerate(services, 1):
        print(f"  {i}. {service}")
    print("  0. Cancel")
    print()

    choice = input("Choice: ").strip()

    if choice == "0":
        return

    try:
        index = int(choice) - 1
        if index < 0 or index >= len(services):
            raise ValueError
        service = services[index]
    except ValueError:
        print("Invalid choice.")
        input("Press Enter to continue...")
        return

    print()
    print(f"You are about to REVOKE all access for: {service}")
    print("This will delete consent and tokens.")
    print()
    confirm = input("Type 'REVOKE' to confirm: ").strip()

    if confirm != "REVOKE":
        print("Revocation cancelled.")
        input("Press Enter to continue...")
        return

    result = revocation.revoke_service(service, revoked_by="human")

    print()
    print(f"Revocation complete for {service}:")
    print(f"  Consent revoked: {result['consent_revoked']}")
    print(f"  Token deleted: {result['token_deleted']}")
    input("Press Enter to continue...")

def emergency_revoke():
    clear_screen()
    print_header()
    print("!!! EMERGENCY REVOKE ALL !!!")
    print("-" * 40)
    print()
    print("WARNING: This will revoke ALL authorizations!")
    print("AI will lose access to ALL connected services.")
    print()
    confirm = input("Type 'EMERGENCY' to confirm: ").strip()

    if confirm != "EMERGENCY":
        print("Emergency revoke cancelled.")
        input("Press Enter to continue...")
        return

    revocation = RevocationManager()
    results = revocation.revoke_all(revoked_by="human")

    print()
    print("Emergency revocation complete!")
    for service, result in results.items():
        print(f"  {service}: consent={result['consent_revoked']}, token={result['token_deleted']}")
    input("Press Enter to continue...")

def view_audit():
    clear_screen()
    print_header()
    print("AUDIT LOG")
    print("-" * 40)
    print()

    audit = get_audit()
    log_file = audit.log_file

    if os.path.exists(log_file):
        print(f"Log file: {log_file}")
        print()
        with open(log_file, "r") as f:
            lines = f.readlines()
            # Show last 20 entries
            for line in lines[-20:]:
                print(line.strip())
    else:
        print("No audit log found.")

    print()
    input("Press Enter to continue...")

def unlock_store():
    clear_screen()
    print_header()
    print("UNLOCK TOKEN STORE")
    print("-" * 40)
    print()

    import getpass
    passphrase = getpass.getpass("Enter passphrase: ")

    store = TokenStore()
    if store.unlock(passphrase):
        print("Token store unlocked successfully!")
    else:
        print("Failed to unlock token store.")

    input("Press Enter to continue...")

def main():
    while True:
        clear_screen()
        print_header()
        print_menu()

        choice = input("Choice: ").strip()

        if choice == "1":
            view_authorizations()
        elif choice == "2":
            grant_authorization()
        elif choice == "3":
            revoke_authorization()
        elif choice == "4":
            emergency_revoke()
        elif choice == "5":
            view_audit()
        elif choice == "6":
            unlock_store()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
