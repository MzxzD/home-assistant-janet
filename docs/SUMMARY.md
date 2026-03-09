# Home Automation Integration - Summary

**Date:** 2026-03-02  
**Status:** Ready to Implement

---

## What We've Built

A comprehensive plan to integrate Home Assistant into the entire Janet ecosystem, enabling voice-controlled smart home automation across all platforms.

### Documents (in this repo)

1. **[INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)** - Complete implementation plan, 5 phases
2. **[QUICKSTART.md](QUICKSTART.md)** - Get running in 30 minutes
3. **[DASHBOARD_ACCESS.md](DASHBOARD_ACCESS.md)** - Janet opens HA in browser

---

## Current State

### Already Implemented (Backend)

**janet-seed (Python):**
- `HomeAssistantClient` class with REST API integration
- Service calls (turn_on, turn_off, set_temperature, etc.)
- State queries (get_state, get_all_entities)
- Connection testing
- Integration with `DelegationManager`
- Setup wizard (`HomeAssistantWizard`)

**janet-max (Janet language):**
- Home Assistant module with WebSocket support
- Event handling (state changes, service calls)
- Device control and state queries
- Real-time updates via WebSocket

**Locations:**
- JanetOS/janet-seed: `src/delegation/home_assistant.py`, `home_assistant_wizard.py`, `home_assistant_dashboard_handler.py`
- janet-max: `src/modules/home-assistant.janet`

**Dashboard Access:** Janet can open HA dashboard in browser via voice. See [DASHBOARD_ACCESS.md](DASHBOARD_ACCESS.md)

### Ready to Implement (Frontend)

- iOS: HomeAssistantManager, Settings UI, shortcuts
- Watch, Desktop, Advanced features (see [ROADMAP.md](ROADMAP.md))

---

## Architecture

```
User Voice Command
       ↓
iOS/Watch/Desktop App
       ↓
janet-seed (WebSocket)
       ↓
Home Assistant REST API
       ↓
Smart Home Devices
```

### Key Features

1. **Voice-First**: "Hey Janet, turn on living room lights"
2. **Offline-First**: Commands queue when offline, execute when online
3. **Privacy-First**: Local network only, no cloud
4. **Constitutional AI**: Soul Check for security actions (doors, locks)
5. **Cross-Platform**: iPhone, Watch, Desktop

---

## Security & Privacy

- **Soul Check** for unlocking doors, disabling security, large temp changes
- **Token Security**: Keychain storage, never logged
- **Local-First**: All on LAN, no cloud, data never leaves home

---

## Resources

- [Quick Start](QUICKSTART.md)
- [Integration Plan](INTEGRATION_PLAN.md)
- [iOS Docs](IOS_SHORTCUTS.md)
- [Troubleshooting Firewall](TROUBLESHOOTING_FIREWALL.md)
