# Installation Guide - Janet Home Assistant Integration

## Quick Start

### Step 1: Install the Integration

**Option A: Manual Installation (Recommended for now)**

1. Copy the integration to your Home Assistant:
   ```bash
   cp -r /Users/mzxzd/Documents/Janet-Projects/home-assistant-janet/custom_components/janet \
         /path/to/homeassistant/config/custom_components/
   ```

2. Restart Home Assistant

**Option B: Direct Copy to Raspberry Pi**

If your Home Assistant is on `192.168.0.25`:

```bash
# From your Mac
cd /Users/mzxzd/Documents/Janet-Projects/home-assistant-janet
scp -r custom_components/janet homeassistant@192.168.0.25:/config/custom_components/

# SSH into the Pi and restart HA
ssh homeassistant@192.168.0.25
ha core restart
```

### Step 2: Configure Janet API Endpoints

Janet needs to expose REST API endpoints for Home Assistant. Add these to `janet-seed`:

**Create: `Janet-Projects/JanetOS/janet-seed/src/api/home_assistant_api.py`**

```python
"""
Home Assistant API endpoints for Janet.
Provides REST API for Home Assistant integration.
"""
from flask import Flask, jsonify, request
from typing import Dict, Any
import logging

_LOGGER = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "janet-seed"}), 200


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get Janet's current status."""
    # TODO: Get actual status from JanetCore
    return jsonify({
        "state": "idle",
        "uptime": 12345,
        "model": "qwen2.5-coder:7b",
        "voice_enabled": True,
        "in_conversation": False,
        "memory_usage": 1024 * 1024 * 50,  # 50 MB
        "green_vault_entries": 42,
        "blue_vault_active": False,
        "red_vault_entries": 3,
    }), 200


@app.route('/api/speak', methods=['POST'])
def speak():
    """Make Janet speak a message."""
    data = request.get_json()
    message = data.get('text', '')
    voice = data.get('voice')
    
    _LOGGER.info(f"Speak request: {message} (voice: {voice})")
    
    # TODO: Integrate with Janet's TTS system
    # from src.voice.tts import speak_text
    # speak_text(message)
    
    return jsonify({"status": "success", "message": message}), 200


@app.route('/api/command', methods=['POST'])
def command():
    """Send a voice command to Janet."""
    data = request.get_json()
    command = data.get('command', '')
    
    _LOGGER.info(f"Command request: {command}")
    
    # TODO: Integrate with Janet's conversation system
    # from src.core.janet_brain import process_input
    # response = process_input(command)
    
    return jsonify({
        "status": "success",
        "command": command,
        "response": "Command received"
    }), 200


def start_api_server(host='0.0.0.0', port=8080):
    """Start the API server."""
    _LOGGER.info(f"Starting Home Assistant API server on {host}:{port}")
    app.run(host=host, port=port, debug=False)
```

### Step 3: Add Janet to Home Assistant

1. Open Home Assistant: `http://192.168.0.25:8123`
2. Go to **Settings** → **Devices & Services**
3. Click **+ Add Integration**
4. Search for "**Janet**"
5. Enter connection details:
   - **Host**: Your Mac's IP (e.g., `192.168.0.121`) or `localhost` if on same machine
   - **API Port**: `8080`
   - **WebSocket Port**: `8765`
6. Click **Submit**

### Step 4: Verify Installation

Check that sensors appear:
- `sensor.janet_status`
- `sensor.janet_conversation`
- `sensor.janet_memory`

Check that services are available:
- `janet.speak`
- `janet.command`

## Testing

### Test 1: Health Check

```bash
curl http://localhost:8080/health
```

Expected response:
```json
{"status": "ok", "service": "janet-seed"}
```

### Test 2: Status Check

```bash
curl http://localhost:8080/api/status
```

### Test 3: Speak Command

```bash
curl -X POST http://localhost:8080/api/speak \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello from Home Assistant"}'
```

### Test 4: Voice Command

```bash
curl -X POST http://localhost:8080/api/command \
  -H "Content-Type: application/json" \
  -d '{"command": "What time is it?"}'
```

### Test 5: Home Assistant Service

In Home Assistant, go to **Developer Tools** → **Services**:

```yaml
service: janet.speak
data:
  message: "Testing Janet integration"
```

## Troubleshooting

### Integration Not Found

1. Check files are in correct location:
   ```bash
   ls -la /config/custom_components/janet/
   ```

2. Restart Home Assistant:
   ```bash
   ha core restart
   ```

### Cannot Connect

1. Check Janet is running:
   ```bash
   curl http://localhost:8080/health
   ```

2. Check firewall:
   ```bash
   # On Mac
   sudo lsof -i :8080
   
   # On Raspberry Pi
   sudo ufw status
   ```

3. Check Home Assistant logs:
   - Settings → System → Logs
   - Search for "janet"

### WebSocket Issues

1. Verify WebSocket port is open:
   ```bash
   nc -zv localhost 8765
   ```

2. Check janet-seed WebSocket server is running

## Next Steps

1. **Create Automations** - Use Janet in your automations
2. **Add Voice Commands** - Integrate with voice assistants
3. **Monitor Status** - Watch Janet's sensors in dashboards
4. **Bidirectional Control** - Let Janet control your smart home

## Configuration Examples

See `README.md` for complete automation examples.

---

**Need Help?** Open an issue on GitHub: https://github.com/MzxzD/home-assistant-janet/issues
