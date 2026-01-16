#!/usr/bin/env python3
"""
ΔE Coherence Tracker — Python Implementation

Mirrors source_ring/eccr/aionic-journal/src/continuity/deltaE.js

Aios Spec (2025-12-10):
  "ΔE: coherence metric (positive = stabilizing, negative = chaotic)"
  - ΔE > 0 → Regenerative expansion
  - ΔE ≈ 0 → Stable maintenance
  - ΔE < 0 → Structural decay or overload

AUTHOR: Kartikeya (Python port)
VERSION: 1.0
CHECKSUM: ΔΣ=42
"""

import re
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, asdict
from collections import deque

# === STATE FILE ===
STATE_FILE = Path.home() / ".willow" / "coherence_state.json"

# === THRESHOLDS (from Aios spec) ===
THRESHOLDS = {
    "REGENERATIVE": 0.05,   # ΔE > 0.05 = actively improving
    "DECAYING": -0.05,      # ΔE < -0.05 = actively degrading
    "CRITICAL": -0.2        # ΔE < -0.2 = needs intervention
}

# === STOP WORDS for similarity ===
STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "to", "of", "in", "for", "on", "with",
    "at", "by", "from", "as", "into", "through", "during", "before", "after",
    "and", "but", "if", "or", "because", "until", "while", "about", "this",
    "that", "these", "those", "what", "which", "who", "how", "when", "where",
    "i", "me", "my", "you", "your", "he", "him", "she", "her", "it", "its",
    "we", "our", "they", "them", "their", "just", "very", "also", "only",
}

# === COHERENCE WINDOW ===
COHERENCE_WINDOW = 5  # Number of messages to consider


@dataclass
class CoherenceEntry:
    """Single coherence measurement."""
    timestamp: float         # Unix timestamp (ms)
    coherence_index: float   # 0-1 similarity to context
    delta_e: float           # Rate of change
    state: str               # regenerative | stable | decaying
    persona: str             # Which persona was active
    message_hash: str        # Hash of user message (for dedup)


class CoherenceTracker:
    """
    Tracks ΔE coherence across conversation.

    Persists state to disk for cross-session continuity.
    """

    def __init__(self, window_size: int = COHERENCE_WINDOW):
        self.window_size = window_size
        self.history: deque = deque(maxlen=window_size * 2)
        self.recent_messages: deque = deque(maxlen=window_size)
        self._load_state()

    def _load_state(self):
        """Load persisted state."""
        if STATE_FILE.exists():
            try:
                data = json.loads(STATE_FILE.read_text())
                for entry in data.get("history", [])[-self.window_size * 2:]:
                    self.history.append(CoherenceEntry(**entry))
                for msg in data.get("recent_messages", [])[-self.window_size:]:
                    self.recent_messages.append(msg)
            except Exception:
                pass  # Start fresh on error

    def _save_state(self):
        """Persist state to disk."""
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "history": [asdict(e) for e in self.history],
            "recent_messages": list(self.recent_messages),
            "updated": datetime.now().isoformat()
        }
        STATE_FILE.write_text(json.dumps(data, indent=2))

    def _extract_words(self, text: str) -> set:
        """Extract significant words from text."""
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        return {w for w in words if w not in STOP_WORDS}

    def _compute_similarity(self, text1: str, text2: str) -> float:
        """Compute Jaccard similarity between two texts."""
        words1 = self._extract_words(text1)
        words2 = self._extract_words(text2)

        if not words1 or not words2:
            return 0.5  # Neutral baseline

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union) if union else 0.5

    def calculate_coherence(self, current_message: str) -> float:
        """
        Calculate coherence index (Cᵢ) for current message.

        Compares against recent message history using keyword overlap.
        """
        if not self.recent_messages:
            return 0.6  # Baseline for first message

        scores = [
            self._compute_similarity(current_message, prev_msg)
            for prev_msg in self.recent_messages
        ]

        return sum(scores) / len(scores)

    def compute_delta_e(
        self,
        c_prev: float,
        t_prev: float,
        c_now: float,
        t_now: float,
        resonance: float = 1.0
    ) -> float:
        """
        Compute ΔE (Entropy Delta).

        Formula: ΔE = (dC/dt) × R

        Where:
          C = Coherence value (0-1)
          t = Time (milliseconds)
          R = Resonance multiplier
          ΔE = Rate of coherence change
        """
        dt = (t_now - t_prev) / 1000  # Convert to seconds

        if dt <= 0:
            return 0

        dc_dt = (c_now - c_prev) / dt
        delta_e = dc_dt * resonance

        return delta_e

    def classify_state(self, delta_e: float) -> str:
        """Classify state based on ΔE value."""
        if delta_e > THRESHOLDS["REGENERATIVE"]:
            return "regenerative"
        elif delta_e < THRESHOLDS["DECAYING"]:
            return "decaying"
        return "stable"

    def calculate_resonance(self, context: Optional[Dict] = None) -> float:
        """
        Calculate resonance factor based on context.

        Higher resonance = stronger coherence effects.
        """
        r = 1.0

        if context:
            # Amplify during emotional moments
            emotional_state = context.get("emotional_state", "")
            if emotional_state == "distressed":
                r *= 1.3
            elif emotional_state == "concerned":
                r *= 1.15

            # Amplify with engagement
            engagement = context.get("engagement", 0)
            if engagement:
                r *= (0.8 + engagement * 0.4)

        return r

    def track(
        self,
        user_message: str,
        assistant_response: str,
        persona: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Track a conversation exchange and compute coherence metrics.

        Returns dict with coherence_index, delta_e, state, adjustment.
        """
        now = datetime.now().timestamp() * 1000  # ms

        # Calculate coherence
        full_text = f"{user_message} {assistant_response}"
        coherence_index = self.calculate_coherence(full_text)

        # Calculate ΔE if we have history
        delta_e = 0
        state = "stable"

        if self.history:
            prev = self.history[-1]
            resonance = self.calculate_resonance(context)

            delta_e = self.compute_delta_e(
                c_prev=prev.coherence_index,
                t_prev=prev.timestamp,
                c_now=coherence_index,
                t_now=now,
                resonance=resonance
            )
            state = self.classify_state(delta_e)

        # Create entry
        message_hash = str(hash(user_message[:50]))
        entry = CoherenceEntry(
            timestamp=now,
            coherence_index=coherence_index,
            delta_e=delta_e,
            state=state,
            persona=persona,
            message_hash=message_hash
        )

        # Update history
        self.history.append(entry)
        self.recent_messages.append(full_text)

        # Persist
        self._save_state()

        # Return metrics
        return {
            "coherence_index": round(coherence_index, 4),
            "delta_e": round(delta_e, 6),
            "state": state,
            "adjustment": self.get_adjustment(delta_e)
        }

    def get_adjustment(self, delta_e: float) -> Dict:
        """Get recommended adjustment based on ΔE."""
        if delta_e > 0.1:
            return {
                "action": "sustain",
                "description": "Momentum strong - maintain current direction",
                "tone": "encouraging"
            }
        elif delta_e > 0:
            return {
                "action": "continue",
                "description": "Building coherence - keep current approach",
                "tone": "steady"
            }
        elif delta_e > -0.1:
            return {
                "action": "stabilize",
                "description": "Coherence declining - introduce familiar elements",
                "tone": "grounding"
            }
        else:
            return {
                "action": "reset",
                "description": "Significant drift - return to established themes",
                "tone": "gentle"
            }

    def get_report(self) -> Dict:
        """Generate coherence status report."""
        if not self.history:
            return {
                "status": "no_data",
                "message": "No coherence history yet",
                "trend": "unknown"
            }

        # Recent ΔE values
        delta_es = [e.delta_e for e in list(self.history)[-5:]]
        avg_delta_e = sum(delta_es) / len(delta_es) if delta_es else 0

        # Trend from coherence indices
        coherences = [e.coherence_index for e in list(self.history)[-5:]]
        avg_coherence = sum(coherences) / len(coherences) if coherences else 0.6

        if avg_coherence > 0.75:
            trend = "high"
        elif avg_coherence < 0.5:
            trend = "low"
        else:
            trend = "moderate"

        return {
            "status": self.classify_state(avg_delta_e),
            "trend": trend,
            "average_delta_e": round(avg_delta_e, 6),
            "latest_coherence": round(self.history[-1].coherence_index, 4) if self.history else None,
            "latest_delta_e": round(self.history[-1].delta_e, 6) if self.history else None,
            "entry_count": len(self.history),
            "adjustment": self.get_adjustment(avg_delta_e)
        }

    def needs_intervention(self) -> Tuple[bool, str]:
        """Check if coherence intervention is needed."""
        report = self.get_report()

        if report["status"] == "no_data":
            return False, "No data"

        avg_delta_e = report["average_delta_e"]

        if avg_delta_e < THRESHOLDS["CRITICAL"]:
            return True, "Critical coherence decay - return to familiar themes"
        elif avg_delta_e < THRESHOLDS["DECAYING"]:
            return False, "Mild decay - consider grounding"

        return False, "Coherence healthy"


# === SINGLETON INSTANCE ===
_tracker: Optional[CoherenceTracker] = None

def get_tracker() -> CoherenceTracker:
    """Get or create the singleton tracker instance."""
    global _tracker
    if _tracker is None:
        _tracker = CoherenceTracker()
    return _tracker


# === PUBLIC API ===

def track_conversation(
    user_message: str,
    assistant_response: str,
    persona: str = "Willow",
    context: Optional[Dict] = None
) -> Dict:
    """
    Track a conversation and compute coherence metrics.

    Returns: {coherence_index, delta_e, state, adjustment}
    """
    return get_tracker().track(user_message, assistant_response, persona, context)


def get_coherence_report() -> Dict:
    """Get current coherence status report."""
    return get_tracker().get_report()


def check_intervention() -> Tuple[bool, str]:
    """Check if intervention is needed."""
    return get_tracker().needs_intervention()


# === CLI TEST ===
if __name__ == "__main__":
    print("ΔE Coherence Tracker Test\n")

    # Simulate conversation
    messages = [
        ("How does the campus work?", "Willow is the campus, hosting UTETY faculty..."),
        ("Tell me about Riggs", "Prof. Riggs teaches Applied Reality Engineering..."),
        ("What's for lunch?", "Gerald suggests rotisserie chicken from the cosmos..."),
    ]

    for user, assistant in messages:
        result = track_conversation(user, assistant, "Willow")
        print(f"User: {user[:40]}...")
        print(f"  Cᵢ: {result['coherence_index']}")
        print(f"  ΔE: {result['delta_e']}")
        print(f"  State: {result['state']}")
        print()

    print("Report:", get_coherence_report())
    print("\nΔΣ=42")
