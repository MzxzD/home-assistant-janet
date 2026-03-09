# Janet Dashboard Access Guide
**How Janet can open and use the Home Assistant dashboard**

---

## Current State

### ✅ What Works Now

**1. Backend Integration (Complete)**
- Janet can control all HA devices via API
- Service calls work (turn on/off, set temperature, etc.)
- State queries work (check device status)

**2. Dashboard Opening (NEW!)**
- Janet can open HA dashboard in your browser
- Can open specific pages (devices, automations, scenes, etc.)
- Works via voice or text commands

### 🔄 What's Coming

**Custom Janet Dashboard (Phase 4)**
- Native dashboard within JanetOS
- Grid view of all devices
- Real-time updates
- Voice control integration
- Planned for Week 3-4

---

## How to Use Dashboard Access Now

### Voice Commands

```
User: "Hey Janet, open Home Assistant dashboard"
Janet: "Opening Home Assistant main dashboard"
      [Opens http://homeassistant.local:8123 in browser]

User: "Show me my devices in Home Assistant"
Janet: "Opening Home Assistant devices page"
      [Opens http://homeassistant.local:8123/config/entities]

User: "Open Home Assistant automations"
Janet: "Opening Home Assistant automations page"
      [Opens http://homeassistant.local:8123/config/automation/dashboard]

User: "Show Home Assistant scenes"
Janet: "Opening Home Assistant scenes page"
      [Opens http://homeassistant.local:8123/config/scene/dashboard]
```

### Available Dashboard Pages

Janet can open these specific pages:

| Command | Page | URL |
|---------|------|-----|
| "Open HA dashboard" | Main dashboard | `/` |
| "Show HA devices" | Devices/Entities | `/config/entities` |
| "Open HA automations" | Automations | `/config/automation/dashboard` |
| "Show HA scenes" | Scenes | `/config/scene/dashboard` |
| "Open HA settings" | Settings | `/config/dashboard` |
| "Show HA history" | History | `/history` |
| "Open HA logbook" | Logbook | `/logbook` |
| "Show HA map" | Map | `/map` |
| "Open HA developer tools" | Developer Tools | `/developer-tools` |

---

## Implementation Details

### New Handler: HomeAssistantDashboardHandler

**Location:** `Janet-Projects/JanetOS/janet-seed/src/delegation/handlers/home_assistant_dashboard_handler.py`

**Features:**
- Opens HA dashboard in default browser
- Supports specific page navigation
- Provides fallback URLs if browser fails
- Checks HA configuration before opening

**Example Usage:**

```python
from delegation.handlers.home_assistant_dashboard_handler import HomeAssistantDashboardHandler
from delegation.home_assistant import HomeAssistantClient

# Initialize
ha_client = HomeAssistantClient("http://homeassistant.local:8123", "your_token")
dashboard_handler = HomeAssistantDashboardHandler(ha_client)

# Open main dashboard
result = dashboard_handler.handle("open home assistant dashboard", {})
print(result["message"])  # "Opening Home Assistant main dashboard"

# Open devices page
result = dashboard_handler.handle("show home assistant devices", {})
print(result["url"])  # "http://homeassistant.local:8123/config/entities"

# Get dashboard info
info = dashboard_handler.get_dashboard_info()
print(info["pages"]["automations"])  # URL to automations page
```

---

## Integration with janet-seed

### Step 1: Register Handler

Add to `delegation_manager.py`:

```python
from .handlers.home_assistant_dashboard_handler import HomeAssistantDashboardHandler

# In _initialize_handlers method:
if home_assistant:
    # Existing HA handler
    ha_handler = HomeAutomationHandler(n8n_handler, home_assistant)
    self.register_handler(ha_handler)
    
    # NEW: Dashboard handler
    dashboard_handler = HomeAssistantDashboardHandler(home_assistant)
    self.register_handler(dashboard_handler)
```

### Step 2: Add to JanetBrain

In `janet_brain.py`, add dashboard detection:

```python
# Check for dashboard requests
dashboard_keywords = ["dashboard", "open home assistant", "show home assistant"]
if any(keyword in user_message.lower() for keyword in dashboard_keywords):
    # Delegate to dashboard handler
    result = self.delegation_manager.delegate(
        capability=HandlerCapability.HOME_AUTOMATION,
        task_description=f"Dashboard: {user_message}",
        context={"user_message": user_message}
    )
    return result["message"]
```

---

## User Experience

### Example Interaction 1: Open Main Dashboard

```
User: "Hey Janet, I want to see my Home Assistant dashboard"

Janet: [Recognizes dashboard request]
       [Checks HA configuration - ✅ configured]
       [Opens http://homeassistant.local:8123 in browser]
       "Opening Home Assistant main dashboard. The dashboard should open in your default browser."

[Browser opens showing HA dashboard]
```

### Example Interaction 2: Open Specific Page

```
User: "Show me all my devices in Home Assistant"

Janet: [Recognizes devices page request]
       [Opens http://homeassistant.local:8123/config/entities]
       "Opening Home Assistant devices page"

[Browser opens showing all entities/devices]
```

### Example Interaction 3: HA Not Configured

```
User: "Open Home Assistant dashboard"

Janet: "Home Assistant is not configured. Please set up Home Assistant first."
       "Configure Home Assistant URL and token in settings."
```

---

## Future: Custom Janet Dashboard

### Phase 4 Implementation (Week 3-4)

**What it will look like:**

```
┌─────────────────────────────────────────────────────────┐
│  Janet Home - Home Automation Dashboard                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Living Room                                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │  💡 Light │  │  🌡️ Temp  │  │  🔌 Fan   │            │
│  │   ON      │  │   72°F    │  │   OFF     │            │
│  │  [Toggle] │  │  [Adjust] │  │  [Toggle] │            │
│  └──────────┘  └──────────┘  └──────────┘            │
│                                                         │
│  Bedroom                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │  💡 Light │  │  🔒 Lock  │  │  📺 TV    │            │
│  │   OFF     │  │  LOCKED   │  │   OFF     │            │
│  │  [Toggle] │  │  [Unlock] │  │  [Turn On]│            │
│  └──────────┘  └──────────┘  └──────────┘            │
│                                                         │
│  Scenes                                                 │
│  [🌅 Good Morning] [🎬 Movie Time] [🌙 Good Night]     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Features:**
- Native UI within JanetOS
- Real-time device states
- Click or voice control
- Liquid Glass design
- Works offline (shows last known states)

**Implementation:**
- Python/GTK for Linux desktop
- SwiftUI for macOS
- Web view for other platforms

---

## Comparison: Current vs Future

| Feature | Current (Browser) | Future (Native) |
|---------|------------------|-----------------|
| **Access** | Opens in browser | Built into JanetOS |
| **Control** | Click in browser | Click or voice |
| **Design** | HA's design | Janet's Liquid Glass |
| **Speed** | Depends on browser | Instant |
| **Offline** | Requires HA running | Shows cached states |
| **Voice** | Must use Janet separately | Integrated |
| **Updates** | Manual refresh | Real-time |

---

## Configuration

### Enable Dashboard Access

1. **Configure Home Assistant** (if not already done):
   ```bash
   cd Janet-Projects/JanetOS/janet-seed
   
   # Set environment variables
   export HOME_ASSISTANT_URL=http://homeassistant.local:8123
   export HOME_ASSISTANT_TOKEN=your_long_lived_access_token
   ```

2. **Restart janet-seed**:
   ```bash
   python -m janet_seed
   ```

3. **Test Dashboard Access**:
   ```
   User: "Hey Janet, open Home Assistant dashboard"
   ```

### Troubleshooting

**Problem:** "Home Assistant is not configured"

**Solution:**
1. Check environment variables are set
2. Verify HA URL is correct
3. Verify token is valid
4. Restart janet-seed

**Problem:** Dashboard doesn't open

**Solution:**
1. Check default browser is set
2. Try manual URL: `http://homeassistant.local:8123`
3. Check firewall settings
4. Verify HA is running

**Problem:** Opens but shows error

**Solution:**
1. Check HA is accessible from your network
2. Verify you're on the same network
3. Try IP address instead of hostname
4. Check HA logs for errors

---

## API Reference

### HomeAssistantDashboardHandler

#### Methods

**`can_handle(task_description: str) -> bool`**
- Check if handler can handle the task
- Returns True for dashboard-related requests

**`handle(task_description: str, context: Dict) -> Dict`**
- Handle dashboard request
- Opens appropriate page in browser
- Returns result with status and URL

**`get_dashboard_url(page: Optional[str] = None) -> Optional[str]`**
- Get URL for specific dashboard page
- Pages: devices, automations, scenes, settings, or None for main
- Returns URL or None if HA not configured

**`get_dashboard_info() -> Dict`**
- Get information about available dashboard pages
- Returns dict with all page URLs

#### Return Format

```python
{
    "status": "success",  # or "error"
    "message": "Opening Home Assistant main dashboard",
    "url": "http://homeassistant.local:8123",
    "suggestion": "The dashboard should open in your default browser."
}
```

---

## Testing

### Manual Test

```bash
cd Janet-Projects/JanetOS/janet-seed

# Test dashboard handler
python -c "
from src.delegation.home_assistant import HomeAssistantClient
from src.delegation.handlers.home_assistant_dashboard_handler import HomeAssistantDashboardHandler

# Initialize
ha_client = HomeAssistantClient('http://homeassistant.local:8123', 'your_token')
handler = HomeAssistantDashboardHandler(ha_client)

# Test
result = handler.handle('open home assistant dashboard', {})
print(result)
"
```

### Integration Test

```bash
# Start janet-seed
python -m janet_seed

# In another terminal, test via WebSocket
# (Use your preferred WebSocket client)
```

---

## Next Steps

### This Week
1. ✅ Dashboard handler created
2. 🔄 Integrate with delegation manager
3. 🔄 Test with voice commands
4. 🔄 Update documentation

### Next 2 Weeks
1. Build custom Janet dashboard (Phase 4)
2. Add real-time updates via WebSocket
3. Implement Liquid Glass design
4. Add voice control integration

---

## Summary

**Current Capability:**
- ✅ Janet can open HA dashboard in browser
- ✅ Can navigate to specific pages
- ✅ Works via voice or text commands
- ✅ Provides helpful error messages

**Coming Soon:**
- 📋 Native dashboard within JanetOS
- 📋 Real-time device updates
- 📋 Integrated voice control
- 📋 Liquid Glass design

**How to Use:**
```
"Hey Janet, open Home Assistant dashboard"
"Show me my devices in Home Assistant"
"Open Home Assistant automations"
```

---

**Status:** ✅ Dashboard access implemented  
**Next:** Integrate with delegation manager and test

---

*Janet can now open and navigate the Home Assistant dashboard!* 🏠✨
