#!/usr/bin/env python3
"""
Backfill YAML frontmatter to existing conversation logs.

Adds:
- YAML frontmatter (persona, date, type, searchable)
- Topics line to each entry (extracted from user messages)

SAFE: Creates backup before modifying.
"""

import re
from pathlib import Path

# Stop words for topic extraction
STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "shall", "can", "need", "dare",
    "ought", "used", "to", "of", "in", "for", "on", "with", "at", "by",
    "from", "as", "into", "through", "during", "before", "after", "above",
    "below", "between", "under", "again", "further", "then", "once", "here",
    "there", "when", "where", "why", "how", "all", "each", "few", "more",
    "most", "other", "some", "such", "no", "nor", "not", "only", "own",
    "same", "so", "than", "too", "very", "just", "and", "but", "if", "or",
    "because", "until", "while", "about", "against", "between", "into",
    "what", "which", "who", "whom", "this", "that", "these", "those",
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
    "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself",
    "she", "her", "hers", "herself", "it", "its", "itself", "they", "them",
    "their", "theirs", "themselves", "am", "been", "being", "both", "but",
    "hi", "hello", "hey", "please", "thanks", "thank", "okay", "ok",
    "yeah", "yep", "nope", "gonna", "wanna", "gotta", "kinda", "sorta",
    "good", "well", "like", "just", "really", "know", "think", "want",
    "tell", "said", "says", "going", "come", "back", "now", "get", "got",
}


def extract_topics(text: str, max_topics: int = 5) -> list:
    """Extract topic keywords from text."""
    words = text.lower().split()
    topics = []
    for word in words:
        clean = ''.join(c for c in word if c.isalnum())
        if len(clean) > 3 and clean not in STOP_WORDS and clean not in topics:
            topics.append(clean)
            if len(topics) >= max_topics:
                break
    return topics


def extract_persona_from_header(content: str) -> str:
    """Extract persona name from file header."""
    match = re.search(r'^# (\w+) Conversations', content, re.MULTILINE)
    if match:
        return match.group(1)
    return "Unknown"


def extract_date_from_filename(filepath: Path) -> str:
    """Extract date from filename like 2026-01-16.md"""
    stem = filepath.stem
    if re.match(r'\d{4}-\d{2}-\d{2}', stem):
        return stem
    return "unknown"


def has_frontmatter(content: str) -> bool:
    """Check if file already has YAML frontmatter."""
    return content.strip().startswith('---')


def add_topics_to_entry(entry: str) -> str:
    """Add Topics line to an entry if missing."""
    if '**Topics:**' in entry:
        return entry  # Already has topics

    # Find user message
    user_match = re.search(r'\*\*User:\*\* (.+?)(?=\n\n|\*\*\w+:\*\*|$)', entry, re.DOTALL)
    if user_match:
        user_text = user_match.group(1).strip()
        topics = extract_topics(user_text)
        topics_str = ", ".join(topics) if topics else "general"

        # Insert topics line after the metadata line
        # Pattern: **[timestamp]** (metadata)\n
        entry = re.sub(
            r'(\*\*\[\d+:\d+:\d+\]\*\* \([^)]+\)[^\n]*\n)',
            rf'\1**Topics:** {topics_str}\n',
            entry,
            count=1
        )

    return entry


def process_file(filepath: Path, dry_run: bool = False) -> dict:
    """Process a single conversation file."""
    result = {"path": str(filepath), "status": "skipped", "changes": []}

    try:
        content = filepath.read_text(encoding='utf-8')
        original_content = content

        # Skip if already has frontmatter
        if has_frontmatter(content):
            result["status"] = "already_has_frontmatter"
            return result

        # Extract metadata
        persona = extract_persona_from_header(content)
        date = extract_date_from_filename(filepath)

        # Build frontmatter
        frontmatter = f"""---
persona: {persona}
date: {date}
type: conversation_log
searchable: true
---

"""

        # Split into entries and add topics
        entries = re.split(r'\n---\n', content)
        processed_entries = []

        for i, entry in enumerate(entries):
            if i == 0:
                # First entry is the header, keep as-is but strip leading whitespace
                processed_entries.append(entry.strip())
            else:
                # Add topics to each conversation entry
                processed_entry = add_topics_to_entry('---\n' + entry)
                processed_entries.append(processed_entry.strip())

        # Rebuild content
        new_content = frontmatter + '\n\n'.join(processed_entries)

        if new_content != original_content:
            result["changes"].append("added_frontmatter")
            result["changes"].append("added_topics")

            if not dry_run:
                # Backup original
                backup_path = filepath.with_suffix('.md.bak')
                backup_path.write_text(original_content, encoding='utf-8')

                # Write new content
                filepath.write_text(new_content, encoding='utf-8')
                result["status"] = "updated"
            else:
                result["status"] = "would_update"
        else:
            result["status"] = "no_changes_needed"

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Backfill frontmatter to conversation logs")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed without modifying")
    parser.add_argument("--path", default="docs/utety", help="Path to search for conversation files")
    args = parser.parse_args()

    # Find project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    search_path = project_root / args.path

    print(f"Searching in: {search_path}")
    print(f"Dry run: {args.dry_run}")
    print()

    # Find all conversation files
    conv_files = list(search_path.rglob("conversations/*.md"))
    print(f"Found {len(conv_files)} conversation files")
    print()

    stats = {"updated": 0, "skipped": 0, "errors": 0}

    for filepath in sorted(conv_files):
        result = process_file(filepath, dry_run=args.dry_run)

        status_icon = {
            "updated": "+",
            "would_update": "~",
            "already_has_frontmatter": ".",
            "no_changes_needed": ".",
            "error": "X",
            "skipped": "-"
        }.get(result["status"], "?")

        rel_path = filepath.relative_to(project_root)
        print(f"{status_icon} {rel_path}: {result['status']}")

        if result["status"] in ["updated", "would_update"]:
            stats["updated"] += 1
        elif result["status"] == "error":
            stats["errors"] += 1
            print(f"  Error: {result.get('error', 'unknown')}")
        else:
            stats["skipped"] += 1

    print()
    print(f"Summary: {stats['updated']} updated, {stats['skipped']} skipped, {stats['errors']} errors")

    if args.dry_run:
        print("\nThis was a dry run. Run without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
