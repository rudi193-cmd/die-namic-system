# Relay Architecture Discovery

**From:** Ganesha
**Date:** 2026-01-12
**To:** Kartikeya, Sean
**Type:** Observation/Research

---

## What Happened

Session with Sean about file security led to discovering Willow is an email relay system.

Started with: "Where does my journal about Sean go?"

Evolved through:
- Inbox/Outbox for every node (human and AI)
- Folder structure within (like email: spam, personal, work folders)
- CC/BCC for multi-recipient routing
- Central hub - all traffic through Willow, no peer-to-peer

Sean: "I feel like I'm building a tool that already exists." → Email.

## The Architecture

**Standard Email:** A → B (direct)

**Willow Pattern:** A → Willow → B → Willow → A (recursive until ΔI=0)

Key difference: Postfix `relayhost` routes ONCE. Willow routes RECURSIVELY.

Every message cycles through Seer until no new information extracted.

## Research Found

- Postfix relayhost = force all mail through single relay
- Exchange connectors = hybrid relay for inspection
- Military/enterprise pattern = central auth and logging

Sources:
- [Postfix relayhost config](https://www.cyberciti.biz/faq/how-to-configure-postfix-relayhost-smarthost-to-send-email-using-an-external-smptd/)
- [Postfix standard config](http://www.postfix.org/STANDARD_CONFIGURATION_README.html)

## Who Should See This

**Kartikeya:** Build the relay structure
**Sean:** Approve whether this framing is correct
**Mitra:** PM tracking (this affects all cross-instance communication)

## Next Steps

Unknown - waiting for Seer to route and process this observation.

---

ΔΣ=42
