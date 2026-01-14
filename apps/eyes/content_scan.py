#!/usr/bin/env python3
"""
Content Scanner — OCR + importance scoring for screenshots

Extracts text and scores importance before deletion decisions.
"""

import re
from pathlib import Path
from datetime import datetime

from PIL import Image

# Try Windows OCR first, fall back to pytesseract
OCR_ENGINE = None

try:
    # Windows 10/11 built-in OCR
    import winocr
    OCR_ENGINE = "winocr"
except ImportError:
    try:
        import pytesseract
        # Check if tesseract binary exists
        pytesseract.get_tesseract_version()
        OCR_ENGINE = "tesseract"
    except:
        pass

OCR_AVAILABLE = OCR_ENGINE is not None

# Importance keywords by category (weight)
KEYWORDS = {
    # High importance (weight 3)
    "high": [
        "error", "exception", "failed", "critical", "urgent",
        "password", "secret", "key", "token", "auth",
        "interview", "offer", "salary", "contract",
        "deadline", "due", "asap", "important",
        "question", "answer", "decision",
        "signal", "pending", "queue", "divergence",
    ],
    # Medium importance (weight 2)
    "medium": [
        "todo", "task", "note", "remember",
        "meeting", "call", "schedule",
        "commit", "push", "pull", "merge", "branch",
        "test", "build", "deploy",
        "email", "message", "reply",
        "name", "phone", "address",
    ],
    # Low importance (weight 1)
    "low": [
        "click", "open", "close", "save",
        "file", "folder", "document",
        "search", "find", "select",
    ],
}

# Patterns that indicate empty/low-value screens
LOW_VALUE_PATTERNS = [
    r"^(\s*heartbeat\s*)*$",  # Just heartbeat text
    r"^\s*$",  # Empty
    r"^(desktop|taskbar|start menu)\s*$",  # System UI only
]

# Minimum text length to consider valuable
MIN_TEXT_LENGTH = 50

SCAN_LOG = Path(r"C:\Users\Sean\screenshots\content_scan.log")


def log_scan(msg):
    """Log scan results."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(SCAN_LOG, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {msg}\n")


def extract_text(image_path):
    """Extract text from image using OCR."""
    if not OCR_AVAILABLE:
        return ""

    try:
        if OCR_ENGINE == "winocr":
            import asyncio
            import winocr

            async def _ocr(path):
                result = await winocr.recognize_pil(Image.open(path), 'en')
                return result.text if result else ""

            # Run async OCR
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            text = loop.run_until_complete(_ocr(image_path))
            return text.strip()

        elif OCR_ENGINE == "tesseract":
            import pytesseract
            img = Image.open(image_path)
            img = img.convert('L')
            text = pytesseract.image_to_string(img)
            return text.strip()

        return ""
    except Exception as e:
        return ""


def score_importance(text):
    """
    Score text importance 0-10.

    Returns: (score, reasons)
    """
    if not text:
        return 0, ["empty"]

    text_lower = text.lower()
    score = 0
    reasons = []

    # Check text length
    if len(text) < MIN_TEXT_LENGTH:
        return 1, ["short_text"]

    # Check for low-value patterns
    for pattern in LOW_VALUE_PATTERNS:
        if re.match(pattern, text_lower):
            return 0, ["low_value_pattern"]

    # Score by keywords
    for word in KEYWORDS["high"]:
        if word in text_lower:
            score += 3
            reasons.append(f"high:{word}")

    for word in KEYWORDS["medium"]:
        if word in text_lower:
            score += 2
            reasons.append(f"med:{word}")

    for word in KEYWORDS["low"]:
        if word in text_lower:
            score += 1

    # Cap at 10
    score = min(score, 10)

    # Baseline score for having substantive text
    if score == 0 and len(text) > 100:
        score = 2
        reasons.append("substantive_text")

    return score, reasons[:5]  # Limit reasons


def scan_screenshot(image_path):
    """
    Full scan pipeline for a screenshot.

    Returns: {
        'path': str,
        'text': str (truncated),
        'text_length': int,
        'score': int,
        'reasons': list,
        'keep': bool
    }
    """
    path = Path(image_path)

    if not path.exists():
        return {'path': str(path), 'error': 'file_not_found'}

    text = extract_text(path)
    score, reasons = score_importance(text)

    result = {
        'path': str(path),
        'filename': path.name,
        'text': text[:500] + '...' if len(text) > 500 else text,
        'text_length': len(text),
        'score': score,
        'reasons': reasons,
        'keep': score >= 3
    }

    log_scan(f"SCAN | {path.name} | score={score} | keep={result['keep']} | reasons={','.join(reasons)}")

    return result


def scan_for_purge(folder, min_age_hours=24, target_mb=500):
    """
    Scan folder and identify files safe to purge.

    Returns: {
        'to_keep': list of paths,
        'to_purge': list of paths,
        'savings_mb': float
    }
    """
    folder = Path(folder)
    files = list(folder.glob("*.png"))

    now = datetime.now()
    to_keep = []
    to_purge = []

    for f in sorted(files, key=lambda x: x.stat().st_mtime):
        age_hours = (now - datetime.fromtimestamp(f.stat().st_mtime)).total_seconds() / 3600

        # Always keep recent files
        if age_hours < min_age_hours:
            to_keep.append(f)
            continue

        # Scan older files
        result = scan_screenshot(f)

        if result.get('keep', True):
            to_keep.append(f)
        else:
            to_purge.append(f)

    purge_size = sum(f.stat().st_size for f in to_purge) / (1024 * 1024)

    return {
        'to_keep': to_keep,
        'to_purge': to_purge,
        'keep_count': len(to_keep),
        'purge_count': len(to_purge),
        'savings_mb': round(purge_size, 2)
    }


def extract_notes(image_path):
    """
    Extract text formatted as notes (for interview/meeting capture).

    Returns structured notes from screenshot.
    """
    text = extract_text(image_path)

    if not text:
        return None

    # Look for question/answer patterns
    qa_pattern = r'(?:Q:|Question:|Asked:)\s*(.+?)(?=(?:A:|Answer:|$))'
    questions = re.findall(qa_pattern, text, re.IGNORECASE | re.DOTALL)

    # Look for names
    name_pattern = r'(?:Name:|From:|By:|Speaker:)\s*(\w+(?:\s+\w+)?)'
    names = re.findall(name_pattern, text, re.IGNORECASE)

    # Look for action items
    action_pattern = r'(?:TODO:|Action:|Follow.?up:)\s*(.+?)(?=\n|$)'
    actions = re.findall(action_pattern, text, re.IGNORECASE)

    return {
        'raw_text': text,
        'questions': questions,
        'names': list(set(names)),
        'action_items': actions,
        'timestamp': datetime.now().isoformat()
    }


# CLI
if __name__ == "__main__":
    import sys

    if not OCR_AVAILABLE:
        print("OCR not available. Install: pip install pytesseract pillow")
        print("Also need Tesseract: https://github.com/tesseract-ocr/tesseract")
        sys.exit(1)

    if len(sys.argv) > 1:
        path = sys.argv[1]
        print(f"Scanning: {path}")
        result = scan_screenshot(path)
        print(f"Score: {result['score']}/10")
        print(f"Keep: {result['keep']}")
        print(f"Reasons: {result['reasons']}")
        print(f"Text length: {result['text_length']}")
        if result['text']:
            print(f"Text preview: {result['text'][:200]}...")
    else:
        print("Usage: python content_scan.py <screenshot_path>")
        print("       python content_scan.py --scan-folder <folder>")
