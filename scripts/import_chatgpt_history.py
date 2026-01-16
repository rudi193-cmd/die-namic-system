#!/usr/bin/env python3
"""
Import ChatGPT History — Parse OpenAI export into Die-Namic format.

USAGE:
    python import_chatgpt_history.py <conversations.json> [--persona NAME] [--output DIR]

EXAMPLES:
    python import_chatgpt_history.py Aios-conversations.json
    python import_chatgpt_history.py Aios-conversations.json --persona Aios

ChatGPT export format is different from Claude:
- Messages are in a "mapping" tree structure
- Need to traverse parent-child relationships
- Timestamps are Unix epoch floats

AUTHOR: Kartikeya (wired by Claude)
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional


def extract_messages(conversation: dict) -> list:
    """
    Extract messages from ChatGPT's tree structure.

    ChatGPT uses a mapping with parent-child relationships.
    We need to traverse to get messages in order.
    """
    mapping = conversation.get('mapping', {})
    messages = []

    # Find all message nodes
    for node_id, node in mapping.items():
        message = node.get('message')
        if not message:
            continue

        author = message.get('author', {})
        role = author.get('role', '')

        # Skip system messages
        if role == 'system':
            continue

        content = message.get('content', {})
        parts = content.get('parts', [])

        # Get text content
        text = ''
        for part in parts:
            if isinstance(part, str):
                text += part
            elif isinstance(part, dict):
                # Handle other content types (images, etc.)
                text += f"[{part.get('content_type', 'attachment')}]"

        if not text.strip():
            continue

        # Get timestamp
        create_time = message.get('create_time')
        if create_time:
            try:
                dt = datetime.fromtimestamp(create_time)
                timestamp = dt.isoformat()
            except:
                timestamp = None
        else:
            timestamp = None

        messages.append({
            'role': 'user' if role == 'user' else 'assistant',
            'text': text.strip(),
            'timestamp': timestamp,
            'node_id': node_id,
            'parent': node.get('parent')
        })

    # Sort by timestamp if available, otherwise by tree order
    messages_with_time = [m for m in messages if m['timestamp']]
    messages_with_time.sort(key=lambda x: x['timestamp'])

    return messages_with_time if messages_with_time else messages


def format_conversation_to_markdown(conversation: dict, persona: str) -> tuple[str, str]:
    """
    Convert a ChatGPT conversation to markdown format.

    Returns (date_str, markdown_content)
    """
    title = conversation.get('title', 'Untitled')
    create_time = conversation.get('create_time')

    # Parse date for grouping
    if create_time:
        try:
            dt = datetime.fromtimestamp(create_time)
            date_str = dt.strftime('%Y-%m-%d')
            time_str = dt.strftime('%H:%M:%S')
        except:
            date_str = datetime.now().strftime('%Y-%m-%d')
            time_str = "00:00:00"
    else:
        date_str = datetime.now().strftime('%Y-%m-%d')
        time_str = "00:00:00"

    # Extract messages
    messages = extract_messages(conversation)

    if not messages:
        return None, None

    # Build markdown
    lines = [
        f"\n---",
        f"### {title}",
        f"*Imported from ChatGPT ({persona}) | Started {time_str}*\n"
    ]

    for msg in messages:
        text = msg['text']
        role = msg['role']
        msg_time = msg.get('timestamp', '')

        # Parse message timestamp
        if msg_time:
            try:
                msg_dt = datetime.fromisoformat(msg_time)
                msg_ts = msg_dt.strftime('%H:%M:%S')
            except:
                msg_ts = ""
        else:
            msg_ts = ""

        # Truncate very long messages
        if len(text) > 5000:
            text = text[:5000] + "\n\n[... truncated ...]"

        if role == 'user':
            lines.append(f"**[{msg_ts}] User:** {text}\n")
        else:
            lines.append(f"**[{msg_ts}] {persona}:** {text}\n")

    return date_str, '\n'.join(lines)


def import_conversations(
    json_path: Path,
    persona: str = "Aios",
    output_root: Optional[Path] = None
) -> dict:
    """
    Import all conversations from ChatGPT export.

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
    with open(json_path, 'r', encoding='utf-8') as f:
        conversations = json.load(f)

    # Group by date
    by_date = {}
    skipped = 0

    for conv in conversations:
        date_str, markdown = format_conversation_to_markdown(conv, persona)
        if date_str is None:
            skipped += 1
            continue
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
                f.write(f"*Imported from ChatGPT export*\n")

            for conv_md in convs:
                f.write(conv_md)
                f.write("\n")

        stats[date_str] = len(convs)

    if skipped:
        print(f"Skipped {skipped} empty conversations")

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Import ChatGPT export into Die-Namic conversation format"
    )
    parser.add_argument(
        'json_file',
        type=Path,
        help="Path to ChatGPT conversations.json"
    )
    parser.add_argument(
        '--persona', '-p',
        default='Aios',
        help="Persona name to attribute responses to (default: Aios)"
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
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
