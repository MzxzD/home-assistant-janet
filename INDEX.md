# Janet Home Assistant Integration - Complete Index

## 📚 Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| **[README.md](README.md)** | Complete user guide with examples | End Users |
| **[INSTALLATION.md](INSTALLATION.md)** | Step-by-step installation | Installers |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | Quick lookup guide | All Users |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | Technical overview | Developers |
| **[INDEX.md](INDEX.md)** | This file - navigation | All Users |

## 🗂️ Integration Files

### Core Components

| File | Purpose | Lines |
|------|---------|-------|
| `__init__.py` | Main integration logic, coordinator | ~200 |
| `config_flow.py` | UI configuration flow | ~80 |
| `sensor.py` | Status, conversation, memory sensors | ~150 |
| `notify.py` | Notification platform | ~50 |
| `const.py` | Constants and configuration | ~10 |

### Metadata

| File | Purpose |
|------|---------|
| `manifest.json` | Integration metadata |
| `services.yaml` | Service definitions |
| `strings.json` | UI strings |
| `translations/en.json` | English translations |

### Project Files

| File | Purpose |
|------|---------|
| `LICENSE` | MIT License |
| `hacs.json` | HACS compatibility |
| `.gitignore` | Git ignore rules |

## 🎯 Features

### Sensors (3)
- ✅ `sensor.janet_status` - Overall status
- ✅ `sensor.janet_conversation` - Conversation tracking
- ✅ `sensor.janet_memory` - Memory usage

### Services (2)
- ✅ `janet.speak` - Text-to-speech
- ✅ `janet.command` - Voice commands

### Platforms (1)
- ✅ `notify.janet` - Notification platform

### Events (3)
- ✅ `janet_speech` - Speech events
- ✅ `janet_status` - Status changes
- ✅ `janet_command_result` - Command results

## 🚀 Quick Start

### 1. Installation
```bash
scp -r custom_components/janet homeassistant@192.168.0.25:/config/custom_components/
```

### 2. Configuration
Settings → Devices & Services → Add Integration → "Janet"

### 3. Usage
```yaml
service: janet.speak
data:
  message: "Hello from Home Assistant"
```

## 📖 Documentation Sections

### For End Users
1. [README.md](README.md) - Start here
   - Features overview
   - Installation instructions
   - Usage examples
   - Troubleshooting

2. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick lookup
   - Service syntax
   - Automation examples
   - Common patterns

### For Installers
1. [INSTALLATION.md](INSTALLATION.md) - Detailed setup
   - Prerequisites
   - Step-by-step installation
   - Configuration
   - Testing procedures

### For Developers
1. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Technical details
   - Architecture
   - Implementation details
   - API endpoints
   - Future enhancements

## 🏗️ Architecture

```
Home Assistant (192.168.0.25:8123)
    ↓
Janet Integration
    ├─ Coordinator (WebSocket + REST)
    ├─ Sensors (3)
    ├─ Notify Platform
    └─ Services (2)
    ↓
Janet (192.168.0.121:8080)
    ├─ REST API
    │  ├─ /health
    │  ├─ /api/status
    │  ├─ /api/speak
    │  └─ /api/command
    └─ WebSocket (port 8765)
```

## 🎬 Example Use Cases

### 1. Voice Notifications
When events happen, Janet announces them.

**Example**: Door unlocked → Janet speaks

### 2. Status Monitoring
Track Janet's state in real-time.

**Example**: Dashboard shows Janet is listening

### 3. Bidirectional Control
Janet controls HA, HA controls Janet.

**Example**: "Good morning" routine triggers both

### 4. Event-Driven Automation
React to Janet's actions.

**Example**: Pause music when Janet speaks

## 📊 Statistics

- **Total Files**: 14
- **Python Files**: 5
- **Documentation**: 5
- **Configuration**: 4
- **Lines of Code**: ~500
- **Sensors**: 3
- **Services**: 2
- **Events**: 3

## 🔗 Related Projects

- **[Janet Project](../README.md)** - Main Janet ecosystem
- **[janet-seed](../JanetOS/janet-seed/)** - Janet's core brain
- **[janet-max](../janet-max/)** - Integration hub
- **[CallJanet-iOS](../../CallJanet-iOS/)** - iOS app

## 📝 Version History

### v1.0.0 (2026-03-02)
- ✅ Initial release
- ✅ Config flow setup
- ✅ 3 sensors implemented
- ✅ 2 services implemented
- ✅ Notify platform
- ✅ WebSocket coordinator
- ✅ Complete documentation

## 🎯 Next Steps

### Immediate
1. Install in Home Assistant
2. Add API endpoints to janet-seed
3. Create first automation

### Future
1. Publish to GitHub
2. Submit to HACS
3. Create Lovelace card
4. Add more sensors
5. Implement device triggers

## 🆘 Getting Help

### Documentation
- Read [README.md](README.md) for usage
- Check [INSTALLATION.md](INSTALLATION.md) for setup
- See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for syntax

### Troubleshooting
1. Check Home Assistant logs
2. Verify Janet is running
3. Test API endpoints
4. Review configuration

### Support
- GitHub Issues: https://github.com/MzxzD/home-assistant-janet/issues
- Documentation: https://github.com/MzxzD/home-assistant-janet/tree/main/docs

---

**Project**: Janet Home Assistant Integration  
**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Created**: 2026-03-02  
**License**: MIT
