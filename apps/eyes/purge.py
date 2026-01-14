#!/usr/bin/env python3
"""
Smart Screenshot Purge — Content-aware deletion

Only deletes low-value screenshots after scanning content.
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent for imports
sys.path.insert(0, str(Path(__file__).parent))

from content_scan import scan_screenshot, OCR_AVAILABLE

SCREENSHOTS_DIR = Path(r"C:\Users\Sean\screenshots")
ROUTED_DIR = SCREENSHOTS_DIR / "routed"
PURGE_LOG = SCREENSHOTS_DIR / "purge.log"

# Defaults
DEFAULT_TARGET_MB = 500
DEFAULT_MIN_AGE_HOURS = 24
DEFAULT_MIN_SCORE = 3


def log_purge(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(PURGE_LOG, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {msg}\n")
    print(msg)


def get_routed_files():
    """Get set of filenames that have been routed."""
    routed = set()
    if ROUTED_DIR.exists():
        for f in ROUTED_DIR.rglob("*.png"):
            routed.add(f.name)
    return routed


def get_folder_size_mb(folder):
    """Get total size of PNG files in MB."""
    total = sum(f.stat().st_size for f in Path(folder).glob("*.png"))
    return total / (1024 * 1024)


def smart_purge(target_mb=DEFAULT_TARGET_MB, min_age_hours=DEFAULT_MIN_AGE_HOURS,
                min_score=DEFAULT_MIN_SCORE, dry_run=True):
    """
    Smart purge that scans content before deleting.

    Args:
        target_mb: Target size in MB
        min_age_hours: Don't touch files newer than this
        min_score: Keep files with score >= this
        dry_run: If True, don't actually delete

    Returns:
        dict with stats
    """
    if not OCR_AVAILABLE:
        log_purge("ERROR: OCR not available, cannot scan content")
        return {"error": "ocr_unavailable"}

    current_mb = get_folder_size_mb(SCREENSHOTS_DIR)
    log_purge(f"PURGE START | current={current_mb:.1f}MB | target={target_mb}MB | dry_run={dry_run}")

    if current_mb <= target_mb:
        log_purge(f"Already under target ({current_mb:.1f}MB <= {target_mb}MB)")
        return {"already_under_target": True, "current_mb": current_mb}

    # Get routed files (always keep)
    routed = get_routed_files()
    log_purge(f"Protected routed files: {len(routed)}")

    # Get all screenshots sorted by age (oldest first)
    files = sorted(SCREENSHOTS_DIR.glob("*.png"), key=lambda f: f.stat().st_mtime)
    now = datetime.now()

    to_delete = []
    to_keep = []
    scanned = 0

    for f in files:
        # Skip routed files
        if f.name in routed:
            to_keep.append(f)
            continue

        # Skip recent files
        age_hours = (now - datetime.fromtimestamp(f.stat().st_mtime)).total_seconds() / 3600
        if age_hours < min_age_hours:
            to_keep.append(f)
            continue

        # Scan content
        scanned += 1
        result = scan_screenshot(f)
        score = result.get('score', 10)  # Default high if scan fails

        if score < min_score:
            to_delete.append(f)
            log_purge(f"  MARK DELETE | {f.name} | score={score} | age={age_hours:.1f}h")
        else:
            to_keep.append(f)

        # Check if we've found enough to delete
        delete_size = sum(x.stat().st_size for x in to_delete) / (1024 * 1024)
        remaining = current_mb - delete_size
        if remaining <= target_mb:
            log_purge(f"Found enough to delete ({delete_size:.1f}MB)")
            break

    # Calculate savings
    delete_size_mb = sum(f.stat().st_size for f in to_delete) / (1024 * 1024)

    # Execute deletion
    deleted_count = 0
    if not dry_run and to_delete:
        for f in to_delete:
            try:
                f.unlink()
                deleted_count += 1
            except Exception as e:
                log_purge(f"  ERROR deleting {f.name}: {e}")

    final_mb = get_folder_size_mb(SCREENSHOTS_DIR) if not dry_run else current_mb - delete_size_mb

    stats = {
        "scanned": scanned,
        "to_delete": len(to_delete),
        "deleted": deleted_count,
        "kept": len(to_keep),
        "protected_routed": len(routed),
        "savings_mb": round(delete_size_mb, 2),
        "before_mb": round(current_mb, 2),
        "after_mb": round(final_mb, 2),
        "dry_run": dry_run
    }

    log_purge(f"PURGE END | scanned={scanned} | deleted={deleted_count} | saved={delete_size_mb:.1f}MB | final={final_mb:.1f}MB")

    return stats


def quick_purge(target_mb=DEFAULT_TARGET_MB, min_age_hours=48, dry_run=True):
    """
    Fast purge without OCR — deletes oldest unrouted files first.
    Use when you need to free space quickly.
    """
    current_mb = get_folder_size_mb(SCREENSHOTS_DIR)
    log_purge(f"QUICK PURGE | current={current_mb:.1f}MB | target={target_mb}MB | dry_run={dry_run}")

    if current_mb <= target_mb:
        log_purge(f"Already under target")
        return {"already_under_target": True, "current_mb": current_mb}

    # Get routed files (always keep)
    routed = get_routed_files()

    # Get all screenshots sorted by age (oldest first)
    files = sorted(SCREENSHOTS_DIR.glob("*.png"), key=lambda f: f.stat().st_mtime)
    now = datetime.now()

    to_delete = []
    total_delete_size = 0
    need_to_free = (current_mb - target_mb) * 1024 * 1024  # bytes

    for f in files:
        # Skip routed
        if f.name in routed:
            continue

        # Skip recent
        age_hours = (now - datetime.fromtimestamp(f.stat().st_mtime)).total_seconds() / 3600
        if age_hours < min_age_hours:
            continue

        to_delete.append(f)
        total_delete_size += f.stat().st_size

        if total_delete_size >= need_to_free:
            break

    # Execute
    deleted_count = 0
    if not dry_run:
        for f in to_delete:
            try:
                f.unlink()
                deleted_count += 1
            except:
                pass

    savings_mb = total_delete_size / (1024 * 1024)
    final_mb = current_mb - savings_mb if not dry_run else current_mb

    log_purge(f"QUICK PURGE END | marked={len(to_delete)} | deleted={deleted_count} | saved={savings_mb:.1f}MB")

    return {
        "to_delete": len(to_delete),
        "deleted": deleted_count,
        "savings_mb": round(savings_mb, 2),
        "before_mb": round(current_mb, 2),
        "after_mb": round(final_mb if not dry_run else current_mb - savings_mb, 2),
        "dry_run": dry_run
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Smart screenshot purge")
    parser.add_argument("--target", type=int, default=DEFAULT_TARGET_MB, help="Target size in MB")
    parser.add_argument("--min-age", type=int, default=DEFAULT_MIN_AGE_HOURS, help="Min age in hours to consider")
    parser.add_argument("--min-score", type=int, default=DEFAULT_MIN_SCORE, help="Min score to keep (0-10)")
    parser.add_argument("--execute", action="store_true", help="Actually delete (default is dry run)")
    parser.add_argument("--quick", action="store_true", help="Quick mode: no OCR, just delete oldest unrouted")

    args = parser.parse_args()

    if args.quick:
        print(f"Quick Purge (no OCR)")
        print(f"  Target: {args.target}MB")
        print(f"  Min age: {args.min_age}h")
        print(f"  Mode: {'EXECUTE' if args.execute else 'DRY RUN'}")
        print()

        stats = quick_purge(
            target_mb=args.target,
            min_age_hours=args.min_age,
            dry_run=not args.execute
        )
    else:
        print(f"Smart Purge (with OCR)")
        print(f"  Target: {args.target}MB")
        print(f"  Min age: {args.min_age}h")
        print(f"  Min score to keep: {args.min_score}")
        print(f"  Mode: {'EXECUTE' if args.execute else 'DRY RUN'}")
        print()

        stats = smart_purge(
            target_mb=args.target,
            min_age_hours=args.min_age,
            min_score=args.min_score,
            dry_run=not args.execute
        )

    print()
    print("Results:")
    for k, v in stats.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
