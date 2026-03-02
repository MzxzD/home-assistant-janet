# Janet Home Assistant Integration - Quick Reference

## 🚀 Installation (3 Steps)

```bash
# 1. Copy to Home Assistant
scp -r custom_components/janet homeassistant@192.168.0.25:/config/custom_components/

# 2. Restart Home Assistant
ssh homeassistant@192.168.0.25
ha core restart

# 3. Add Integration
# UI: Settings → Devices & Services → Add Integration → "Janet"
```

## 📊 Sensors

| Entity | Description | States |
|--------|-------------|--------|
| `sensor.janet_status` | Janet's current state | idle, listening, thinking, speaking, disconnected |
| `sensor.janet_conversation` | Conversation tracking | active, inactive |
| `sensor.janet_memory` | Memory usage (MB) | Numeric value |

## 🎯 Services

### `janet.speak`
Make Janet speak a message.
```yaml
service: janet.speak
data:
  message: "Hello from Home Assistant"
  voice: "default"  # optional
```

### `janet.command`
Send a voice command to Janet.
```yaml
service: janet.command
data:
  command: "Turn on the living room lights"
```

### `notify.janet`
Send notification to Janet.
```yaml
service: notify.janet
data:
  message: "The washing machine is done"
```

## 📡 Events

| Event | Description | Data |
|-------|-------------|------|
| `janet_speech` | Janet spoke | `text` |
| `janet_status` | Status changed | `state`, `model`, etc. |
| `janet_command_result` | Command completed | `command`, `result` |

## 🎬 Example Automations

### Voice Notification
```yaml
automation:
  - alias: "Door unlocked notification"
    trigger:
      platform: state
      entity_id: lock.front_door
      to: "unlocked"
    action:
      service: janet.speak
      data:
        message: "The front door has been unlocked"
```

### Status-Based Action
```yaml
automation:
  - alias: "Pause music when Janet speaks"
    trigger:
      platform: state
      entity_id: sensor.janet_status
      to: "speaking"
    action:
      service: media_player.media_pause
      entity_id: media_player.living_room
```

### Event-Driven
```yaml
automation:
  - alias: "Log Janet speech"
    trigger:
      platform: event
      event_type: janet_speech
    action:
      service: logbook.log
      data:
        name: "Janet"
        message: "{{ trigger.event.data.text }}"
```

### Morning Routine
```yaml
automation:
  - alias: "Good morning"
    trigger:
      platform: time
      at: "07:00:00"
    action:
      - service: janet.command
        data:
          command: "Good morning Janet"
      - delay:
          seconds: 2
      - service: janet.speak
        data:
          message: "Good morning! Today is {{ now().strftime('%A') }}"
```

## 🔧 Configuration

### Connection Details
- **Host**: Your Janet IP (e.g., `192.168.0.121`)
- **API Port**: `8080` (default)
- **WebSocket Port**: `8765` (default)

### Required Janet Endpoints
```
GET  /health              # Health check
GET  /api/status          # Get status
POST /api/speak           # Make Janet speak
POST /api/command         # Send command
WS   ws://HOST:8765       # WebSocket events
```

## 🐛 Troubleshooting

### Integration Not Found
```bash
# Check files exist
ls -la /config/custom_components/janet/

# Restart HA
ha core restart
```

### Cannot Connect
```bash
# Test Janet API
curl http://192.168.0.121:8080/health

# Check firewall
sudo lsof -i :8080
```

### Services Not Available
1. Check integration is configured
2. Go to Developer Tools → Services
3. Search for `janet.`

## 📂 File Structure

```
custom_components/janet/
├── __init__.py           # Main integration
├── manifest.json         # Metadata
├── config_flow.py        # UI setup
├── const.py             # Constants
├── sensor.py            # Sensors
├── notify.py            # Notify platform
├── services.yaml        # Service definitions
├── strings.json         # UI strings
└── translations/
    └── en.json          # Translations
```

## 🔗 Quick Links

- **Full Documentation**: [README.md](README.md)
- **Installation Guide**: [INSTALLATION.md](INSTALLATION.md)
- **Project Summary**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **Janet Project**: [../README.md](../README.md)

## 💡 Pro Tips

1. **Use events** for real-time reactions
2. **Monitor sensors** in dashboards
3. **Create blueprints** for reusable automations
4. **Test with Developer Tools** before creating automations
5. **Check logs** for debugging: Settings → System → Logs

---

**Version**: 1.0.0  
**Updated**: 2026-03-02
