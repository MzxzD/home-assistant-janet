# Home Automation Integration - Documentation Index

**Complete guide to Home Assistant integration in Janet ecosystem**

---

## Quick Navigation

### Getting Started
- **[Summary](SUMMARY.md)** - Executive overview (5 min read)
- **[Quick Start](QUICKSTART.md)** - Get running in 30 minutes
- **[Roadmap](ROADMAP.md)** - Visual timeline and milestones
- **[Onboarding](ONBOARDING.md)** - New user flow

### Implementation
- **[Integration Plan](INTEGRATION_PLAN.md)** - Complete technical plan
- **[iOS Documentation](IOS_SHORTCUTS.md)** - iOS-specific features

### Reference
- **[Dashboard Access](DASHBOARD_ACCESS.md)** - Janet opens HA in browser
- **[Troubleshooting Firewall](TROUBLESHOOTING_FIREWALL.md)** - Port 8123 blocked
- **[Acceptance Criteria](../JanetOS/docs/ACCEPTANCE_CRITERIA.md)** - AC-HA1 through AC-HA4 (in JanetOS)

---

## By Role

### For Project Managers
1. Read: [Summary](SUMMARY.md)
2. Review: [Roadmap](ROADMAP.md)
3. Track: Progress in roadmap document

### For Developers
1. Read: [Quick Start](QUICKSTART.md)
2. Implement: Follow [Integration Plan](INTEGRATION_PLAN.md)
3. Reference: [iOS Documentation](IOS_SHORTCUTS.md)

### For Architects
1. Read: [Integration Plan](INTEGRATION_PLAN.md)
2. Review: Architecture sections
3. Validate: Against Acceptance Criteria (AC-HA1-HA4)

### For Users
1. Read: [Onboarding](ONBOARDING.md)
2. Setup: Follow [Quick Start](QUICKSTART.md)
3. Learn: Example interactions in [Summary](SUMMARY.md)

---

## Implementation Status

### Complete (Backend)
- [x] HomeAssistantClient (Python)
- [x] REST API integration
- [x] Service calls, state queries
- [x] DelegationManager integration
- [x] Setup wizard
- [x] janet-max module
- [x] Dashboard access (open HA in browser)

### In Progress (iOS)
- [ ] HomeAssistantManager.swift
- [ ] Settings UI
- [ ] Voice command integration
- [ ] Shortcut creation
- [ ] Offline queueing

### Planned
- [ ] Watch, Desktop, Advanced features

---

## Code Locations

### Backend (janet-seed, janet-max)
- `JanetOS/janet-seed/src/delegation/home_assistant.py`
- `JanetOS/janet-seed/src/expansion/wizards/home_assistant_wizard.py`
- `JanetOS/janet-seed/src/delegation/handlers/home_assistant_dashboard_handler.py`
- `janet-max/src/modules/home-assistant.janet`

### This Repo (home-assistant-janet)
- `custom_components/janet/` - Janet as HA device

---

**Ready to start?** [Quick Start](QUICKSTART.md) | [Summary](SUMMARY.md) | [Roadmap](ROADMAP.md)
