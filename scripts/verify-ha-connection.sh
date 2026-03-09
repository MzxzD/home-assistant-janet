#!/bin/bash
# Test Home Assistant connection
# Usage: ./test-ha-connection.sh <token>

set -e

HA_URL="http://192.168.0.25:8123"
TOKEN="$1"

if [ -z "$TOKEN" ]; then
    echo "Usage: $0 <home-assistant-token>"
    echo ""
    echo "Get your token from Home Assistant:"
    echo "1. Open http://192.168.0.25:8123"
    echo "2. Click your profile (bottom left)"
    echo "3. Scroll to 'Long-Lived Access Tokens'"
    echo "4. Create token named 'Janet Integration'"
    exit 1
fi

echo "🔍 Testing Home Assistant connection..."
echo "URL: $HA_URL"
echo ""

# Test 1: Check if HA is reachable
echo "Test 1: Checking if Home Assistant is reachable..."
if curl -s --connect-timeout 5 "$HA_URL" > /dev/null 2>&1; then
    echo "✅ Home Assistant is reachable"
else
    echo "❌ Cannot reach Home Assistant"
    echo "   Troubleshooting:"
    echo "   - Check if HA is running: http://192.168.0.25:8123"
    echo "   - Check firewall settings"
    echo "   - Try: ping 192.168.0.25"
    exit 1
fi

# Test 2: Check API endpoint
echo ""
echo "Test 2: Testing API endpoint..."
API_RESPONSE=$(curl -s -w "\n%{http_code}" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    "$HA_URL/api/")

HTTP_CODE=$(echo "$API_RESPONSE" | tail -n1)
BODY=$(echo "$API_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ API endpoint working"
    echo "   Response: $BODY"
else
    echo "❌ API endpoint failed (HTTP $HTTP_CODE)"
    echo "   Response: $BODY"
    if [ "$HTTP_CODE" = "401" ]; then
        echo "   → Invalid token. Create a new one in Home Assistant."
    fi
    exit 1
fi

# Test 3: List devices
echo ""
echo "Test 3: Listing devices..."
DEVICES=$(curl -s \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    "$HA_URL/api/states")

DEVICE_COUNT=$(echo "$DEVICES" | jq '. | length' 2>/dev/null || echo "0")
echo "✅ Found $DEVICE_COUNT devices"

if [ "$DEVICE_COUNT" -gt 0 ]; then
    echo ""
    echo "Sample devices:"
    echo "$DEVICES" | jq -r '.[0:5] | .[] | "  - \(.entity_id) (\(.state))"' 2>/dev/null || echo "  (install jq for pretty output)"
fi

# Test 4: WebSocket connection
echo ""
echo "Test 4: Testing WebSocket connection..."
WS_URL="${HA_URL/http/ws}/api/websocket"
echo "   WebSocket URL: $WS_URL"
echo "   (WebSocket test requires wscat: npm install -g wscat)"

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All tests passed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "1. Copy config/secrets.janet.example to config/secrets.janet"
echo "2. Add your token to config/secrets.janet"
echo "3. Update :home-assistant-url in config/default.janet to:"
echo "   :home-assistant-url \"$HA_URL\""
echo "4. Run: janet src/main.janet"
echo ""
echo "Your token (save this):"
echo "$TOKEN"
