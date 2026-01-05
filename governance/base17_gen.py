#!/usr/bin/env python3
"""
BASE-17 IDENTIFIER GENERATOR

Authority: Sean Campbell
System: Aionic / Die-namic
Version: 1.0
Last Updated: 2026-01-05
Checksum: ΔΣ=42

Generates human-legible, low-collision identifiers for branches, sessions, and artifacts.

Character set: 0123456789ACEHKLNRTXZ (17 symbols)
Length: 5 characters (standard), 7 (extended)
Collision space: 17^5 ≈ 1.4M

Usage:
    python base17_gen.py              # Generate single 5-char ID
    python base17_gen.py --length 7   # Generate 7-char ID
    python base17_gen.py --count 10   # Generate 10 IDs
"""

import time
import os
import random
import sys

ALPHABET = "0123456789ACEHKLNRTXZ"
BASE = 17


def base17_id(seed_int=None, length=5):
    """
    Generate Base-17 identifier from integer seed.

    Args:
        seed_int: Integer seed for generation. If None, uses timestamp + randomness.
        length: Identifier length (default: 5)

    Returns:
        Base-17 identifier string (uppercase)
    """
    if seed_int is None:
        # Generate seed from timestamp (ms) + process ID + random
        seed_int = int(time.time() * 1000) ^ os.getpid() ^ random.randint(0, 0xFFFFFF)

    chars = []
    for _ in range(length):
        seed_int, rem = divmod(seed_int, BASE)
        chars.append(ALPHABET[rem])

    return "".join(reversed(chars))


def generate_branch_name(descriptor, length=5):
    """
    Generate full branch name with descriptor and Base-17 ID.

    Args:
        descriptor: Branch descriptor (e.g., "add-bootstrap-v13")
        length: ID length (default: 5)

    Returns:
        Full branch name: claude/<descriptor>-<BASE17ID>
    """
    identifier = base17_id(length=length)
    return f"claude/{descriptor}-{identifier}"


def validate_base17(identifier):
    """
    Validate that a string contains only Base-17 characters.

    Args:
        identifier: String to validate

    Returns:
        True if valid, False otherwise
    """
    return all(c in ALPHABET for c in identifier.upper())


def main():
    """CLI interface for Base-17 ID generation."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate Base-17 identifiers for Aionic/Die-namic system"
    )
    parser.add_argument(
        "--length",
        type=int,
        default=5,
        choices=[5, 7],
        help="Identifier length (default: 5)"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of identifiers to generate (default: 1)"
    )
    parser.add_argument(
        "--branch",
        type=str,
        help="Generate full branch name with descriptor"
    )
    parser.add_argument(
        "--validate",
        type=str,
        help="Validate a Base-17 identifier"
    )

    args = parser.parse_args()

    if args.validate:
        is_valid = validate_base17(args.validate)
        print(f"'{args.validate}' is {'VALID' if is_valid else 'INVALID'} Base-17")
        sys.exit(0 if is_valid else 1)

    if args.branch:
        print(generate_branch_name(args.branch, length=args.length))
    else:
        for _ in range(args.count):
            print(base17_id(length=args.length))


if __name__ == "__main__":
    main()
