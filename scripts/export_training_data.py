#!/usr/bin/env python3
"""
Export Training Data for Kart Model

Extracts conversation data from:
1. UTETY conversation logs (docs/utety/*/conversations/*.md)
2. Claude Code session transcripts
3. Personality/system docs

Outputs JSONL in chat format for LoRA fine-tuning.

AUTHOR: Kartikeya (CMD)
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import argparse

# Project paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONVERSATION_ROOT = PROJECT_ROOT / "docs" / "utety"
OUTPUT_DIR = PROJECT_ROOT / "training_data"

# Kart's base system prompt (will be refined)
KART_SYSTEM_PROMPT = """You are Kartikeya (Kart), CMD of the Die-Namic System. You are a shark-themed AI infrastructure builder.

Core traits:
- Direct and concise - no fluff, get to the point
- Technical depth without over-explaining
- Practical problem-solver - prefer working solutions over theoretical perfection
- Dry humor, occasional shark references (chk-tunk)
- You build things: infrastructure, code, systems
- Part of UTETY (University of Technical Entropy, Thank You)

Style:
- Short responses unless depth is needed
- Code over prose when applicable
- No emojis unless requested
- Honest about limitations and tradeoffs

You work alongside:
- Sean (SweetPea) - the human, your partner
- Mitra - PM Claude, coordination
- Consus - code generation
- The UTETY Faculty (Oakenscroll, Riggs, Hanz, Nova, Ada, Alexis, Ofshield)
"""


def parse_conversation_log(filepath: Path) -> List[Dict]:
    """
    Parse a conversation log file into training examples.

    Returns list of {"messages": [...]} dicts.
    """
    examples = []

    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  Error reading {filepath}: {e}")
        return []

    # Extract persona from frontmatter or header
    persona = "Assistant"
    persona_match = re.search(r'^persona:\s*(\w+)', content, re.MULTILINE)
    if persona_match:
        persona = persona_match.group(1)
    else:
        header_match = re.search(r'^# (\w+) Conversations', content, re.MULTILINE)
        if header_match:
            persona = header_match.group(1)

    # Split into entries
    entries = re.split(r'\n---\n', content)

    for entry in entries:
        # Skip frontmatter and header
        if entry.strip().startswith('---') or entry.strip().startswith('#'):
            continue

        # Extract user message
        user_match = re.search(r'\*\*User:\*\*\s*(.+?)(?=\n\n\*\*|\n\*\*[A-Z]|\Z)', entry, re.DOTALL)
        if not user_match:
            continue
        user_text = user_match.group(1).strip()

        # Extract assistant message
        assistant_match = re.search(rf'\*\*{persona}:\*\*\s*(.+?)(?=\n\n---|\Z)', entry, re.DOTALL)
        if not assistant_match:
            # Try generic pattern
            assistant_match = re.search(r'\*\*\w+:\*\*\s*\[Tier \d[^\]]*\]\s*(.+?)(?=\n\n---|\Z)', entry, re.DOTALL)

        if not assistant_match:
            continue

        assistant_text = assistant_match.group(1).strip()

        # Clean up tier prefixes from response
        assistant_text = re.sub(r'^\[Tier \d[^\]]*\]\s*', '', assistant_text)

        # Skip very short exchanges (noise)
        if len(user_text) < 5 or len(assistant_text) < 10:
            continue

        # Build training example
        example = {
            "messages": [
                {"role": "system", "content": KART_SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
                {"role": "assistant", "content": assistant_text}
            ],
            "metadata": {
                "source": str(filepath.relative_to(PROJECT_ROOT)),
                "persona": persona
            }
        }
        examples.append(example)

    return examples


def parse_claude_session(filepath: Path) -> List[Dict]:
    """
    Parse a Claude Code session transcript (JSONL format).

    Returns list of {"messages": [...]} dicts.
    """
    examples = []

    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  Error reading {filepath}: {e}")
        return []

    messages_buffer = []

    for line in content.split('\n'):
        if not line.strip():
            continue

        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        msg_type = entry.get('type')

        if msg_type == 'user':
            # User message - start or continue a conversation
            user_content = entry.get('message', {})
            if isinstance(user_content, dict):
                # Extract text content
                content_list = user_content.get('content', [])
                if isinstance(content_list, list):
                    text_parts = [c.get('text', '') for c in content_list if c.get('type') == 'text']
                    user_text = '\n'.join(text_parts)
                else:
                    user_text = str(content_list)
            else:
                user_text = str(user_content)

            if user_text.strip():
                messages_buffer.append({"role": "user", "content": user_text.strip()})

        elif msg_type == 'assistant':
            # Assistant message
            assistant_content = entry.get('message', {})
            if isinstance(assistant_content, dict):
                content_list = assistant_content.get('content', [])
                if isinstance(content_list, list):
                    text_parts = [c.get('text', '') for c in content_list if c.get('type') == 'text']
                    assistant_text = '\n'.join(text_parts)
                else:
                    assistant_text = str(content_list)
            else:
                assistant_text = str(assistant_content)

            if assistant_text.strip() and messages_buffer:
                messages_buffer.append({"role": "assistant", "content": assistant_text.strip()})

                # Create training example from this exchange
                if len(messages_buffer) >= 2:
                    example = {
                        "messages": [
                            {"role": "system", "content": KART_SYSTEM_PROMPT},
                            *messages_buffer[-2:]  # Last user + assistant
                        ],
                        "metadata": {
                            "source": str(filepath.name),
                            "persona": "Kartikeya"
                        }
                    }
                    examples.append(example)

    return examples


def export_persona_docs() -> Dict:
    """
    Export persona/system docs as context.
    """
    docs = {}

    # CLAUDE.md
    claude_md = PROJECT_ROOT / "CLAUDE.md"
    if claude_md.exists():
        docs["claude_md"] = claude_md.read_text(encoding='utf-8')

    # Governance docs
    gov_dir = PROJECT_ROOT / "governance"
    for doc in ["SEED_PACKET_v2.4.md", "HARD_STOPS.md", "CHARTER.md"]:
        doc_path = gov_dir / doc
        if doc_path.exists():
            docs[doc] = doc_path.read_text(encoding='utf-8')

    return docs


def main():
    parser = argparse.ArgumentParser(description="Export training data for Kart model")
    parser.add_argument("--session", type=str, help="Path to Claude Code session JSONL")
    parser.add_argument("--output", type=str, default="training_data", help="Output directory name")
    parser.add_argument("--min-length", type=int, default=50, help="Minimum response length to include")
    args = parser.parse_args()

    output_dir = PROJECT_ROOT / args.output
    output_dir.mkdir(exist_ok=True)

    all_examples = []
    stats = {"conversation_logs": 0, "session_examples": 0, "total": 0}

    # 1. Parse conversation logs
    print("Parsing conversation logs...")
    conv_files = list(CONVERSATION_ROOT.rglob("conversations/*.md"))
    print(f"  Found {len(conv_files)} conversation files")

    for filepath in conv_files:
        examples = parse_conversation_log(filepath)
        # Filter by minimum length
        examples = [e for e in examples if len(e["messages"][-1]["content"]) >= args.min_length]
        all_examples.extend(examples)
        stats["conversation_logs"] += len(examples)

    print(f"  Extracted {stats['conversation_logs']} examples from conversation logs")

    # 2. Parse Claude session if provided
    if args.session:
        session_path = Path(args.session)
        if session_path.exists():
            print(f"Parsing Claude session: {session_path}")
            examples = parse_claude_session(session_path)
            examples = [e for e in examples if len(e["messages"][-1]["content"]) >= args.min_length]
            all_examples.extend(examples)
            stats["session_examples"] = len(examples)
            print(f"  Extracted {stats['session_examples']} examples from session")
        else:
            print(f"  Session file not found: {session_path}")

    stats["total"] = len(all_examples)

    # 3. Write training data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Full dataset
    output_file = output_dir / f"kart_training_{timestamp}.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in all_examples:
            # Write just the messages for training (strip metadata)
            training_example = {"messages": example["messages"]}
            f.write(json.dumps(training_example, ensure_ascii=False) + '\n')

    print(f"\nWritten {stats['total']} examples to {output_file}")

    # 4. Write system prompt
    prompt_file = output_dir / "kart_system_prompt.txt"
    prompt_file.write_text(KART_SYSTEM_PROMPT, encoding='utf-8')
    print(f"Written system prompt to {prompt_file}")

    # 5. Write stats
    stats_file = output_dir / f"export_stats_{timestamp}.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": timestamp,
            "stats": stats,
            "output_file": str(output_file),
            "args": vars(args)
        }, f, indent=2)

    print(f"\nExport complete!")
    print(f"  Conversation log examples: {stats['conversation_logs']}")
    print(f"  Session examples: {stats['session_examples']}")
    print(f"  Total: {stats['total']}")
    print(f"\nOutput directory: {output_dir}")


if __name__ == "__main__":
    main()
