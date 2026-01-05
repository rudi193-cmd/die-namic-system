#!/bin/bash
# Cross-reference Verification Script
# Owner: Sean Campbell
# System: Aionic / Die-namic
# Version: 1.0
# Last Updated: 2026-01-05
# Checksum: ΔΣ=42

set -euo pipefail

GOVERNANCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$GOVERNANCE_DIR")"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================"
echo "Cross-Reference Verification"
echo "================================"
echo ""

ERRORS=0
WARNINGS=0

# Function to check if a file exists
check_file_ref() {
    local source_file="$1"
    local ref_path="$2"
    local line_context="$3"

    # Try relative to governance dir first
    if [[ -f "$GOVERNANCE_DIR/$ref_path" ]]; then
        echo -e "${GREEN}✓${NC} $source_file → $ref_path"
        return 0
    fi

    # Try relative to repo root
    if [[ -f "$REPO_ROOT/$ref_path" ]]; then
        echo -e "${GREEN}✓${NC} $source_file → $ref_path"
        return 0
    fi

    # Not found
    echo -e "${RED}✗${NC} $source_file → $ref_path (NOT FOUND)"
    echo "   Context: $line_context"
    ((ERRORS++))
    return 1
}

echo "Checking governance document cross-references..."
echo ""

# Check GOVERNANCE.md references
echo "Checking GOVERNANCE.md..."
check_file_ref "GOVERNANCE.md" "governance/gate.py" "gate.py reference"
check_file_ref "GOVERNANCE.md" "governance/GATEKEEPER_README.md" "GATEKEEPER_README reference"
check_file_ref "GOVERNANCE.md" "governance/CONTRIBUTOR_PROTOCOL.md" "CONTRIBUTOR_PROTOCOL reference"
check_file_ref "GOVERNANCE.md" "governance/NAMING_PROTOCOL.md" "NAMING_PROTOCOL reference"
check_file_ref "GOVERNANCE.md" "governance/BRIGGS.md" "BRIGGS reference"
check_file_ref "GOVERNANCE.md" "governance/CHARTER.md" "CHARTER reference"
check_file_ref "GOVERNANCE.md" "governance/DECISION_LOG.md" "DECISION_LOG reference"

echo ""

# Check AIONIC_BOOTSTRAP references
echo "Checking AIONIC_BOOTSTRAP_v1.2.md..."
check_file_ref "AIONIC_BOOTSTRAP_v1.2.md" "bridge_ring/HALT_LOG.md" "HALT_LOG reference"

echo ""

# Check AIONIC_CONTINUITY references
echo "Checking AIONIC_CONTINUITY_v5.1.md..."
check_file_ref "AIONIC_CONTINUITY_v5.1.md" "governance/gate.py" "gate.py reference"
check_file_ref "AIONIC_CONTINUITY_v5.1.md" "governance/THE_ELEVEN_PRINCIPLE.md" "ELEVEN_PRINCIPLE reference"
check_file_ref "AIONIC_CONTINUITY_v5.1.md" "governance/AUTONOMY_BENCHMARK.md" "AUTONOMY_BENCHMARK reference"
check_file_ref "AIONIC_CONTINUITY_v5.1.md" "governance/BRIGGS.md" "BRIGGS reference"
check_file_ref "AIONIC_CONTINUITY_v5.1.md" "governance/NAMING_PROTOCOL.md" "NAMING_PROTOCOL reference"

echo ""

# Check DUAL_COMMIT references
echo "Checking DUAL_COMMIT.md..."
check_file_ref "DUAL_COMMIT.md" "governance/api.py" "api.py reference"

echo ""

# Check RELATIONSHIP_TRACKING_PROTOCOL references
echo "Checking RELATIONSHIP_TRACKING_PROTOCOL.md..."
check_file_ref "RELATIONSHIP_TRACKING_PROTOCOL.md" "docs/journal/RELATIONSHIP_SCHEMA.md" "journal schema reference"

echo ""

# Check for broken internal links (markdown format)
# Note: Markdown link checking disabled - most links are relative or anchors
# Manual verification recommended for new documents
echo "Markdown link checking: skipped (manual verification recommended)"
echo ""

echo ""
echo "================================"
echo "Summary"
echo "================================"
echo -e "Errors:   ${RED}$ERRORS${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"

if [[ $ERRORS -eq 0 ]]; then
    echo -e "${GREEN}Cross-reference verification passed.${NC}"
    exit 0
else
    echo -e "${RED}Cross-reference verification failed.${NC}"
    exit 1
fi
