# Home Automation Quick Start Guide
**Get Home Assistant working with Janet in 30 minutes**

---

## What You'll Build

By the end of this guide, you'll be able to:
- Say "Hey Janet, turn on living room lights" on iPhone
- Control devices from Apple Watch
- Use "Hey Siri, living room on" shortcuts
- Queue commands when offline
- See all devices in Janet's interface

---

## Prerequisites

### Required
- Home Assistant installed and running (`http://homeassistant.local:8123` or your IP)
- Long-lived access token created
- Janet iOS app installed
- janet-seed running (backend)
- Xcode 15+ (for development)

### Optional
- Apple Watch, JanetOS desktop

---

## Step 1: Configure janet-seed Backend (5 minutes)

```bash
cd JanetOS/janet-seed

# Set environment
export HOME_ASSISTANT_URL=http://homeassistant.local:8123
export HOME_ASSISTANT_TOKEN=your_long_lived_access_token_here

# Test connection
python -c "
from src.delegation.home_assistant import HomeAssistantClient
client = HomeAssistantClient(
    base_url='http://homeassistant.local:8123',
    access_token='your_token_here'
)
print('Connected!' if client.test_connection() else 'Failed')
"
```

---

## Step 2–5: iOS, Settings, Testing

See [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) Phase 2 and [IOS_SHORTCUTS.md](IOS_SHORTCUTS.md) for full details.

---

## Quick Troubleshooting

### Cannot connect
- Check firewall: [TROUBLESHOOTING_FIREWALL.md](TROUBLESHOOTING_FIREWALL.md)
- Verify token: `curl -H "Authorization: Bearer TOKEN" http://homeassistant.local:8123/api/`
- Same network: `ping homeassistant.local`

### Entity not found
- Use exact entity ID (case-sensitive)
- List entities: `curl -H "Authorization: Bearer TOKEN" http://homeassistant.local:8123/api/states | jq '.[].entity_id'`

---

## Next Steps

- [Integration Plan](INTEGRATION_PLAN.md)
- [iOS Documentation](IOS_SHORTCUTS.md)
- [Dashboard Access](DASHBOARD_ACCESS.md)
