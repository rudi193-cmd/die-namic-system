#!/usr/bin/env python3
"""
Import Claude History — Parse official Anthropic export into Die-Namic format.

USAGE:
    python import_claude_history.py <conversations.json> [--persona NAME] [--output DIR]

EXAMPLES:
    python import_claude_history.py ~/Downloads/claude_export/conversations.json
    python import_claude_history.py conversations.json --persona Willow
    python import_claude_history.py conversations.json --persona Kartikeya --output ./imported

DEFAULT BEHAVIOR:
    - Persona defaults to "Claude" (creates docs/utety/claude/conversations/)
    - Output defaults to project's docs/utety/ folder
    - Groups conversations by date
    - Preserves conversation titles and timestamps

AUTHOR: Kartikeya (wired by Claude)
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional


def parse_claude_export(json_path: Path) -> list:
    """
    Parse official Anthropic export JSON.

    Expected format:
    [
        {
            "uuid": "conv_abc123",
            "name": "Conversation title",
            "created_at": "2024-01-15T10:30:00.000Z",
            "chat_messages": [
                {"text": "...", "sender": "human", "created_at": "..."},
                {"text": "...", "sender": "assistant", "created_at": "..."}
            ]
        }
    ]
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Handle both array format and wrapper format
    if isinstance(data, dict):
        # Some exports wrap in {"conversations": [...]}
        data = data.get('conversations', data.get('chats', [data]))

    return data


def format_conversation_to_markdown(conversation: dict, persona: str) -> tuple[str, str]:
    """
    Convert a single conversation to markdown format.

    Returns (date_str, markdown_content)
    """
    title = conversation.get('name', 'Untitled')
    created = conversation.get('created_at', '')
    messages = conversation.get('chat_messages', [])

    # Parse date for grouping
    try:
        dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
        date_str = dt.strftime('%Y-%m-%d')
        time_str = dt.strftime('%H:%M:%S')
    except (ValueError, AttributeError):
        date_str = datetime.now().strftime('%Y-%m-%d')
        time_str = "00:00:00"

    # Build markdown
    lines = [
        f"\n---",
        f"### {title}",
        f"*Imported from Claude.ai | Started {time_str}*\n"
    ]

    for msg in messages:
        text = msg.get('text', '')
        sender = msg.get('sender', 'unknown')
        msg_time = msg.get('created_at', '')

        # Parse message timestamp
        try:
            msg_dt = datetime.fromisoformat(msg_time.replace('Z', '+00:00'))
            msg_ts = msg_dt.strftime('%H:%M:%S')
        except (ValueError, AttributeError):
            msg_ts = ""

        if sender == 'human':
            lines.append(f"**[{msg_ts}] User:** {text}\n")
        else:
            lines.append(f"**[{msg_ts}] {persona}:** {text}\n")

    return date_str, '\n'.join(lines)


def import_conversations(
    json_path: Path,
    persona: str = "Claude",
    output_root: Optional[Path] = None
) -> dict:
    """
    Import all conversations from Claude export.

    Returns dict of {date: num_conversations}
    """
    # Default output to project's docs/utety folder
    if output_root is None:
        script_dir = Path(__file__).parent
        output_root = script_dir.parent / "docs" / "utety"

    # Create persona folder
    persona_folder = persona.lower().replace(' ', '_')
    conv_dir = output_root / persona_folder / "conversations"
    conv_dir.mkdir(parents=True, exist_ok=True)

    # Parse export
    conversations = parse_claude_export(json_path)

    # Group by date
    by_date = {}
    for conv in conversations:
        date_str, markdown = format_conversation_to_markdown(conv, persona)
        if date_str not in by_date:
            by_date[date_str] = []
        by_date[date_str].append(markdown)

    # Write daily files
    stats = {}
    for date_str, convs in by_date.items():
        log_file = conv_dir / f"{date_str}.md"

        # Check if file exists (append mode)
        is_new = not log_file.exists()

        with open(log_file, 'a', encoding='utf-8') as f:
            if is_new:
                f.write(f"# {persona} Conversations - {date_str}\n")
                f.write(f"*Imported from Claude.ai export*\n")

            for conv_md in convs:
                f.write(conv_md)
                f.write("\n")

        stats[date_str] = len(convs)

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Import Claude.ai export into Die-Namic conversation format"
    )
    parser.add_argument(
        'json_file',
        type=Path,
        help="Path to conversations.json from Claude export"
    )
    parser.add_argument(
        '--persona', '-p',
        default='Claude',
        help="Persona name to attribute responses to (default: Claude)"
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        default=None,
        help="Output root directory (default: docs/utety/)"
    )

    args = parser.parse_args()

    if not args.json_file.exists():
        print(f"ERROR: File not found: {args.json_file}")
        return 1

    print(f"Importing from: {args.json_file}")
    print(f"Persona: {args.persona}")
    print(f"Output: {args.output or 'docs/utety/'}")
    print()

    try:
        stats = import_conversations(
            args.json_file,
            persona=args.persona,
            output_root=args.output
        )

        total = sum(stats.values())
        print(f"Imported {total} conversations across {len(stats)} days:")
        for date_str, count in sorted(stats.items()):
            print(f"  {date_str}: {count} conversations")

        print(f"\nConversations saved to: docs/utety/{args.persona.lower()}/conversations/")
        return 0

    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
