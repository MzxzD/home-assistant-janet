# Home Assistant + iOS Shortcuts + Siri Integration

**JanetOS Feature:** Control your smart home using Janet through Home Assistant, with automatic iOS Shortcuts creation and Siri voice commands.

**Status:** Architecture defined, ready for implementation  
**Acceptance Criteria:** AC-HA1–HA4  
**Related:** [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md), [Home Assistant Docs](https://developers.home-assistant.io/)

---

## Overview

Janet integrates with Home Assistant to provide voice-controlled smart home automation that works across iPhone, Apple Watch, and Siri. When you ask Janet to control a device, she:

1. **Calls Home Assistant API** to execute the action
2. **Creates an iOS Shortcut** automatically for future use
3. **Enables Siri voice commands** ("Hey Siri, living room on")
4. **Syncs to Green Vault** so shortcuts work across all your devices

This combines the power of Home Assistant (local, privacy-first smart home) with the convenience of iOS Shortcuts and Siri.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  User: "Hey Janet, turn on living room lights"             │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  SiriKitIntegration.swift                                   │
│  • Voice recognition via Speech framework                   │
│  • Intent classification: "turn_on_lights"                  │
│  • Parameters: {"entity": "light.living_room"}              │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  DynamicShortcutBuilder.swift                               │
│  • Check: Does shortcut exist for this intent?              │
│  • If NO: Create new shortcut interactively                 │
│  • If YES: Execute existing shortcut                        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  HomeAssistantManager.swift (TO IMPLEMENT)                  │
│  • REST API client: http://homeassistant.local:8123         │
│  • Service calls: light.turn_on, switch.toggle, etc.        │
│  • Entity state queries                                     │
│  • Scene activation                                         │
│  • WebSocket for real-time updates (optional)               │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  Home Assistant Server (Local Network)                      │
│  • http://homeassistant.local:8123/api/services/...         │
│  • Long-lived access token authentication                   │
│  • Local control (no cloud required)                        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  Smart Home Devices                                         │
│  • Lights turn on                                           │
│  • Janet confirms: "Living room lights are on!"             │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  iOS Shortcuts App                                          │
│  • New shortcut saved: "Living Room On"                     │
│  • Siri phrase: "Hey Siri, living room on"                 │
│  • Synced to Green Vault for other devices                  │
└─────────────────────────────────────────────────────────────┘
```

---

## User Experience Flow

### First Time: Learning Mode

```
User: "Hey Janet, turn on living room lights"

Janet: "I don't have a shortcut for that yet. Let me help you create one.
        What's the Home Assistant entity ID?"

User: "light.living_room"

Janet: "Got it! What should I call this shortcut?"

User: "Living Room On"

Janet: [Creates shortcut]
       [Calls Home Assistant API]
       [Saves to Green Vault]
       "Done! Living room lights are on. 
        Next time, you can say 'Hey Siri, living room on' directly!"
```

### Subsequent Times: Instant Execution

```
User: "Hey Janet, turn on living room lights"

Janet: [Finds existing shortcut]
       [Executes immediately]
       "Living room lights are on!"

// OR via Siri directly:

User: "Hey Siri, living room on"

Siri: [Executes shortcut]
      [Calls Home Assistant]
      "Done."
```

---

## Implementation Components

### 1. HomeAssistantManager.swift (NEW)

**Location:** `platforms/ios/JanetOS-iOS/Sources/Core/HomeAssistantManager.swift`

**Responsibilities:**
- REST API client for Home Assistant
- Service calls (lights, switches, scenes, climate)
- Entity state queries
- Configuration management (URL, token)
- Error handling and offline queueing

**Key Methods:**

```swift
class HomeAssistantManager: ObservableObject {
    // Configuration
    func configure(url: String, token: String)
    
    // Service Calls
    func callService(domain: String, service: String, entityId: String) async throws
    func turnOn(_ entityId: String) async throws
    func turnOff(_ entityId: String) async throws
    func toggle(_ entityId: String) async throws
    func activateScene(_ sceneId: String) async throws
    
    // State Queries
    func getState(for entityId: String) async throws -> EntityState
    func getAllStates() async throws -> [EntityState]
    
    // Discovery
    func discoverEntities() async throws -> [Entity]
    func getServices() async throws -> [Service]
}
```

### 2. Integration with DynamicShortcutBuilder

**Enhancement:** Add Home Assistant intent recognition

```swift
// In DynamicShortcutBuilder.swift

private func recognizeIntent(from text: String) async -> RecognizedIntent? {
    // Existing code...
    
    // Add Home Assistant patterns
    if text.contains("turn on") || text.contains("turn off") || 
       text.contains("toggle") || text.contains("activate") {
        return recognizeHomeAssistantIntent(from: text)
    }
}

private func recognizeHomeAssistantIntent(from text: String) -> RecognizedIntent? {
    // Parse: "turn on living room lights"
    // Extract: action="turn_on", entity="light.living_room"
    
    let action = extractAction(from: text) // "turn_on", "turn_off", "toggle"
    let entity = extractEntity(from: text) // "light.living_room"
    
    return RecognizedIntent(
        action: "home_assistant_\(action)",
        parameters: ["entity_id": entity],
        confidence: 0.9
    )
}
```

### 3. Shortcut Definition for Home Assistant

```swift
// In DynamicShortcutBuilder.swift

struct HomeAssistantShortcut: Codable {
    let entityId: String
    let domain: String      // "light", "switch", "scene"
    let service: String     // "turn_on", "turn_off", "toggle"
    let friendlyName: String
    let siriPhrase: String
    
    var urlScheme: String {
        // Format: janetos://ha/call_service?domain=light&service=turn_on&entity_id=light.living_room
        return "janetos://ha/call_service?domain=\(domain)&service=\(service)&entity_id=\(entityId)"
    }
}
```

### 4. Siri Intent Donation

**Enhancement:** Donate Home Assistant shortcuts to Siri

```swift
// In JanetShortcuts.swift

func donateHomeAssistantShortcut(_ shortcut: HomeAssistantShortcut) {
    let intent = INPlayMediaIntent()
    intent.suggestedInvocationPhrase = shortcut.siriPhrase
    
    let interaction = INInteraction(intent: intent, response: nil)
    interaction.identifier = "ha-\(shortcut.entityId)"
    
    interaction.donate { error in
        if let error = error {
            print("⚠️ Failed to donate HA shortcut: \(error)")
        } else {
            print("✅ Donated Siri phrase: '\(shortcut.siriPhrase)'")
        }
    }
}
```

---

## Configuration

### Home Assistant Setup

1. **Install Home Assistant** (if not already installed)
   - Docker: `docker run -d --name homeassistant -p 8123:8123 homeassistant/home-assistant`
   - Home Assistant OS: Flash to device
   - Supervised: Follow [installation guide](https://www.home-assistant.io/installation/)

2. **Create Long-Lived Access Token**
   - Open Home Assistant: `http://homeassistant.local:8123`
   - Profile → Security → Long-Lived Access Tokens
   - Create token: "JanetOS iOS"
   - Copy token (you won't see it again!)

3. **Configure in JanetOS**
   - Open JanetOS app → Settings → Home Assistant
   - Enter URL: `http://homeassistant.local:8123`
   - Enter token: `[paste token]`
   - Tap "Test Connection"
   - ✅ "Connected to Home Assistant"

### JanetOS App Configuration

**Settings UI:**

```swift
// In SettingsView.swift

Section("Home Assistant") {
    TextField("URL", text: $homeAssistantURL)
        .autocapitalization(.none)
        .keyboardType(.URL)
    
    SecureField("Access Token", text: $homeAssistantToken)
    
    Button("Test Connection") {
        Task {
            let success = await HomeAssistantManager.shared.testConnection()
            connectionStatus = success ? "Connected ✅" : "Failed ❌"
        }
    }
    
    if !connectionStatus.isEmpty {
        Text(connectionStatus)
            .foregroundColor(connectionStatus.contains("✅") ? .green : .red)
    }
    
    Button("Discover Devices") {
        Task {
            let entities = await HomeAssistantManager.shared.discoverEntities()
            print("Found \(entities.count) entities")
        }
    }
}
```

---

## API Reference

### Home Assistant REST API

**Base URL:** `http://homeassistant.local:8123/api`

**Authentication:** 
```
Authorization: Bearer YOUR_LONG_LIVED_ACCESS_TOKEN
```

### Common Endpoints

#### 1. Call Service

```http
POST /api/services/{domain}/{service}
Content-Type: application/json
Authorization: Bearer {token}

{
  "entity_id": "light.living_room"
}
```

**Examples:**

```swift
// Turn on light
POST /api/services/light/turn_on
{"entity_id": "light.living_room"}

// Turn off switch
POST /api/services/switch/turn_off
{"entity_id": "switch.bedroom_fan"}

// Activate scene
POST /api/services/scene/turn_on
{"entity_id": "scene.movie_time"}

// Set thermostat
POST /api/services/climate/set_temperature
{"entity_id": "climate.living_room", "temperature": 72}
```

#### 2. Get State

```http
GET /api/states/{entity_id}
Authorization: Bearer {token}
```

**Response:**

```json
{
  "entity_id": "light.living_room",
  "state": "on",
  "attributes": {
    "friendly_name": "Living Room Light",
    "brightness": 255,
    "color_temp": 370
  }
}
```

#### 3. Get All States

```http
GET /api/states
Authorization: Bearer {token}
```

#### 4. Get Services

```http
GET /api/services
Authorization: Bearer {token}
```

---

## Example Shortcuts

### 1. Turn On Living Room Lights

**Voice Commands:**
- "Hey Janet, turn on living room lights"
- "Hey Siri, living room on"

**Shortcut Definition:**

```json
{
  "id": "ha-light-living-room-on",
  "intent": "home_assistant_turn_on",
  "parameters": {
    "entity_id": "light.living_room",
    "domain": "light",
    "service": "turn_on"
  },
  "urlScheme": "janetos://ha/call_service?domain=light&service=turn_on&entity_id=light.living_room",
  "name": "Living Room On",
  "description": "Turn on living room lights",
  "siriPhrase": "Living room on"
}
```

### 2. Movie Time Scene

**Voice Commands:**
- "Hey Janet, activate movie time"
- "Hey Siri, movie time"

**Shortcut Definition:**

```json
{
  "id": "ha-scene-movie-time",
  "intent": "home_assistant_activate_scene",
  "parameters": {
    "entity_id": "scene.movie_time",
    "domain": "scene",
    "service": "turn_on"
  },
  "urlScheme": "janetos://ha/call_service?domain=scene&service=turn_on&entity_id=scene.movie_time",
  "name": "Movie Time",
  "description": "Activate movie time scene",
  "siriPhrase": "Movie time"
}
```

### 3. Good Night Routine

**Voice Commands:**
- "Hey Janet, good night" (triggers evening routine + this)
- "Hey Siri, good night routine"

**Actions:**
- Turn off all lights
- Lock doors
- Set thermostat to 68°F
- Activate security system

**Shortcut Definition:**

```json
{
  "id": "ha-scene-good-night",
  "intent": "home_assistant_good_night",
  "parameters": {
    "entity_id": "scene.good_night",
    "domain": "scene",
    "service": "turn_on"
  },
  "urlScheme": "janetos://ha/call_service?domain=scene&service=turn_on&entity_id=scene.good_night",
  "name": "Good Night Routine",
  "description": "Turn off lights, lock doors, set thermostat",
  "siriPhrase": "Good night routine"
}
```

---

## Offline Mode Support

### Behavior When Offline

1. **Network Unavailable:**
   - Commands queued in `OfflineManager`
   - Janet responds: "I've queued that command. It will execute when we're back online."
   - Shows pending count in UI

2. **Home Assistant Unreachable:**
   - Retry with exponential backoff
   - After 3 attempts: queue for later
   - Notification when connection restored

3. **Queued Commands:**
   - Stored in UserDefaults
   - Auto-execute when online
   - Deduplicated (don't turn light on 5 times)

### Implementation

```swift
// In HomeAssistantManager.swift

func callService(domain: String, service: String, entityId: String) async throws {
    // Check if online
    guard OfflineManager.shared.isOnline else {
        // Queue for later
        let command = HACommand(domain: domain, service: service, entityId: entityId)
        OfflineManager.shared.queueHomeAssistantCommand(command)
        throw HomeAssistantError.offline
    }
    
    // Execute normally
    try await executeService(domain: domain, service: service, entityId: entityId)
}
```

---

## Security & Privacy

### Local-First Architecture

✅ **All communication is local** (LAN only)
- Home Assistant runs on your network
- No cloud services required
- Data never leaves your home

✅ **Token stored securely**
- iOS Keychain for access token
- Never logged or transmitted
- User can revoke anytime

✅ **Constitutional AI compliance**
- Major actions trigger Soul Check
- User confirmation required for:
  - Unlocking doors
  - Disabling security
  - Temperature changes >10°F

### Token Management

```swift
// Store token securely
KeychainManager.shared.save(token: token, for: "home_assistant_token")

// Retrieve token
let token = KeychainManager.shared.retrieve(key: "home_assistant_token")

// Delete token
KeychainManager.shared.delete(key: "home_assistant_token")
```

---

## Testing

### Manual Testing Checklist

- [ ] Configure Home Assistant URL and token
- [ ] Test connection (should show "Connected ✅")
- [ ] Discover entities (should list all devices)
- [ ] Create shortcut: "Turn on living room lights"
  - [ ] Janet asks for entity ID
  - [ ] Janet asks for shortcut name
  - [ ] Shortcut saved successfully
  - [ ] Light turns on
- [ ] Execute existing shortcut: "Turn on living room lights"
  - [ ] Executes immediately (no questions)
  - [ ] Light turns on
- [ ] Test Siri: "Hey Siri, living room on"
  - [ ] Shortcut executes
  - [ ] Light turns on
- [ ] Test offline mode:
  - [ ] Disconnect WiFi
  - [ ] Try command
  - [ ] Command queued
  - [ ] Reconnect WiFi
  - [ ] Command executes automatically
- [ ] Test on Apple Watch
  - [ ] Same shortcuts work
  - [ ] Voice commands work

### Automated Testing

```swift
// In HomeAssistantManagerTests.swift

func testTurnOnLight() async throws {
    let manager = HomeAssistantManager.shared
    manager.configure(url: "http://test.local:8123", token: "test_token")
    
    try await manager.turnOn("light.living_room")
    
    let state = try await manager.getState(for: "light.living_room")
    XCTAssertEqual(state.state, "on")
}

func testOfflineQueueing() async throws {
    OfflineManager.shared.offlineMode = true
    
    let manager = HomeAssistantManager.shared
    
    do {
        try await manager.turnOn("light.living_room")
        XCTFail("Should throw offline error")
    } catch HomeAssistantError.offline {
        // Expected
    }
    
    XCTAssertEqual(OfflineManager.shared.pendingRequestsCount, 1)
}
```

---

## Troubleshooting

### Connection Issues

**Problem:** "Cannot connect to Home Assistant"

**Solutions:**
1. Check Home Assistant is running: `http://homeassistant.local:8123`
2. Verify token is correct (create new one if needed)
3. Check firewall settings (allow port 8123)
4. Try IP address instead of hostname: `http://192.168.1.100:8123`
5. Ensure iPhone and HA are on same network

### Entity Not Found

**Problem:** "Entity light.living_room not found"

**Solutions:**
1. Check entity ID in Home Assistant UI
2. Entity IDs are case-sensitive
3. Use discovery: Settings → Home Assistant → Discover Devices
4. Verify entity is enabled in Home Assistant

### Shortcut Not Working

**Problem:** Shortcut executes but nothing happens

**Solutions:**
1. Check Home Assistant logs: Settings → System → Logs
2. Verify entity supports the service (e.g., some lights don't support brightness)
3. Test service call directly in Home Assistant Developer Tools
4. Check entity state: might already be in desired state

### Siri Not Recognizing

**Problem:** "Hey Siri, living room on" doesn't work

**Solutions:**
1. Check Siri is enabled: Settings → Siri & Search
2. Verify shortcut was donated: Check Shortcuts app
3. Try different phrase (avoid conflicts with existing shortcuts)
4. Re-donate shortcut: Delete and recreate
5. Wait 5-10 minutes for Siri to index new shortcuts

---

## Advanced Features

### 1. State-Based Shortcuts

**Example:** Toggle light (turn on if off, turn off if on)

```swift
func toggleLight(_ entityId: String) async throws {
    let state = try await getState(for: entityId)
    
    if state.state == "on" {
        try await turnOff(entityId)
    } else {
        try await turnOn(entityId)
    }
}
```

### 2. Conditional Shortcuts

**Example:** "Turn on lights only if dark outside"

```swift
func turnOnLightsIfDark() async throws {
    let sunState = try await getState(for: "sun.sun")
    
    guard sunState.state == "below_horizon" else {
        print("It's still light outside, skipping")
        return
    }
    
    try await turnOn("light.living_room")
}
```

### 3. Multi-Device Shortcuts

**Example:** "Turn on all living room devices"

```swift
func turnOnAllInRoom(_ room: String) async throws {
    let entities = try await discoverEntities()
    let roomEntities = entities.filter { $0.area == room }
    
    for entity in roomEntities {
        try await turnOn(entity.entityId)
    }
}
```

### 4. Scheduled Shortcuts

**Example:** "Turn on lights at sunset"

```swift
// Use iOS Background Tasks
func scheduleAtSunset() {
    let request = BGAppRefreshTaskRequest(identifier: "com.janetos.sunset")
    request.earliestBeginDate = calculateSunsetTime()
    
    try? BGTaskScheduler.shared.submit(request)
}
```

---

## Integration with JanetOS Features

### Morning Routine (AC-MR1-MR12)

When user says "Good morning Janet!" or on OS boot:

```swift
func morningRoutine() async {
    // ... existing morning routine code ...
    
    // Add Home Assistant actions
    if Config.homeAssistantEnabled {
        try? await HomeAssistantManager.shared.activateScene("scene.good_morning")
        // Turns on lights, opens blinds, starts coffee maker
    }
}
```

### Evening Routine (AC-ER1-ER8)

When user says "Good night Janet":

```swift
func eveningRoutine() async {
    // ... existing evening routine code ...
    
    // Add Home Assistant actions
    if Config.homeAssistantEnabled {
        try? await HomeAssistantManager.shared.activateScene("scene.good_night")
        // Turns off lights, locks doors, arms security
    }
}
```

### File Search Integration

**Example:** "Janet, find my Home Assistant config"

```swift
// Janet can search for and open HA configuration files
// Integrates with AC-F1-F8 (File Operations)
```

---

## Roadmap

### Phase 1: Basic Control (Current)
- [x] Architecture defined
- [ ] HomeAssistantManager implementation
- [ ] REST API client
- [ ] Basic service calls (on/off/toggle)
- [ ] Configuration UI
- [ ] Shortcut creation

### Phase 2: Advanced Features
- [ ] WebSocket support (real-time updates)
- [ ] Entity discovery and autocomplete
- [ ] State-based shortcuts
- [ ] Multi-device shortcuts
- [ ] Scheduled shortcuts

### Phase 3: Deep Integration
- [ ] Janet can create HA instances (AC-HA4)
- [ ] HA dashboard in JanetOS
- [ ] Custom scenes via Janet
- [ ] Automation suggestions
- [ ] Energy monitoring

---

## References

- **Home Assistant Docs:** https://developers.home-assistant.io/
- **REST API:** https://developers.home-assistant.io/docs/api/rest/
- **iOS Companion:** https://companion.home-assistant.io/docs/integrations/siri-shortcuts
- **Acceptance Criteria:** [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md) (AC-HA1-HA4)
- **Dynamic Shortcuts:** [DYNAMIC_SHORTCUTS_COMPLETE.md](../DYNAMIC_SHORTCUTS_COMPLETE.md)

---

## Contributing

To implement this feature:

1. Create `HomeAssistantManager.swift` (see Implementation Components above)
2. Enhance `DynamicShortcutBuilder.swift` with HA intent recognition
3. Add Settings UI for HA configuration
4. Implement offline queueing for HA commands
5. Add Siri intent donation for HA shortcuts
6. Write tests (see Testing section)
7. Update acceptance criteria coverage

**Questions?** Open an issue or ask Janet! 😊
