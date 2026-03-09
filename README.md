# Janet AI Companion - Home Assistant Integration

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/MzxzD/home-assistant-janet)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Janet Home Automation](https://img.shields.io/badge/docs-Home%20Automation-blue)](docs/INDEX.md)

**Janet Home Automation — one repo.** Turn your Home Assistant into a bidirectional AI companion with Janet!

This custom integration allows Home Assistant to communicate with [Janet](https://github.com/MzxzD/JANET), enabling voice control, notifications, and intelligent automation.

## ✨ Features

### 🎤 Voice Control
- **Send commands to Janet** from Home Assistant automations
- **Receive responses** via text-to-speech
- **Natural language processing** for smart home control

### 📊 Real-time Monitoring
- **Status sensor** - Janet's current state (idle, listening, thinking, speaking)
- **Conversation sensor** - Active conversation tracking
- **Memory sensor** - Memory usage and vault statistics

### 🔔 Notifications
- **Notify platform** - Send messages to Janet to speak
- **Event-driven** - React to Janet's speech and status changes
- **Bidirectional** - Janet can trigger Home Assistant automations

### 🤖 Services
- `janet.speak` - Make Janet speak a message
- `janet.command` - Send a voice command to Janet

### 📊 Dashboard
- Add Janet to your Lovelace dashboard - see **[DASHBOARD.md](DASHBOARD.md)** for copy-paste cards

## 📚 Documentation

Full Janet Home Automation docs (integration plan, quickstart, roadmap, troubleshooting):

- **[docs/INDEX.md](docs/INDEX.md)** — Start here
- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** — Get running in 30 minutes
- **[docs/SUMMARY.md](docs/SUMMARY.md)** — Overview and status

## 📦 Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/MzxzD/home-assistant-janet`
6. Category: "Integration"
7. Click "Add"
8. Find "Janet AI Companion" and click "Download"
9. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/janet` folder to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

## ⚙️ Configuration

### Prerequisites

1. **Janet must be running** on your network
   - Default API port: `8080`
   - Default WebSocket port: `8765`
   - See [Janet documentation](https://github.com/MzxzD/JANET) and [docs/QUICKSTART.md](docs/QUICKSTART.md) for setup

2. **Network connectivity** between Home Assistant and Janet

### Setup via UI

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "**Janet**"
4. Enter your Janet connection details:
   - **Host**: `localhost` (or Janet's IP address)
   - **API Port**: `8080` (default)
   - **WebSocket Port**: `8765` (default)
5. Click **Submit**

### Setup via YAML (Alternative)

Add to your `configuration.yaml`:

```yaml
# Not supported - use UI configuration
```

This integration uses config flow and must be configured via the UI.

## 🚀 Usage

### Services

#### `janet.speak`

Make Janet speak a message using text-to-speech.

```yaml
service: janet.speak
data:
  message: "Hello! The front door is unlocked."
  voice: "default"  # optional
```

**Example Automation:**

```yaml
automation:
  - alias: "Notify when door unlocked"
    trigger:
      - platform: state
        entity_id: lock.front_door
        to: "unlocked"
    action:
      - service: janet.speak
        data:
          message: "Alert: The front door has been unlocked."
```

#### `janet.command`

Send a voice command to Janet as if you spoke it.

```yaml
service: janet.command
data:
  command: "Turn on the living room lights"
```

**Example Automation:**

```yaml
automation:
  - alias: "Good morning routine"
    trigger:
      - platform: time
        at: "07:00:00"
    action:
      - service: janet.command
        data:
          command: "Good morning Janet, activate morning routine"
```

### Sensors

#### `sensor.janet_status`

Shows Janet's current state.

**States:**
- `idle` - Ready and waiting
- `listening` - Actively listening for input
- `thinking` - Processing a request
- `speaking` - Delivering a response
- `disconnected` - Not connected

**Attributes:**
- `connected` - Connection status
- `host` - Janet's host address
- `uptime` - How long Janet has been running
- `model` - Current LLM model in use
- `voice_enabled` - Whether voice I/O is active

#### `sensor.janet_conversation`

Tracks active conversations.

**States:**
- `active` - Currently in a conversation
- `inactive` - No active conversation

**Attributes:**
- `last_input` - Last user input
- `last_response` - Last Janet response
- `turn_count` - Number of conversation turns

#### `sensor.janet_memory`

Shows memory usage in MB.

**Attributes:**
- `green_vault_entries` - Number of safe memories
- `blue_vault_active` - Ephemeral secrets active
- `red_vault_entries` - Number of encrypted secrets

### Notify Platform

Send notifications to Janet:

```yaml
service: notify.janet
data:
  message: "The washing machine is done!"
```

### Events

Listen for Janet events in automations:

#### `janet_speech`

Fired when Janet speaks.

```yaml
automation:
  - alias: "Log Janet speech"
    trigger:
      - platform: event
        event_type: janet_speech
    action:
      - service: logbook.log
        data:
          name: "Janet"
          message: "{{ trigger.event.data.text }}"
```

#### `janet_status`

Fired when Janet's status changes.

```yaml
automation:
  - alias: "Janet started listening"
    trigger:
      - platform: event
        event_type: janet_status
        event_data:
          state: "listening"
    action:
      - service: light.turn_on
        entity_id: light.indicator
        data:
          color_name: "blue"
```

#### `janet_command_result`

Fired when a command completes.

```yaml
automation:
  - alias: "Command completed"
    trigger:
      - platform: event
        event_type: janet_command_result
    action:
      - service: persistent_notification.create
        data:
          title: "Janet Command"
          message: "{{ trigger.event.data.result }}"
```

## 🎯 Example Automations

### Voice Notifications

```yaml
automation:
  - alias: "Motion detected announcement"
    trigger:
      - platform: state
        entity_id: binary_sensor.front_door_motion
        to: "on"
    action:
      - service: janet.speak
        data:
          message: "Motion detected at the front door."
```

### Bidirectional Control

```yaml
automation:
  - alias: "Janet controls lights"
    trigger:
      - platform: event
        event_type: janet_command_result
        event_data:
          command: "lights"
    action:
      - service: light.toggle
        entity_id: light.living_room
```

### Status-Based Automation

```yaml
automation:
  - alias: "Pause music when Janet speaks"
    trigger:
      - platform: state
        entity_id: sensor.janet_status
        to: "speaking"
    action:
      - service: media_player.media_pause
        entity_id: media_player.living_room
```

### Morning Routine

```yaml
automation:
  - alias: "Good morning with Janet"
    trigger:
      - platform: time
        at: "07:00:00"
    action:
      - service: janet.command
        data:
          command: "Good morning Janet"
      - delay:
          seconds: 2
      - service: janet.speak
        data:
          message: "Good morning! It's {{ now().strftime('%A, %B %d') }}. The temperature is {{ states('sensor.outdoor_temperature') }} degrees."
```

## 🔧 Troubleshooting

### Integration Not Showing Up

1. Ensure files are in `config/custom_components/janet/`
2. Restart Home Assistant
3. Check logs: **Settings** → **System** → **Logs**

### Cannot Connect

1. Verify Janet is running: `curl http://localhost:8080/health`
2. Check firewall settings
3. Ensure correct host and port
4. Check Home Assistant logs for connection errors

### WebSocket Issues

1. Verify WebSocket port (default: 8765)
2. Check Janet logs for WebSocket connections
3. Restart both Janet and Home Assistant

### Services Not Available

1. Ensure integration is configured
2. Check **Developer Tools** → **Services** for `janet.*`
3. Restart Home Assistant

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│     Home Assistant                      │
│  ┌───────────────────────────────────┐  │
│  │  Janet Integration                │  │
│  │  • Config Flow                    │  │
│  │  • Sensors (status, memory, etc.) │  │
│  │  • Notify Platform                │  │
│  │  • Services (speak, command)      │  │
│  └────────────┬──────────────────────┘  │
└───────────────┼─────────────────────────┘
                │
                │ REST API (port 8080)
                │ WebSocket (port 8765)
                │
┌───────────────▼─────────────────────────┐
│     Janet AI Companion                  │
│  ┌───────────────────────────────────┐  │
│  │  janet-seed                       │  │
│  │  • Constitutional AI              │  │
│  │  • Voice I/O                      │  │
│  │  • Memory Vaults                  │  │
│  │  • Delegation System              │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **This Integration**: https://github.com/MzxzD/home-assistant-janet
- **Documentation**: [docs/INDEX.md](docs/INDEX.md)
- **Issues**: https://github.com/MzxzD/home-assistant-janet/issues
- **Janet Ecosystem**: https://github.com/MzxzD/JANET
- **Home Assistant**: https://www.home-assistant.io

## 🙏 Acknowledgments

- Built for the [Janet AI Companion](https://github.com/MzxzD/JANET) project
- Inspired by the Home Assistant community
- Constitutional AI principles from the Janet ecosystem

---

**Made with ❤️ for the Janet community**
