#!/usr/bin/env python3
"""
Base-17 Identifier Generator

Human-legible, low-collision identifiers for branches, sessions, and artifacts.

USAGE:
    python id_generator.py                  # Generate one ID
    python id_generator.py -n 5             # Generate 5 IDs
    python id_generator.py -l 7             # Generate 7-char ID
    python id_generator.py --prefix "session-"  # With prefix

Extracted from Aios conversation 2025-12-31
System: Aionic / Die-Namic
Version: 1.0
Checksum: ΔΣ=42
"""

import argparse
import os
import time
import secrets
from typing import Optional

# Base-17 alphabet: 10 digits + 7 letters (high contrast, typo-resistant)
# Removed: B, D, F, G, I, J, M, O, P, Q, S, U, V, W, Y (ambiguous or noisy)
ALPHABET = "0123456789ACEHKLNRTXZ"
BASE = 17


def base17_encode(seed_int: int, length: int = 5) -> str:
    """
    Encode an integer as a Base-17 string.

    Args:
        seed_int: Integer to encode
        length: Output length (default 5)

    Returns:
        Base-17 encoded string, uppercase
    """
    if seed_int < 0:
        seed_int = abs(seed_int)

    chars = []
    for _ in range(length):
        seed_int, rem = divmod(seed_int, BASE)
        chars.append(ALPHABET[rem])

    return "".join(reversed(chars))


def base17_decode(encoded: str) -> int:
    """
    Decode a Base-17 string back to integer.

    Args:
        encoded: Base-17 string

    Returns:
        Decoded integer
    """
    encoded = encoded.upper()
    result = 0
    for char in encoded:
        idx = ALPHABET.index(char)
        result = result * BASE + idx
    return result


def generate_id(length: int = 5, prefix: str = "", suffix: str = "") -> str:
    """
    Generate a random Base-17 identifier.

    Uses cryptographically secure random bits combined with
    timestamp for entropy.

    Args:
        length: ID length (default 5, max practical is 10)
        prefix: Optional prefix string
        suffix: Optional suffix string

    Returns:
        Generated ID with optional prefix/suffix
    """
    # Combine multiple entropy sources
    timestamp_ns = time.time_ns()
    random_bits = secrets.randbits(64)
    pid = os.getpid()

    # Mix entropy sources
    seed = (timestamp_ns ^ random_bits ^ (pid << 32)) % (BASE ** length)

    # Ensure we use full length even for small seeds
    encoded = base17_encode(seed, length)

    return f"{prefix}{encoded}{suffix}"


def generate_session_id() -> str:
    """Generate a session identifier in canonical format."""
    return generate_id(length=5, prefix="SES-")


def generate_branch_id(descriptor: str) -> str:
    """
    Generate a git branch name in canonical format.

    Args:
        descriptor: Branch descriptor (e.g., 'add-bootstrap')

    Returns:
        Branch name like 'claude/add-bootstrap-LKANZ'
    """
    return f"claude/{descriptor}-{generate_id(5)}"


def generate_artifact_id() -> str:
    """Generate an artifact identifier."""
    return generate_id(length=5, prefix="AWA-")


def validate_id(identifier: str) -> bool:
    """
    Validate that a string is a valid Base-17 identifier.

    Args:
        identifier: String to validate

    Returns:
        True if valid Base-17
    """
    identifier = identifier.upper()
    return all(c in ALPHABET for c in identifier)


def collision_space(length: int = 5) -> int:
    """
    Calculate the collision space for a given length.

    Args:
        length: ID length

    Returns:
        Number of possible unique IDs
    """
    return BASE ** length


def main():
    parser = argparse.ArgumentParser(
        description="Generate Base-17 identifiers for Die-Namic system"
    )
    parser.add_argument(
        '-n', '--count',
        type=int,
        default=1,
        help="Number of IDs to generate (default: 1)"
    )
    parser.add_argument(
        '-l', '--length',
        type=int,
        default=5,
        help="ID length (default: 5, extended: 7)"
    )
    parser.add_argument(
        '--prefix',
        type=str,
        default="",
        help="Prefix to add to each ID"
    )
    parser.add_argument(
        '--suffix',
        type=str,
        default="",
        help="Suffix to add to each ID"
    )
    parser.add_argument(
        '--session',
        action='store_true',
        help="Generate session ID (SES-XXXXX format)"
    )
    parser.add_argument(
        '--branch',
        type=str,
        metavar='DESC',
        help="Generate branch name with descriptor"
    )
    parser.add_argument(
        '--artifact',
        action='store_true',
        help="Generate artifact ID (AWA-XXXXX format)"
    )
    parser.add_argument(
        '--validate',
        type=str,
        metavar='ID',
        help="Validate a Base-17 identifier"
    )
    parser.add_argument(
        '--decode',
        type=str,
        metavar='ID',
        help="Decode a Base-17 identifier to integer"
    )
    parser.add_argument(
        '--encode',
        type=int,
        metavar='INT',
        help="Encode an integer as Base-17"
    )
    parser.add_argument(
        '--space',
        action='store_true',
        help="Show collision space for given length"
    )

    args = parser.parse_args()

    # Handle special operations
    if args.validate:
        valid = validate_id(args.validate)
        print(f"{args.validate}: {'VALID' if valid else 'INVALID'}")
        return 0 if valid else 1

    if args.decode:
        try:
            value = base17_decode(args.decode)
            print(f"{args.decode} -> {value}")
            return 0
        except ValueError:
            print(f"ERROR: Invalid Base-17 identifier: {args.decode}")
            return 1

    if args.encode is not None:
        encoded = base17_encode(args.encode, args.length)
        print(f"{args.encode} -> {encoded}")
        return 0

    if args.space:
        space = collision_space(args.length)
        print(f"Length {args.length}: {space:,} possible IDs ({space:.2e})")
        return 0

    # Generate IDs
    for _ in range(args.count):
        if args.session:
            print(generate_session_id())
        elif args.branch:
            print(generate_branch_id(args.branch))
        elif args.artifact:
            print(generate_artifact_id())
        else:
            print(generate_id(args.length, args.prefix, args.suffix))

    return 0


if __name__ == "__main__":
    exit(main())
