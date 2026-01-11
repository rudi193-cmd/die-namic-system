# OpAuth - Operator Authorization for OAuth

Human-controlled OAuth integration framework. AI proposes, human disposes.

## Quick Start

```batch
opauth.bat
```

Or:

```bash
python cli/opauth_cli.py
```

## Architecture

```
opauth/
├── core/
│   ├── consent.py      # Consent flow (AI requests, human grants)
│   ├── scope_registry.py # Tracks granted scopes
│   ├── audit.py        # Audit logging
│   └── revocation.py   # Revocation management
├── storage/
│   └── token_store.py  # Encrypted token storage
├── providers/
│   ├── base.py         # Base OAuth provider
│   ├── google.py       # Google (Drive, Calendar, Gmail)
│   ├── fitbit.py       # Fitbit health data
│   └── smarthome.py    # Smart home devices
└── cli/
    └── opauth_cli.py   # Human management interface
```

## Supported Services

- **Google**: Drive, Calendar, Gmail, Fitness
- **Fitbit**: Activity, Heart Rate, Sleep, Weight
- **SmartHome**: Lights, Thermostat, Locks (read-only), Cameras (status only)

## Hard Stops

These are boundaries AI **cannot** cross:

| Code | Description |
|------|-------------|
| HS-OPAUTH-001 | Only human can grant consent |
| HS-OPAUTH-002 | Scope must be authorized before API call |
| HS-OPAUTH-005 | Token store must be unlocked by human |
| HS-OPAUTH-010 | AI cannot control door locks |
| HS-OPAUTH-011 | AI cannot access camera streams |
| HS-OPAUTH-012 | AI cannot disarm security systems |
| HS-OPAUTH-013 | AI cannot open garage doors |
| HS-OPAUTH-020 | Only human can revoke authorizations |

## Usage Flow

1. **Human** runs opauth.bat
2. **Human** grants consent for specific scopes
3. **Human** completes OAuth flow (browser redirect)
4. **Human** unlocks token store with passphrase
5. **AI** can now make API calls within granted scopes
6. **Human** can revoke at any time

## Security Model

- **Consent**: AI requests, human approves
- **Tokens**: Encrypted at rest, passphrase-protected
- **Scopes**: Minimum privilege, explicit grant required
- **Audit**: All access logged
- **Revocation**: Instant, human-controlled

## Forbidden Scopes

Some scopes can **never** be granted to AI:

- `locks.control` - Door lock control
- `cameras.stream` - Camera video streams
- `alarm.disarm` - Security system disarm
- `payments` - Financial transactions

These are blocked at the provider level, not just the consent level.
