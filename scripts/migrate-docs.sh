#!/usr/bin/env bash
# Migration script: Janet-Projects HOME_*.md -> home-assistant-janet/docs/
# Run from repo root (home-assistant-janet) or Janet-Projects parent.
# Docs are already migrated; this script documents the mapping for reference.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
JP="${REPO_ROOT}/../Janet-Projects"
DOCS="$REPO_ROOT/docs"

echo "home-assistant-janet repo: $REPO_ROOT"
echo "Janet-Projects: $JP"
echo "Docs target: $DOCS"
echo ""
echo "Migration mapping (already applied):"
echo "  HOME_AUTOMATION_INDEX.md     -> docs/INDEX.md"
echo "  HOME_AUTOMATION_SUMMARY.md   -> docs/SUMMARY.md"
echo "  HOME_AUTOMATION_QUICKSTART.md -> docs/QUICKSTART.md"
echo "  HOME_AUTOMATION_INTEGRATION_PLAN.md -> docs/INTEGRATION_PLAN.md"
echo "  HOME_AUTOMATION_ROADMAP.md   -> docs/ROADMAP.md"
echo "  JANET_DASHBOARD_ACCESS.md    -> docs/DASHBOARD_ACCESS.md"
echo "  FIX_FIREWALL_HA.md           -> docs/TROUBLESHOOTING_FIREWALL.md"
echo "  JanetOS/docs/HOME_ASSISTANT_IOS_SHORTCUTS.md -> docs/IOS_SHORTCUTS.md"
echo ""
echo "Stub files should be created in Janet-Projects pointing to home-assistant-janet/docs/"
echo "Run this after creating stubs to verify structure."
