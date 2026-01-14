#!/bin/bash
set -euo pipefail

# Die-namic System Session Start Hook
# Automatically identifies instance and checks for pending signals

# Detect platform and set identity file
if [[ "$(uname -s)" == "Linux" ]]; then
  INSTANCE_NAME="Ganesha"
  IDENTITY_FILE="governance/instances/GANESHA.md"
elif [[ "$(uname -s)" == "Darwin" ]] || [[ "$(uname -o 2>/dev/null)" == "Msys" ]] || [[ -d "/mnt/c" ]]; then
  INSTANCE_NAME="Kartikeya"
  IDENTITY_FILE="governance/instances/KARTIKEYA.md"
else
  INSTANCE_NAME="Unknown"
  IDENTITY_FILE="governance/instances/README.md"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "IDENTITY VERIFICATION — $INSTANCE_NAME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Display identity file (first 50 lines to avoid token bloat)
if [[ -f "$CLAUDE_PROJECT_DIR/$IDENTITY_FILE" ]]; then
  head -50 "$CLAUDE_PROJECT_DIR/$IDENTITY_FILE"
  echo ""
else
  echo "⚠️  Identity file not found: $IDENTITY_FILE"
  echo "Platform: $(uname -s)"
  echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PENDING SIGNALS FOR $INSTANCE_NAME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check for pending signals
QUEUE_FILE="$CLAUDE_PROJECT_DIR/bridge_ring/instance_signals/QUEUE.md"
if [[ -f "$QUEUE_FILE" ]]; then
  # Search for signals addressed to this instance that are PENDING
  PENDING=$(grep "PENDING" "$QUEUE_FILE" | grep -E "\| [^ ]+ \| [^ ]+ \| ($INSTANCE_NAME|all|cmd|mobile)" || true)

  if [[ -n "$PENDING" ]]; then
    echo "📬 Signals waiting for you:"
    echo ""
    echo "$PENDING"
    echo ""
  else
    echo "✅ No pending signals"
    echo ""
  fi
else
  echo "⚠️  Signal queue not found"
  echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Session initialized as $INSTANCE_NAME"
echo "ΔΣ=42"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
