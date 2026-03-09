# Janet Dashboard Setup Guide

Add Janet to your Home Assistant dashboard in a few steps.

## 💬 Text to Janet (Type & Send)

**The main feature**: Type any message and send it to Janet from your dashboard.

### Step 1: Create Input Text Helper (one-time setup)

1. Go to **Settings** → **Devices & Services** → **Helpers**
2. Click **+ Create Helper**
3. Choose **Text**
4. Set **Name** to: `Message to Janet`
5. Set **Entity ID** to: `input_text.janet_message` (or leave auto-generated, then update the card's entity_id to match)
6. Click **Create**

### Step 2: Add the Text-to-Janet Card

1. Edit your dashboard → **Add card** → **Manual**
2. Paste this YAML:

```yaml
type: vertical-stack
cards:
  - type: entities
    title: Text to Janet
    icon: mdi:message-text
    entities:
      - entity: input_text.janet_message
        name: Message
        icon: mdi:chat
  - type: horizontal-stack
    cards:
      - type: button
        name: Send to Janet
        tap_action:
          action: call-service
          service: janet.command
          service_data:
            command: "{{ states('input_text.janet_message') }}"
        icon: mdi:send
        show_state: false
      - type: button
        name: Clear
        tap_action:
          action: call-service
          service: input_text.set_value
          service_data:
            entity_id: input_text.janet_message
            value: ""
        icon: mdi:eraser
        show_state: false
```

3. If your helper has a different entity_id (e.g. `input_text.message_to_janet`), replace `input_text.janet_message` everywhere in the YAML.
4. Save the card and dashboard.

---

## Quick Method (Status Cards)

### 1. Edit Your Dashboard

1. Go to your **Overview** (or any dashboard)
2. Click the **three dots** (⋮) in the top right
3. Click **Edit dashboard**
4. Click **Add card** (bottom right)
5. Scroll down and select **Manual**

### 2. Paste This Card

Copy and paste this YAML for a complete Janet card:

```yaml
type: entities
title: Janet AI Companion
icon: mdi:robot
show_header_toggle: false
entities:
  - entity: sensor.janet_status
    name: Status
    icon: mdi:robot
  - entity: sensor.janet_conversation
    name: Conversation
    icon: mdi:message-text
  - entity: sensor.janet_memory
    name: Memory
    icon: mdi:database
    unit: MB
```

6. Click **Save**
7. Click **Save** again to save the dashboard

---

## Alternative: Add via UI (No YAML)

### Option A: Entities Card

1. **Edit Dashboard** → **Add card**
2. Choose **Entities**
3. Click **Choose entity** for each:
   - `sensor.janet_status`
   - `sensor.janet_conversation`
   - `sensor.janet_memory`
4. Set **Card title** to "Janet AI Companion"
5. Save

### Option B: Glance Card (Compact)

1. **Edit Dashboard** → **Add card**
2. Choose **Glance**
3. Add the three sensors above
4. Save

### Option C: Single Entity Card

1. **Edit Dashboard** → **Add card**
2. Choose **Entity**
3. Select `sensor.janet_status`
4. Optionally set icon to `mdi:robot`
5. Save

---

## Card with Quick Actions (Speak & Command)

Add a card with buttons to trigger Janet:

```yaml
type: vertical-stack
cards:
  - type: entities
    title: Janet AI Companion
    icon: mdi:robot
    entities:
      - entity: sensor.janet_status
      - entity: sensor.janet_conversation
      - entity: sensor.janet_memory
  - type: horizontal-stack
    cards:
      - type: button
        name: Speak
        tap_action:
          action: call-service
          service: janet.speak
          service_data:
            message: "Hello from dashboard"
        icon: mdi:microphone
      - type: button
        name: Command
        tap_action:
          action: call-service
          service: janet.command
          service_data:
            command: "What time is it?"
        icon: mdi:chat
```

---

## Entity IDs

**Janet sensors:**
- `sensor.janet_status`
- `sensor.janet_conversation`
- `sensor.janet_memory`

**Text-to-Janet (helper you create):**
- `input_text.janet_message` — the input field for typing messages

Find Janet entities: **Settings** → **Devices & Services** → **Janet AI Companion** → **Entities**

---

## Troubleshooting

**Entities not found?**
- Ensure the Janet integration is configured
- Restart Home Assistant
- Check Settings → Devices & Services for "Janet AI Companion"

**Card shows "Entity not available"?**
- Start the Janet API server on your Mac
- Verify the integration can connect

**"Text to Janet" card shows "Entity not available"?**
- Create the Input Text helper first (Step 1 above)
- Ensure entity_id matches: `input_text.janet_message`
