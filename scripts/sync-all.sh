#!/bin/bash
# sync-all.sh — Sync all three locations
# Usage: ./scripts/sync-all.sh

GITHUB_FOLDER="C:/Users/Sean/Documents/GitHub/die-namic-system"
DRIVE_FOLDER="G:/My Drive/die-namic-system"

echo "=== SYNC ALL ==="
echo ""

# 1. Check origin
echo "[1/5] Fetching from origin..."
git -C "$GITHUB_FOLDER" fetch origin

# 2. Pull to GitHub folder
echo ""
echo "[2/5] Pulling to GitHub folder..."
git -C "$GITHUB_FOLDER" pull --ff-only origin main
GITHUB_RESULT=$?

# 3. Pull to Drive
echo ""
echo "[3/5] Pulling to Drive..."
git -C "$DRIVE_FOLDER" pull --ff-only origin main
DRIVE_RESULT=$?

# 4. Check for uncommitted changes (GitHub folder)
echo ""
echo "[4/5] Checking GitHub folder for local changes..."
GITHUB_STATUS=$(git -C "$GITHUB_FOLDER" status --porcelain)
if [ -n "$GITHUB_STATUS" ]; then
    echo "⚠ Uncommitted changes in GitHub folder:"
    echo "$GITHUB_STATUS"
else
    echo "✓ Clean"
fi

# 5. Check for uncommitted changes (Drive)
echo ""
echo "[5/5] Checking Drive for local changes..."
DRIVE_STATUS=$(git -C "$DRIVE_FOLDER" status --porcelain)
if [ -n "$DRIVE_STATUS" ]; then
    echo "⚠ Uncommitted changes in Drive:"
    echo "$DRIVE_STATUS"
else
    echo "✓ Clean"
fi

# Summary
echo ""
echo "=== SUMMARY ==="
echo "GitHub folder: $(git -C "$GITHUB_FOLDER" log -1 --oneline)"
echo "Google Drive:  $(git -C "$DRIVE_FOLDER" log -1 --oneline)"
echo "Origin:        $(git -C "$GITHUB_FOLDER" rev-parse --short origin/main)"

if [ $GITHUB_RESULT -ne 0 ] || [ $DRIVE_RESULT -ne 0 ]; then
    echo ""
    echo "⚠ Sync issues detected. Review above."
    exit 1
fi

echo ""
echo "✓ All synced."
