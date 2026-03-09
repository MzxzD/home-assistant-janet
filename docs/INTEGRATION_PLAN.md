# Home Automation Integration Plan
**Complete Home Assistant Integration Across Janet Ecosystem**

**Status:** 🔄 Ready to Implement  
**Date:** 2026-03-02  
**Priority:** High

---

## Executive Summary

This document outlines the complete integration of Home Assistant into the Janet ecosystem, enabling voice-controlled smart home automation across all platforms (iOS, watchOS, macOS, JanetOS) while maintaining Janet's core principles: offline-first, privacy-first, and constitutional AI.

### Current State

✅ **Already Implemented:**
- `janet-seed` Home Assistant REST API client (`delegation/home_assistant.py`)
- `janet-max` Home Assistant module (Janet language)
- Home Assistant wizard for setup (`expansion/wizards/home_assistant_wizard.py`)
- Delegation manager integration with HA capability
- Comprehensive iOS documentation (`HOME_ASSISTANT_IOS_SHORTCUTS.md`)

❌ **Not Yet Implemented:**
- iOS `HomeAssistantManager.swift`
- iOS Settings UI for HA configuration
- Dynamic shortcut creation for HA commands
- Siri intent donation for HA shortcuts
- Apple Watch HA controls
- JanetOS desktop HA dashboard
- "Janet creates Home Assistant instance" feature

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  User: "Hey Janet, turn on living room lights"             │
└─────────────────┬───────────────────────────────────────────┘
                  │
    ┌─────────────┴─────────────┐
    │                           │
    ▼                           ▼
┌─────────────┐         ┌──────────────┐
│  iOS App    │         │  JanetOS     │
│  (iPhone/   │         │  (Desktop)   │
│   Watch)    │         │              │
└──────┬──────┘         └──────┬───────┘
       │                       │
       └───────────┬───────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │  janet-seed Core    │
         │  (WebSocket Server) │
         │  Port 8765          │
         └─────────┬───────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │  Home Assistant     │
         │  REST API           │
         │  :8123              │
         └─────────┬───────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │  Smart Home Devices │
         │  (Lights, Switches, │
         │   Thermostat, etc.) │
         └─────────────────────┘
```

---

## Implementation Phases

### Phase 1: Core Backend (janet-seed) ✅ COMPLETE

**Status:** Already implemented

**Components:**
- ✅ `HomeAssistantClient` class with REST API integration
- ✅ Service calls (turn_on, turn_off, set_temperature)
- ✅ State queries (get_state, get_all_entities)
- ✅ Connection testing
- ✅ Integration with `DelegationManager`
- ✅ Setup wizard

**Location:** `Janet-Projects/JanetOS/janet-seed/src/delegation/home_assistant.py`

---

### Phase 2: iOS Implementation 🔄 IN PROGRESS

#### 2.1 HomeAssistantManager.swift (NEW)

**Location:** `CallJanet-iOS/JanetOS-iOS/Sources/Core/HomeAssistantManager.swift`

**Purpose:** iOS client for Home Assistant REST API

**Key Features:**
- REST API client
- Service calls (lights, switches, scenes, climate)
- Entity state queries
- Configuration management (URL, token in Keychain)
- Offline queueing
- Error handling

**Implementation:**

```swift
import Foundation
import Combine

class HomeAssistantManager: ObservableObject {
    static let shared = HomeAssistantManager()
    
    @Published var isConnected: Bool = false
    @Published var entities: [HAEntity] = []
    
    private var baseURL: String?
    private var accessToken: String?
    
    // MARK: - Configuration
    
    func configure(url: String, token: String) {
        self.baseURL = url.trimmingCharacters(in: CharacterSet(charactersIn: "/"))
        self.accessToken = token
        
        // Save to Keychain
        KeychainManager.shared.save(token: token, for: "home_assistant_token")
        UserDefaults.standard.set(url, forKey: "home_assistant_url")
    }
    
    func loadConfiguration() {
        self.baseURL = UserDefaults.standard.string(forKey: "home_assistant_url")
        self.accessToken = KeychainManager.shared.retrieve(key: "home_assistant_token")
    }
    
    // MARK: - Connection
    
    func testConnection() async -> Bool {
        guard let url = baseURL, let token = accessToken else {
            return false
        }
        
        let endpoint = "\(url)/api/"
        var request = URLRequest(url: URL(string: endpoint)!)
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        
        do {
            let (_, response) = try await URLSession.shared.data(for: request)
            if let httpResponse = response as? HTTPURLResponse {
                let connected = httpResponse.statusCode == 200
                await MainActor.run {
                    self.isConnected = connected
                }
                return connected
            }
        } catch {
            print("⚠️ HA connection test failed: \(error)")
        }
        
        return false
    }
    
    // MARK: - Service Calls
    
    func callService(domain: String, service: String, entityId: String, data: [String: Any] = [:]) async throws {
        guard let url = baseURL, let token = accessToken else {
            throw HAError.notConfigured
        }
        
        // Check if offline
        guard OfflineManager.shared.isOnline else {
            let command = HACommand(domain: domain, service: service, entityId: entityId, data: data)
            OfflineManager.shared.queueHomeAssistantCommand(command)
            throw HAError.offline
        }
        
        let endpoint = "\(url)/api/services/\(domain)/\(service)"
        var request = URLRequest(url: URL(string: endpoint)!)
        request.httpMethod = "POST"
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        var payload = data
        payload["entity_id"] = entityId
        request.httpBody = try JSONSerialization.data(withJSONObject: payload)
        
        let (_, response) = try await URLSession.shared.data(for: request)
        
        if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode != 200 {
            throw HAError.serviceCallFailed(statusCode: httpResponse.statusCode)
        }
    }
    
    func turnOn(_ entityId: String, brightness: Int? = nil) async throws {
        var data: [String: Any] = [:]
        if let brightness = brightness {
            data["brightness"] = brightness
        }
        try await callService(domain: "light", service: "turn_on", entityId: entityId, data: data)
    }
    
    func turnOff(_ entityId: String) async throws {
        let domain = entityId.split(separator: ".").first.map(String.init) ?? "light"
        try await callService(domain: domain, service: "turn_off", entityId: entityId)
    }
    
    func toggle(_ entityId: String) async throws {
        let domain = entityId.split(separator: ".").first.map(String.init) ?? "light"
        try await callService(domain: domain, service: "toggle", entityId: entityId)
    }
    
    func activateScene(_ sceneId: String) async throws {
        try await callService(domain: "scene", service: "turn_on", entityId: sceneId)
    }
    
    // MARK: - State Queries
    
    func getState(for entityId: String) async throws -> HAEntityState {
        guard let url = baseURL, let token = accessToken else {
            throw HAError.notConfigured
        }
        
        let endpoint = "\(url)/api/states/\(entityId)"
        var request = URLRequest(url: URL(string: endpoint)!)
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        
        let (data, _) = try await URLSession.shared.data(for: request)
        let state = try JSONDecoder().decode(HAEntityState.self, from: data)
        return state
    }
    
    func discoverEntities() async throws -> [HAEntity] {
        guard let url = baseURL, let token = accessToken else {
            throw HAError.notConfigured
        }
        
        let endpoint = "\(url)/api/states"
        var request = URLRequest(url: URL(string: endpoint)!)
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        
        let (data, _) = try await URLSession.shared.data(for: request)
        let states = try JSONDecoder().decode([HAEntityState].self, from: data)
        
        let entities = states.map { state in
            HAEntity(
                entityId: state.entityId,
                friendlyName: state.attributes.friendlyName ?? state.entityId,
                domain: state.entityId.split(separator: ".").first.map(String.init) ?? "unknown",
                state: state.state
            )
        }
        
        await MainActor.run {
            self.entities = entities
        }
        
        return entities
    }
}

// MARK: - Models

struct HAEntity: Identifiable, Codable {
    let id = UUID()
    let entityId: String
    let friendlyName: String
    let domain: String
    let state: String
}

struct HAEntityState: Codable {
    let entityId: String
    let state: String
    let attributes: HAAttributes
    
    enum CodingKeys: String, CodingKey {
        case entityId = "entity_id"
        case state
        case attributes
    }
}

struct HAAttributes: Codable {
    let friendlyName: String?
    
    enum CodingKeys: String, CodingKey {
        case friendlyName = "friendly_name"
    }
}

struct HACommand: Codable {
    let domain: String
    let service: String
    let entityId: String
    let data: [String: Any]
    let timestamp: Date = Date()
}

enum HAError: Error {
    case notConfigured
    case offline
    case serviceCallFailed(statusCode: Int)
    case invalidResponse
}
```

#### 2.2 Settings UI for Home Assistant

**Location:** `CallJanet-iOS/JanetOS-iOS/Sources/UI/Settings/HomeAssistantSettingsView.swift`

**Purpose:** Configure Home Assistant connection

**Implementation:**

```swift
import SwiftUI

struct HomeAssistantSettingsView: View {
    @StateObject private var manager = HomeAssistantManager.shared
    @State private var url: String = ""
    @State private var token: String = ""
    @State private var connectionStatus: String = ""
    @State private var showingDiscovery = false
    
    var body: some View {
        Form {
            Section("Configuration") {
                TextField("URL", text: $url)
                    .autocapitalization(.none)
                    .keyboardType(.URL)
                    .placeholder("http://homeassistant.local:8123")
                
                SecureField("Access Token", text: $token)
                    .placeholder("Long-lived access token")
                
                Button("Save Configuration") {
                    manager.configure(url: url, token: token)
                    connectionStatus = "Configuration saved"
                }
                .disabled(url.isEmpty || token.isEmpty)
            }
            
            Section("Connection") {
                HStack {
                    Text("Status")
                    Spacer()
                    if manager.isConnected {
                        Text("Connected ✅")
                            .foregroundColor(.green)
                    } else {
                        Text("Not Connected")
                            .foregroundColor(.secondary)
                    }
                }
                
                Button("Test Connection") {
                    Task {
                        let success = await manager.testConnection()
                        connectionStatus = success ? "Connected ✅" : "Connection Failed ❌"
                    }
                }
                
                if !connectionStatus.isEmpty {
                    Text(connectionStatus)
                        .foregroundColor(connectionStatus.contains("✅") ? .green : .red)
                }
            }
            
            Section("Devices") {
                Button("Discover Devices") {
                    showingDiscovery = true
                }
                .disabled(!manager.isConnected)
                
                if !manager.entities.isEmpty {
                    Text("\(manager.entities.count) devices found")
                        .foregroundColor(.secondary)
                }
            }
            
            Section("Help") {
                Link("Home Assistant Setup Guide", destination: URL(string: "https://www.home-assistant.io/installation/")!)
                Link("Create Access Token", destination: URL(string: "https://www.home-assistant.io/docs/authentication/")!)
            }
        }
        .navigationTitle("Home Assistant")
        .onAppear {
            manager.loadConfiguration()
            url = UserDefaults.standard.string(forKey: "home_assistant_url") ?? ""
        }
        .sheet(isPresented: $showingDiscovery) {
            DeviceDiscoveryView()
        }
    }
}

struct DeviceDiscoveryView: View {
    @StateObject private var manager = HomeAssistantManager.shared
    @State private var isLoading = false
    @Environment(\.dismiss) private var dismiss
    
    var body: some View {
        NavigationView {
            List(manager.entities) { entity in
                VStack(alignment: .leading) {
                    Text(entity.friendlyName)
                        .font(.headline)
                    HStack {
                        Text(entity.entityId)
                            .font(.caption)
                            .foregroundColor(.secondary)
                        Spacer()
                        Text(entity.state)
                            .font(.caption)
                            .padding(4)
                            .background(Color.blue.opacity(0.2))
                            .cornerRadius(4)
                    }
                }
            }
            .navigationTitle("Discovered Devices")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Done") {
                        dismiss()
                    }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Refresh") {
                        Task {
                            isLoading = true
                            try? await manager.discoverEntities()
                            isLoading = false
                        }
                    }
                    .disabled(isLoading)
                }
            }
            .overlay {
                if isLoading {
                    ProgressView()
                }
            }
        }
        .task {
            try? await manager.discoverEntities()
        }
    }
}
```

#### 2.3 Integration with DynamicShortcutBuilder

**Location:** `CallJanet-iOS/JanetOS-iOS/Sources/Core/DynamicShortcutBuilder.swift`

**Enhancement:** Add Home Assistant intent recognition

**Add to existing file:**

```swift
// Add to recognizeIntent method
private func recognizeIntent(from text: String) async -> RecognizedIntent? {
    // ... existing code ...
    
    // Check for Home Assistant patterns
    if text.contains("turn on") || text.contains("turn off") || 
       text.contains("toggle") || text.contains("activate") ||
       text.contains("lights") || text.contains("scene") {
        return await recognizeHomeAssistantIntent(from: text)
    }
    
    // ... rest of existing code ...
}

private func recognizeHomeAssistantIntent(from text: String) async -> RecognizedIntent? {
    // Extract action
    let action: String
    if text.contains("turn on") {
        action = "turn_on"
    } else if text.contains("turn off") {
        action = "turn_off"
    } else if text.contains("toggle") {
        action = "toggle"
    } else if text.contains("activate") {
        action = "activate_scene"
    } else {
        return nil
    }
    
    // Extract entity (simplified - can be enhanced with NLP)
    let words = text.lowercased().components(separatedBy: " ")
    var entityHint = ""
    
    if let lightIndex = words.firstIndex(of: "lights") ?? words.firstIndex(of: "light") {
        if lightIndex > 0 {
            entityHint = words[lightIndex - 1]
        }
    }
    
    return RecognizedIntent(
        action: "home_assistant_\(action)",
        parameters: [
            "entity_hint": entityHint,
            "full_text": text
        ],
        confidence: 0.8
    )
}
```

#### 2.4 Offline Mode Integration

**Location:** `CallJanet-iOS/JanetOS-iOS/Sources/Core/OfflineManager.swift`

**Enhancement:** Add HA command queueing

**Add to existing OfflineManager:**

```swift
private var pendingHACommands: [HACommand] = []

func queueHomeAssistantCommand(_ command: HACommand) {
    pendingHACommands.append(command)
    savePendingCommands()
}

func processPendingHACommands() async {
    guard !pendingHACommands.isEmpty else { return }
    
    let commands = pendingHACommands
    pendingHACommands.removeAll()
    savePendingCommands()
    
    for command in commands {
        do {
            try await HomeAssistantManager.shared.callService(
                domain: command.domain,
                service: command.service,
                entityId: command.entityId,
                data: command.data
            )
            print("✅ Executed queued HA command: \(command.entityId)")
        } catch {
            print("⚠️ Failed to execute queued HA command: \(error)")
            // Re-queue if failed
            pendingHACommands.append(command)
        }
    }
    
    savePendingCommands()
}

private func savePendingCommands() {
    // Save to UserDefaults (simplified)
    let encoder = JSONEncoder()
    if let data = try? encoder.encode(pendingHACommands) {
        UserDefaults.standard.set(data, forKey: "pending_ha_commands")
    }
}

private func loadPendingCommands() {
    let decoder = JSONDecoder()
    if let data = UserDefaults.standard.data(forKey: "pending_ha_commands"),
       let commands = try? decoder.decode([HACommand].self, from: data) {
        pendingHACommands = commands
    }
}
```

---

### Phase 3: Apple Watch Implementation

#### 3.1 WatchHomeAssistantManager.swift

**Location:** `CallJanet-iOS/Watch/Sources/Core/WatchHomeAssistantManager.swift`

**Purpose:** Simplified HA manager for watchOS

**Features:**
- Quick actions (turn on/off favorite devices)
- Complications showing device states
- Voice commands via watch
- Haptic feedback on success

**Implementation:** Similar to iOS manager but optimized for watch constraints

---

### Phase 4: JanetOS Desktop Integration

#### 4.1 Janet Desktop HA Dashboard

**Location:** `Janet-Projects/JanetOS/platforms/linux/janet_desktop/ha_dashboard.py`

**Purpose:** Home Assistant dashboard in Janet Desktop

**Features:**
- Grid view of all devices
- Quick controls
- Scene activation
- Real-time state updates via WebSocket

#### 4.2 Voice Control Integration

**Location:** `Janet-Projects/JanetOS/core/keywords.py`

**Enhancement:** Add HA keywords to privilege guard

**Keywords:**
- "turn on [device]"
- "turn off [device]"
- "activate [scene]"
- "what's the temperature"
- "set thermostat to [temp]"

---

### Phase 5: Advanced Features

#### 5.1 Janet Creates Home Assistant Instance

**Acceptance Criteria:** AC-HA4

**Implementation:**
- Docker-based HA installation
- Wizard-guided setup
- Automatic configuration
- Network discovery

**Location:** `Janet-Projects/JanetOS/janet-seed/src/expansion/wizards/home_assistant_installer.py`

#### 5.2 Routine Integration

**Morning Routine:**
- Turn on lights
- Open blinds
- Start coffee maker
- Show weather

**Evening Routine:**
- Turn off lights
- Lock doors
- Set thermostat
- Arm security

**Location:** Integrate with existing routine handlers

#### 5.3 Automation Suggestions

**Features:**
- Janet learns patterns
- Suggests automations
- "You always turn on the lights at 6pm. Should I create an automation?"

---

## Testing Strategy

### Unit Tests

```swift
// HomeAssistantManagerTests.swift

func testConnection() async throws {
    let manager = HomeAssistantManager.shared
    manager.configure(url: "http://test.local:8123", token: "test_token")
    
    let connected = await manager.testConnection()
    XCTAssertTrue(connected)
}

func testTurnOnLight() async throws {
    let manager = HomeAssistantManager.shared
    try await manager.turnOn("light.living_room", brightness: 255)
    
    let state = try await manager.getState(for: "light.living_room")
    XCTAssertEqual(state.state, "on")
}

func testOfflineQueueing() async throws {
    OfflineManager.shared.offlineMode = true
    
    let manager = HomeAssistantManager.shared
    
    do {
        try await manager.turnOn("light.living_room")
        XCTFail("Should throw offline error")
    } catch HAError.offline {
        // Expected
    }
    
    XCTAssertEqual(OfflineManager.shared.pendingHACommandsCount, 1)
}
```

### Integration Tests

1. **End-to-End Voice Command**
   - Say "Hey Janet, turn on living room lights"
   - Verify light turns on
   - Verify shortcut created
   - Verify Siri phrase works

2. **Offline Mode**
   - Disconnect network
   - Issue command
   - Verify queued
   - Reconnect
   - Verify executed

3. **Multi-Platform**
   - Issue command on iPhone
   - Verify works on Watch
   - Verify works on JanetOS desktop

---

## Acceptance Criteria Coverage

### AC-HA1: Janet can control Home Assistant ✅
- Voice commands work
- Text commands work
- Confirmation provided

### AC-HA2: Official API usage ✅
- REST API for service calls
- WebSocket for real-time updates (optional)
- Local communication only

### AC-HA3: HA client/handler ✅
- `HomeAssistantClient` in janet-seed
- `HomeAssistantManager` in iOS
- Configuration documented

### AC-HA4: Janet can create HA instance 🔄
- Docker-based installation
- Wizard-guided setup
- Automatic configuration

---

## Security & Privacy

### Constitutional AI Compliance

**Soul Check triggers:**
- Unlocking doors
- Disabling security
- Temperature changes >10°F
- Any "destructive" action

### Token Security

- iOS Keychain storage
- Never logged
- User can revoke anytime
- Secure transmission only

### Local-First

- All communication on LAN
- No cloud dependencies
- Data never leaves home network
- Works offline (with queueing)

---

## Documentation Updates

### Files to Update

1. **CallJanet-iOS/COMPLETE_IOS_DOCUMENTATION.md**
   - Add Home Assistant section
   - Document configuration
   - Add troubleshooting

2. **Janet-Projects/JanetOS/DOCUMENTATION_INDEX.md**
   - Add HA integration guide
   - Link to iOS docs

3. **.cursor/AGENT_KNOWLEDGE.md**
   - Update with HA implementation details
   - Add troubleshooting guide

4. **Janet-Projects/README.md**
   - Update feature list
   - Add HA to status

---

## Timeline

### Week 1: iOS Core (Phase 2.1-2.2)
- [ ] Implement `HomeAssistantManager.swift`
- [ ] Create Settings UI
- [ ] Test connection and basic controls
- [ ] Update documentation

### Week 2: iOS Advanced (Phase 2.3-2.4)
- [ ] Integrate with DynamicShortcutBuilder
- [ ] Implement offline queueing
- [ ] Add Siri intent donation
- [ ] Create shortcuts for common actions

### Week 3: Watch & Desktop (Phase 3-4)
- [ ] Implement Watch manager
- [ ] Add complications
- [ ] Create desktop dashboard
- [ ] Integrate with voice keywords

### Week 4: Advanced Features (Phase 5)
- [ ] Janet creates HA instance
- [ ] Routine integration
- [ ] Automation suggestions
- [ ] Comprehensive testing

---

## Success Metrics

### Functional
- ✅ User can control devices via voice
- ✅ Shortcuts created automatically
- ✅ Siri integration works
- ✅ Offline mode queues commands
- ✅ Works across all platforms

### Performance
- ⚡ <500ms response time for local commands
- ⚡ <2s for shortcut creation
- ⚡ <100ms for offline queueing

### User Experience
- 😊 Intuitive setup process
- 😊 Clear error messages
- 😊 Seamless offline/online transitions
- 😊 Consistent across platforms

---

## Next Steps

1. **Review this plan** with team/stakeholders
2. **Start with Phase 2.1** - iOS HomeAssistantManager
3. **Test incrementally** - don't wait for full implementation
4. **Update documentation** as you go
5. **Get user feedback** early and often

---

## Questions & Decisions

### Open Questions
1. Should we support HomeKit as alternative to HA?
2. Do we need WebSocket support for real-time updates?
3. Should Janet suggest automations proactively?
4. What's the minimum HA version we support?

### Decisions Made
- ✅ Use REST API (not MQTT)
- ✅ Local-only communication
- ✅ Offline queueing required
- ✅ Constitutional AI applies to HA commands

---

## References

- [Home Assistant Docs](https://developers.home-assistant.io/)
- [REST API Reference](https://developers.home-assistant.io/docs/api/rest/)
- [iOS Companion App](https://companion.home-assistant.io/)
- [JanetOS Acceptance Criteria](Janet-Projects/JanetOS/docs/ACCEPTANCE_CRITERIA.md)
- [iOS Complete Documentation](CallJanet-iOS/COMPLETE_IOS_DOCUMENTATION.md)

---

**Status:** Ready to implement  
**Owner:** Development team  
**Last Updated:** 2026-03-02

---

*This plan maintains Janet's core principles: offline-first, privacy-first, constitutional AI, and voice-first interaction.*
