# Janet Home Automation Documentation Migration

**Date:** 2026-03-10  
**To:** Janet ecosystem stakeholders, contributors  
**From:** Lynda (Business)

---

## Summary

All Janet Home Automation documentation has been consolidated into the **home-assistant-janet** repository.

---

## What Changed

### Moved
- `HOME_AUTOMATION_*.md` → `home-assistant-janet/docs/`
- `HOME_ASSISTANT_*.md` content → merged into `docs/`
- `JANET_DASHBOARD_ACCESS.md` → `docs/DASHBOARD_ACCESS.md`
- `FIX_FIREWALL_HA.md` → `docs/TROUBLESHOOTING_FIREWALL.md`
- JanetOS `HOME_ASSISTANT_IOS_SHORTCUTS.md` → `docs/IOS_SHORTCUTS.md`

### New
- `docs/INDEX.md` — single entry point
- `docs/ONBOARDING.md` — new user flow
- `docs/BUSINESS_CASE.md` — consolidation rationale
- `docs/persona/HABITAT.md` — Habitat persona for agents
- `scripts/verify-ha-connection.sh` — HA connection test

### Deprecation
- Old paths in `Janet-Projects/` now contain stubs pointing to `home-assistant-janet/docs/`

---

## Timeline

| Week | Action |
|------|--------|
| 1 | Docs migration complete; stubs in Janet-Projects |
| 2 | Habitat persona registered; workspace references updated |
| Ongoing | Update any external links to new paths |

---

## For Contributors

**New doc path:** `https://github.com/MzxzD/home-assistant-janet/tree/main/docs`  
**Entry point:** [docs/INDEX.md](INDEX.md)

Please update bookmarks and internal links to the new locations.

---

## Questions

Open an issue in the home-assistant-janet repository or contact the Janet ecosystem maintainers.
