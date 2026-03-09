# Fix Home Assistant Firewall Issue

## 🔍 Problem Identified

**Port 8123 is FILTERED** - The Raspberry Pi firewall is blocking connections.

```
PORT     STATE    SERVICE
8123/tcp filtered polipo
```

This means:
- ✅ Home Assistant is running
- ✅ Your Mac can see the device
- ❌ Firewall is blocking port 8123

## 🔧 Solution: Open Port 8123 on Raspberry Pi

### Option 1: SSH into Raspberry Pi

If you can SSH into your Raspberry Pi:

```bash
# SSH into the Pi
ssh pi@192.168.0.25
# or
ssh homeassistant@192.168.0.25

# Check firewall status
sudo ufw status

# Allow port 8123
sudo ufw allow 8123/tcp

# Verify it's allowed
sudo ufw status | grep 8123
```

### Option 2: Using iptables

If UFW isn't installed:

```bash
# Check current rules
sudo iptables -L -n | grep 8123

# Allow port 8123
sudo iptables -I INPUT -p tcp --dport 8123 -j ACCEPT

# Save the rules (Debian/Raspbian)
sudo iptables-save | sudo tee /etc/iptables/rules.v4

# Or on some systems
sudo service iptables save
```

### Option 3: Home Assistant OS

If you're running Home Assistant OS (not Raspbian), you may need to:

1. Access Home Assistant via the web interface from another device
2. Go to Settings → System → Network
3. Check firewall settings
4. Or access via the console (connect keyboard/monitor to Pi)

### Option 4: Router Configuration

Some routers have firewall rules. Check your router settings:

1. Login to router (usually `http://192.168.0.1`)
2. Look for "Firewall" or "Port Forwarding" settings
3. Ensure port 8123 is not blocked for `192.168.0.25`

## ✅ Testing After Fix

Once you've opened the port, test from your Mac:

```bash
# Test with curl
curl -I http://192.168.0.25:8123

# Test with token
curl -X GET \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  http://192.168.0.25:8123/api/

# Or use the test script
cd /Users/mzxzd/Documents/Janet-Projects/janet-max
./test-ha-connection.sh "YOUR_TOKEN"
```

Should return:
```
HTTP/1.1 200 OK
```

## 🚀 After Fixing

Once the firewall is fixed, run janet-max:

```bash
cd /Users/mzxzd/Documents/Janet-Projects/janet-max
janet src/main.janet
```

You should see:
```
Home Assistant module initialized, URL: http://192.168.0.25:8123
Connected to Home Assistant WebSocket
```

## 📋 Configuration Already Done

I've already configured janet-max for you:

✅ **config/secrets.janet** - Created with your token  
✅ **config/default.janet** - Updated with correct URL (`http://192.168.0.25:8123`)

All you need to do is fix the firewall!

## 🆘 Can't SSH?

If you can't SSH into the Raspberry Pi:

1. **Physical Access**: Connect keyboard/monitor to the Pi
2. **Other Device**: Try accessing HA from your phone/tablet - if it works, the firewall might only be blocking your Mac
3. **Restart**: Try restarting the Raspberry Pi
4. **Check HA Documentation**: https://www.home-assistant.io/docs/configuration/securing/

## 📊 Current Status

```
✅ Home Assistant found: 192.168.0.25:8123
✅ Token obtained and saved
✅ janet-max configured
✅ Device is reachable (ARP/routing)
❌ Port 8123 filtered by firewall
```

**Next Step**: Open port 8123 on the Raspberry Pi firewall

---

**Priority**: HIGH - This is the only remaining blocker  
**Estimated Time**: 5 minutes once you have SSH access  
**Last Updated**: 2026-03-02
