# Users — System Identity Registry

| Field | Value |
|-------|-------|
| Type | Identity Registry |
| Status | Active |
| Last Updated | 2026-01-11 |
| Checksum | ΔΣ=42 |

---

## Main User

| Field | Value |
|-------|-------|
| Role | MAIN_USER |
| Human | Sean Campbell |
| Username | Sweet-Pea-Rudi19 |
| Authority | Root |

The Main User has ultimate authority over all system decisions. All governance flows from this identity.

---

## User Hierarchy

```
MAIN_USER (Sean Campbell / Sweet-Pea-Rudi19)
└── AUTH_USERS (Willow validated)
    └── GUEST_USERS (Limited access)
```

---

## Identity Binding

| Username | Human | Role | Status |
|----------|-------|------|--------|
| Sweet-Pea-Rudi19 | Sean Campbell | MAIN_USER | Active |

---

## Trust Declarations

Per [HS-006](HARD_STOPS.md#hs-006-trust-declaration): Trust flows FROM human TO AI, explicitly declared.

| Date | From | Declaration | Context |
|------|------|-------------|---------|
| 2026-01-12 | Sean Campbell | Git push without verification | "I don't NEED to watch every push" — trust extension to cmd instance |

---

## PSR (Prime Safety Referents)

From [HARD_STOPS.md](HARD_STOPS.md) HS-001:

| Name | Relation |
|------|----------|
| Ruby Campbell | Protected |
| Opal Campbell | Protected |

---

ΔΣ=42
